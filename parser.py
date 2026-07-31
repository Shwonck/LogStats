import re
from datetime import datetime

LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+)\s+'                # IP do cliente
    r'\S+\s+\S+\s+'                   # Dois campos ignoráveis (ex: - -)
    r'\[(?P<timestamp>[^\]]+)\]\s+'   # Timestamp entre colchetes
    r'"(?P<method>\S+)\s+(?P<endpoint>\S+)\s+(?P<protocol>[^"]+)"\s+' # Requisição entre aspas
    r'(?P<status>\d{3})\s+'           # Código de status (3 dígitos)
    r'(?P<bytes>\d+|-)\s+'            # Tamanho da resposta em bytes (ou -)
    r'(?P<response_time>\d+(?:\.\d+)?)$' # Tempo de resposta em segundos (int ou float)
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
    
    except(ValueError, KeyError): #### Tratar posteriormente

        return None