from datetime import datetime, timezone
import pytest
from parser import parse_line


def test_parse_valid_line():
    line = '10.0.0.14 - - [21/Jul/2026:10:15:32 +0000] "GET /api/users HTTP/1.1" 200 1043 0.042'
    result = parse_line(line)

    assert result is not None
    assert result['ip'] == "10.0.0.14"
    assert result['method'] == "GET"
    assert result['endpoint'] == "/api/users"
    assert result['protocol'] == "HTTP/1.1"
    assert result['status'] == 200
    assert result['bytes'] == 1043
    assert result['response_time'] == 0.042
    
    ''' Validate timestamp convertion to UTC timezone '''
    expected_dt = datetime(2026, 7, 21, 10, 15, 32, tzinfo=timezone.utc)
    assert result['timestamp'] == expected_dt


def test_parse_dash_bytes():
    line = '10.0.3.185 - - [21/Jul/2026:09:00:39 +0000] "GET /static/style.css HTTP/1.1" 304 - 0.007'
    result = parse_line(line)

    assert result is not None
    assert result['status'] == 304
    assert result['bytes'] == 0


@pytest.mark.parametrize("malformed_line", [
    "",
    "   ",
    "#### log rotated ####",
    "10.0.1.55 - - [21/Jul/2026:09:41:02 +0000] \"GET /api/users HTTP/1.1\" 200",
    "10.0.1.203 - - [21/Jul/2026:10:44:08 +0000] \"POST /api/orders HTTP/1.1\" 201 4410 not_a_number",
    "10.0.0.99 - - [32/Jul/2026:99:99:99 +0000] \"GET /health HTTP/1.1\" 200 12 0.002",
    "10.0.2.11 - - [21/Jul/2026:10:03:19 +0000] \"GET /api/orders HTTP/1.1\" abc 1200 0.150",
])
def test_parse_malformed_lines(malformed_line):
    result = parse_line(malformed_line)
    assert result is None