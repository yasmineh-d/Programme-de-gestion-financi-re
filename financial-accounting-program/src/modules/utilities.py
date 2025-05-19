def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_currency(amount):
    return f"{amount:,.2f} ر.س"

def calculate_percentage(part, whole):
    if whole == 0:
        return 0
    return (part / whole) * 100

def sanitize_input(input_string):
    return input_string.strip()