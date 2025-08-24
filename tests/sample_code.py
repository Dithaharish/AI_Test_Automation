def add(a, b):
    """Simple addition function."""
    return a + b


def subtract(a, b):
    """Simple subtraction function."""
    return a - b


def multiply(a, b):
    """Simple multiplication function."""
    return a * b


def divide(a, b):
    """Division function with zero check."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def login(username, password):
    """Mock login function for testing."""
    valid_users = {
        'user': 'pass',
        'admin': 'admin123',
        'testuser': 'testpass'
    }

    if username in valid_users and valid_users[username] == password:
        return {
            'status': 'success',
            'user_id': hash(username),
            'username': username
        }
    return {
        'status': 'failure',
        'error': 'Invalid credentials'
    }


def validate_email(email: str) -> bool:
    """Better email validation function."""
    if "@" not in email or "." not in email:
        return False

    parts = email.split("@")
    if len(parts) != 2:  # more than one '@'
        return False

    local, domain = parts
    if not local or not domain:  # empty before/after '@'
        return False

    if "." not in domain:  # domain must contain dot
        return False

    return True


def calculate_discount(price, discount_percent):
    """Calculate discounted price."""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount percent must be between 0 and 100")

    discount_amount = price * (discount_percent / 100)
    return price - discount_amount


class Calculator:
    """Simple calculator class for testing."""

    def __init__(self):
        self.history = []

    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []
