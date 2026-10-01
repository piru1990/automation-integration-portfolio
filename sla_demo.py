"""Independent offline example: closed-ticket SLA in elapsed hours."""
import json
from datetime import datetime


def timestamp(value):
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError('timezone required')
    return parsed


def sla_summary(tickets, target_hours=24):
    if target_hours <= 0:
        raise ValueError('positive target required')
    resolved, durations, seen, excluded = [], [], set(), 0
    for ticket in tickets:
        if ticket['id'] in seen:
            raise ValueError('duplicate ticket ID')
        seen.add(ticket['id'])
        if ticket['status'] not in ('resolved', 'open', 'cancelled', 'duplicate'):
            raise ValueError('invalid status')
        if ticket['status'] != 'resolved':
            excluded += 1
            continue
        elapsed = (timestamp(ticket['closed_at']) - timestamp(ticket['created_at'])).total_seconds() / 3600
        if elapsed < 0:
            raise ValueError('closure precedes creation')
        durations.append(elapsed)
        resolved.append(elapsed <= target_hours)
    count = len(resolved)
    return {
        'target_hours': target_hours, 'resolved': count, 'excluded': excluded,
        'within_sla': sum(resolved), 'breached': count - sum(resolved),
        'compliance_pct': round(sum(resolved) / count * 100, 2) if count else None,
        'mean_resolution_hours': round(sum(durations) / count, 2) if count else None,
    }


def demonstration():
    tickets = [
        {'id': 'DEMO-1', 'status': 'resolved', 'created_at': '2026-09-01T09:00:00+00:00', 'closed_at': '2026-09-02T09:00:00+00:00'},
        {'id': 'DEMO-2', 'status': 'resolved', 'created_at': '2026-09-01T09:00:00+00:00', 'closed_at': '2026-09-02T10:00:00+00:00'},
        {'id': 'DEMO-3', 'status': 'cancelled'},
        {'id': 'DEMO-4', 'status': 'duplicate'},
        {'id': 'DEMO-5', 'status': 'open'},
    ]
    return sla_summary(tickets)


if __name__ == '__main__':
    print(json.dumps(demonstration(), indent=2))
