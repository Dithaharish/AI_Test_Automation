import pytest
from tests.sample_code import (
    add, subtract, multiply, divide, login,
    validate_email, calculate_discount, Calculator
)
class TestMathFunctions:
    """Test cases for basic math functions."""

    def test_add_positive_numbers(self):
        """Test addition with positive numbers."""
        assert add(2, 3) == 5
        assert add(10, 15) == 25
        assert add(0, 5) == 5

    def test_add_negative_numbers(self):
        """Test addition with negative numbers."""
        assert add(-2, -3) == -5
        assert add(-10, 5) == -5
        assert add(10, -5) == 5

    def test_add_zero(self):
        """Test addition with zero."""
        assert add(0, 0) == 0
        assert add(5, 0) == 5
        assert add(0, -5) == -5

    def test_subtract(self):
        """Test subtraction function."""
        assert subtract(5, 3) == 2
        assert subtract(10, 15) == -5
        assert subtract(0, 5) == -5

    def test_multiply(self):
        """Test multiplication function."""
        assert multiply(2, 3) == 6
        assert multiply(-2, 3) == -6
        assert multiply(0, 5) == 0

    def test_divide_valid(self):
        """Test division with valid inputs."""
        assert divide(6, 2) == 3
        assert divide(5, 2) == 2.5
        assert divide(-6, 2) == -3

    def test_divide_by_zero(self):
        """Test division by zero raises error."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5, 0)


class TestLoginFunction:
    """Test cases for login functionality."""

    def test_login_valid_credentials(self):
        """Test login with valid credentials."""
        result = login('user', 'pass')
        assert result['status'] == 'success'
        assert result['username'] == 'user'
        assert 'user_id' in result

    def test_login_valid_admin(self):
        """Test login with admin credentials."""
        result = login('admin', 'admin123')
        assert result['status'] == 'success'
        assert result['username'] == 'admin'

    def test_login_invalid_password(self):
        """Test login with invalid password."""
        result = login('user', 'wrongpass')
        assert result['status'] == 'failure'
        assert 'error' in result

    def test_login_invalid_username(self):
        """Test login with invalid username."""
        result = login('invaliduser', 'pass')
        assert result['status'] == 'failure'
        assert 'error' in result

    def test_login_empty_credentials(self):
        """Test login with empty credentials."""
        result = login('', '')
        assert result['status'] == 'failure'
        assert 'error' in result


class TestEmailValidation:
    """Test cases for email validation."""

    def test_valid_emails(self):
        """Test valid email addresses."""
        assert validate_email('test@example.com') is True
        assert validate_email('user.name@domain.co.uk') is True
        assert validate_email('admin@company.org') is True

    def test_invalid_emails(self):
        """Test invalid email addresses."""
        assert validate_email('invalid.email') is False
        assert validate_email('test@') is False
        assert validate_email('@domain.com') is False
        assert validate_email('') is False


class TestDiscountCalculation:
    """Test cases for discount calculation."""

    def test_valid_discount(self):
        """Test discount calculation with valid inputs."""
        assert calculate_discount(100, 10) == 90
        assert calculate_discount(50, 20) == 40
        assert calculate_discount(200, 0) == 200

    def test_full_discount(self):
        """Test 100% discount."""
        assert calculate_discount(100, 100) == 0

    def test_invalid_discount_negative(self):
        """Test negative discount raises error."""
        with pytest.raises(ValueError, match="Discount percent must be between 0 and 100"):
            calculate_discount(100, -10)

    def test_invalid_discount_over_100(self):
        """Test discount over 100% raises error."""
        with pytest.raises(ValueError, match="Discount percent must be between 0 and 100"):
            calculate_discount(100, 150)


class TestCalculatorClass:
    """Test cases for Calculator class."""

    def test_calculator_add(self):
        """Test calculator add method."""
        calc = Calculator()
        result = calc.add(5, 3)
        assert result == 8

    def test_calculator_history(self):
        """Test calculator maintains history."""
        calc = Calculator()
        calc.add(5, 3)
        calc.add(10, 2)

        history = calc.get_history()
        assert len(history) == 2
        assert "5 + 3 = 8" in history
        assert "10 + 2 = 12" in history

    def test_calculator_clear_history(self):
        """Test calculator clear history."""
        calc = Calculator()
        calc.add(5, 3)
        calc.clear_history()

        assert len(calc.get_history()) == 0


# Parametrized tests for more comprehensive coverage
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, -50, 50),
    (0.1, 0.2, 0.30000000000000004)  # Floating point precision
])
def test_add_parametrized(a, b, expected):
    """Parametrized test for add function."""
    assert add(a, b) == expected


@pytest.mark.parametrize("username,password,expected_status", [
    ('user', 'pass', 'success'),
    ('admin', 'admin123', 'success'),
    ('testuser', 'testpass', 'success'),
    ('user', 'wrongpass', 'failure'),
    ('wronguser', 'pass', 'failure'),
    ('', '', 'failure')
])
def test_login_parametrized(username, password, expected_status):
    """Parametrized test for login function."""
    result = login(username, password)
    assert result['status'] == expected_status
