"""Independent offline example: idempotent one-way synchronization.

No network calls or real ticket closures. --store is an optional local JSON file.
"""
import argparse
import json
import os
import tempfile
from pathlib import Path


class MockTaskAdapter:
    def __init__(self, tasks=None):
        self.tasks = {} if tasks is None else {key: dict(value) for key, value in tasks.items()}
        self.writes = 0

    def upsert(self, external_key, payload):
        if self.tasks.get(external_key) == payload:
            return 'unchanged'
        action = 'created' if external_key not in self.tasks else 'updated'
        self.tasks[external_key] = dict(payload)
        self.writes += 1
        return action


def sync_tickets(tickets, adapter):
    validated, seen = [], set()
    for ticket in tickets:
        external_key = 'helpdesk:' + str(ticket['id'])
        if not str(ticket['id']).strip() or external_key in seen:
            raise ValueError('missing or duplicate ticket ID')
        if ticket['status'] not in ('open', 'resolved'):
            raise ValueError('unsupported status')
        seen.add(external_key)
        validated.append((external_key, {
            'title': ticket['title'],
            'status': 'done' if ticket['status'] == 'resolved' else 'todo',
        }))
    changes = {'created': 0, 'updated': 0, 'unchanged': 0}
    for key, payload in validated:
        changes[adapter.upsert(key, payload)] += 1
    return changes


def save_store(path, tasks):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, delete=False) as handle:
        temp = Path(handle.name)
        json.dump(tasks, handle, indent=2)
    try:
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def demonstration(store=None):
    tasks = json.loads(Path(store).read_text()) if store and Path(store).exists() else {}
    adapter = MockTaskAdapter(tasks)
    tickets = [
        {'id': 'DEMO-1', 'title': 'Example service check', 'status': 'open'},
        {'id': 'DEMO-2', 'title': 'Example integration fix', 'status': 'resolved'},
    ]
    first = sync_tickets(tickets, adapter)
    second = sync_tickets(tickets, adapter)
    if store:
        save_store(store, adapter.tasks)
    return {'first_run': first, 'repeated_run': second, 'task_count': len(adapter.tasks), 'writes': adapter.writes}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store', help='Optional path for local simulated tasks')
    print(json.dumps(demonstration(parser.parse_args().store), indent=2))
