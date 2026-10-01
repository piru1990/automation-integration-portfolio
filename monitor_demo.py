"""Independent offline example: sample availability, not a production SLA."""
import json
from datetime import datetime, timezone


def sample_summary(samples):
    buckets = {}
    seen = set()
    for sample in samples:
        key = (sample['service'], sample['at'])
        if key in seen:
            raise ValueError('duplicate service/timestamp sample')
        seen.add(key)
        status = sample['status']
        if status not in ('up', 'down', 'unknown'):
            raise ValueError('invalid status')
        stamp = datetime.fromisoformat(sample['at'])
        if stamp.tzinfo is None:
            raise ValueError('timezone required')
        buckets.setdefault(sample['service'], []).append((stamp, status))
    result = {}
    for service, rows in sorted(buckets.items()):
        known = [state for _, state in rows if state != 'unknown']
        up = known.count('up')
        result[service] = {
            'samples': len(rows), 'known_samples': len(known),
            'unknown_samples': len(rows) - len(known),
            'availability_pct': round(up / len(known) * 100, 2) if known else None,
            'latest_status': max(rows, key=lambda r: r[0])[1],
        }
    return result


def simulate_probe(service, at, probe):
    try:
        status = 'up' if probe() else 'down'
    except TimeoutError:
        status = 'down'
    except Exception:
        status = 'unknown'
    return {'service': service, 'at': at, 'status': status}


def demonstration():
    history = [
        {'service': 'demo-erp', 'at': '2026-09-01T10:00:00+00:00', 'status': 'up'},
        {'service': 'demo-erp', 'at': '2026-09-01T10:05:00+00:00', 'status': 'down'},
        {'service': 'demo-erp', 'at': '2026-09-01T10:10:00+00:00', 'status': 'up'},
        {'service': 'demo-mail', 'at': '2026-09-01T10:00:00+00:00', 'status': 'unknown'},
    ]
    return sample_summary(history)


if __name__ == '__main__':
    print(json.dumps(demonstration(), indent=2))
