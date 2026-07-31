import statistics
from collections import Counter, defaultdict
import LogEntry

'''
LogStats Metrics Aggregator

- Accumulates and computes statistical metrics from parsed log entries:
- Records the total number of read, processed, and discarded (malformed) lines.
- Groups HTTP status codes into 2xx, 3xx, 4xx, and 5xx classes.
- Ranks top endpoints by total request volume and average response time.
- Calculates overall p95 response time latency.
'''

class LogStats:
    def __init__(self, since=None):
        self.since = since
        self.total_lines_since = 0
        self.total_lines = 0
        self.discarded_lines = 0
        self.status_counts = Counter()
        self.endpoint_counts = Counter()
        self.endpoint_times = defaultdict(list)
        self.all_response_times = []

    def recorded_malformed(self):
        self.total_lines += 1
        self.discarded_lines += 1

    def add_entry(self, entry: LogEntry):

        self.total_lines += 1

        # Flag filter --since
        if self.since and entry['timestamp'] < self.since:
            return

        self.total_lines_since += 1
        status_group = f"{entry['status'] // 100}xx"
        self.status_counts[status_group] += 1

        self.endpoint_counts[entry['endpoint']] += 1
        self.endpoint_times[entry['endpoint']].append(entry['response_time'])

        self.all_response_times.append(entry['response_time'])

    def calculate_results(self) -> dict:
        top_5_reqs = self.endpoint_counts.most_common(5)
        avg_times = Counter({
            ep: sum(times)/len(times)
            for ep, times in self.endpoint_times.items() if times
        })

        top_5_avg_times = avg_times.most_common(5)

        p95 = 0.0
        if self.all_response_times:
            p95 = statistics.quantiles(self.all_response_times, n=100)[94]

        return {
            "total_lines": self.total_lines,
            "total_processed": self.total_lines_since,
            "discarded": self.discarded_lines,
            "status_counts": dict(self.status_counts),
            "top_5_requests": top_5_reqs,
            "top_5_avg_latency": top_5_avg_times,
            "p95_latency": round(p95, 4),
        }