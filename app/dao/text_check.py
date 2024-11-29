import re







def check_value(value):
    pattern = re.compile(r'^[a-zA-Z0-9]+$')
    return pattern.match(value) is not None

def check_for_malicious_code(value):
    pattern = re.compile(r'[\x00-\x1f\x7f-\xff]')
    return pattern.search(value) is None
