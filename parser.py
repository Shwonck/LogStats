import re
from datetime import datetime

'''
Common Log Format specification:
- ip: Client IPv4 address
- timestamp: Date, time, and UTC offset [DD/Mon/YYYY:HH:MM:SS +0000]
- method: HTTP request method (GET, POST, etc.)
- endpoint: Requested URI path
- protocol: HTTP protocol version (e.g., HTTP/1.1)
- status: 3-digit HTTP response status code
- bytes: Response body payload size in bytes
- response_time: Total request processing duration in seconds
'''

LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+)\s+'
    r'\S+\s+\S+\s+'
    r'\[(?P<timestamp>[^\]]+)\]\s+'
    r'"(?P<method>\S+)\s+(?P<endpoint>\S+)\s+(?P<protocol>[^"]+)"\s+'
    r'(?P<status>\d{3})\s+'
    r'(?P<bytes>\d+|-)\s+'
    r'(?P<response_time>\d+(?:\.\d+)?)$'
)

def parse_line(log_line):

    match = LOG_PATTERN.match(log_line.strip())

    if not match:
        return None

    data = match.groupdict()

    try:

        parsed_data = {
            'ip': data['ip'],
            'timestamp': datetime.strptime(data['timestamp'], "%d/%b/%Y:%H:%M:%S %z"),
            'method': data['method'],
            'endpoint': data['endpoint'],
            'protocol': data['protocol'],
            'status': int(data['status']),
            'bytes': 0 if data['bytes'] == '-' else int(data['bytes']),
            'response_time': float(data['response_time'])
        }
        return parsed_data
    
    except(ValueError, KeyError):
        return None