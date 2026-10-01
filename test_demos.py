import json
import tempfile
import unittest
from pathlib import Path
from monitor_demo import sample_summary, simulate_probe
from sla_demo import sla_summary
from sync_demo import MockTaskAdapter, sync_tickets, save_store


class MonitoringTests(unittest.TestCase):
    def test_outage_and_unknown_are_distinct(self):
        rows = [{'service': 'example', 'at': f'2026-09-01T10:0{i}:00+00:00', 'status': state} for i, state in enumerate(['up', 'down', 'unknown'])]
        result = sample_summary(rows)['example']
        self.assertEqual(result['availability_pct'], 50)
        self.assertEqual(result['unknown_samples'], 1)
        self.assertEqual(result['latest_status'], 'unknown')

    def test_empty_and_no_known_observations(self):
        self.assertEqual(sample_summary([]), {})
        self.assertIsNone(sample_summary([{'service': 'example', 'at': '2026-09-01T10:00:00+00:00', 'status': 'unknown'}])['example']['availability_pct'])

    def test_timeout_is_down(self):
        def timeout(): raise TimeoutError()
        self.assertEqual(simulate_probe('example', '2026-09-01T10:00:00+00:00', timeout)['status'], 'down')

    def test_duplicate_sample_rejected(self):
        row = {'service': 'example', 'at': '2026-09-01T10:00:00+00:00', 'status': 'up'}
        with self.assertRaises(ValueError): sample_summary([row, row])


class SLATests(unittest.TestCase):
    def ticket(self, close):
        return {'id': 'DEMO-1', 'status': 'resolved', 'created_at': '2026-09-01T09:00:00+00:00', 'closed_at': close}

    def test_exact_boundary_and_one_second_breach(self):
        self.assertEqual(sla_summary([self.ticket('2026-09-02T09:00:00+00:00')])['within_sla'], 1)
        self.assertEqual(sla_summary([self.ticket('2026-09-02T09:00:01+00:00')])['breached'], 1)

    def test_timezone_equivalence(self):
        self.assertEqual(sla_summary([self.ticket('2026-09-02T03:00:00-06:00')])['within_sla'], 1)

    def test_exclusions_and_zero_denominator(self):
        rows = [{'id': str(i), 'status': state} for i, state in enumerate(['open', 'cancelled', 'duplicate'])]
        result = sla_summary(rows)
        self.assertEqual(result['excluded'], 3)
        self.assertIsNone(result['compliance_pct'])

    def test_invalid_duration_target_and_duplicate(self):
        with self.assertRaises(ValueError): sla_summary([self.ticket('2026-09-01T08:00:00+00:00')])
        with self.assertRaises(ValueError): sla_summary([], 0)
        with self.assertRaises(ValueError): sla_summary([self.ticket('2026-09-02T09:00:00+00:00')] * 2)


class SyncTests(unittest.TestCase):
    def ticket(self, status='open'):
        return {'id': 'DEMO-1', 'title': 'Example', 'status': status}

    def test_replay_and_update_without_duplicates(self):
        adapter = MockTaskAdapter()
        self.assertEqual(sync_tickets([self.ticket()], adapter)['created'], 1)
        self.assertEqual(sync_tickets([self.ticket()], adapter)['unchanged'], 1)
        self.assertEqual(sync_tickets([self.ticket('resolved')], adapter)['updated'], 1)
        self.assertEqual(len(adapter.tasks), 1)
        self.assertEqual(adapter.writes, 2)

    def test_replay_after_reload(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'tasks.json'
            adapter = MockTaskAdapter()
            sync_tickets([self.ticket()], adapter)
            save_store(path, adapter.tasks)
            reloaded = MockTaskAdapter(json.loads(path.read_text()))
            self.assertEqual(sync_tickets([self.ticket()], reloaded)['unchanged'], 1)
            self.assertEqual(reloaded.writes, 0)

    def test_validation_prevents_partial_write(self):
        adapter = MockTaskAdapter()
        with self.assertRaises(ValueError): sync_tickets([self.ticket(), self.ticket('resolved')], adapter)
        self.assertEqual(adapter.tasks, {})

    def test_retry_after_adapter_failure(self):
        class FailOnce(MockTaskAdapter):
            failed = False
            def upsert(self, key, payload):
                if key.endswith('DEMO-2') and not self.failed:
                    self.failed = True
                    raise ConnectionError('simulated failure')
                return super().upsert(key, payload)
        tickets = [self.ticket(), {'id': 'DEMO-2', 'title': 'Second example', 'status': 'open'}]
        adapter = FailOnce()
        with self.assertRaises(ConnectionError): sync_tickets(tickets, adapter)
        result = sync_tickets(tickets, adapter)
        self.assertEqual(result, {'created': 1, 'updated': 0, 'unchanged': 1})
        self.assertEqual(len(adapter.tasks), 2)


if __name__ == '__main__':
    unittest.main()
