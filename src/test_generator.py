import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class Generator:
    """
    Generate pytest test cases from structured JSON requirements.
    Later can be enhanced with LLM integration for more sophisticated test generation.
    """

    def __init__(self, output_dir: str = "tests/generated"):
        self.output_dir = output_dir
        self.ensure_output_directory()

    def ensure_output_directory(self):
        """Create the output directory if it doesn't exist."""
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_test_from_requirement(self, requirement: Dict) -> str:
        """
        Generate a pytest test case from a single structured requirement.

        Args:
            requirement (Dict): Structured requirement JSON

        Returns:
            str: Generated pytest test code
        """
        feature = requirement.get('feature', 'unknown')
        conditions = requirement.get('conditions', [])
        expected = requirement.get('expected', 'success')
        original_text = requirement.get('original_text', '')

        # Generate test function name
        test_name = self._generate_test_name(feature, conditions)

        # Generate test code
        test_code = self._generate_test_code(
            test_name, feature, conditions, expected, original_text
        )

        return test_code

    def _generate_test_name(self, feature: str, conditions: List[str]) -> str:
        """Generate a descriptive test function name."""
        # Clean feature name
        clean_feature = feature.replace(' ', '_').replace('-', '_')

        # Add condition indicators
        condition_suffix = ""
        if conditions and conditions != ["no specific conditions"]:
            # Take first condition and clean it
            first_condition = conditions[0].replace(' ', '_').replace('-', '_')
            # Remove common words and keep meaningful parts
            meaningful_words = [word for word in first_condition.split('_')
                                if word not in ['and', 'or', 'with', 'using']]
            if meaningful_words:
                condition_suffix = f"_{'_'.join(meaningful_words[:2])}"

        return f"test_{clean_feature}{condition_suffix}"

    def _generate_test_code(self, test_name: str, feature: str, conditions: List[str],
                            expected: str, original_text: str) -> str:
        """Generate the actual pytest test code."""

        # Create test template based on feature type
        if feature == 'login':
            return self._generate_login_test(test_name, conditions, expected, original_text)
        elif feature == 'register' or feature == 'registration':
            return self._generate_register_test(test_name, conditions, expected, original_text)
        elif feature == 'validate' or feature == 'validation':
            return self._generate_validation_test(test_name, conditions, expected, original_text)
        elif feature == 'search':
            return self._generate_search_test(test_name, conditions, expected, original_text)
        else:
            return self._generate_generic_test(test_name, feature, conditions, expected, original_text)

    def _generate_login_test(self, test_name: str, conditions: List[str],
                             expected: str, original_text: str) -> str:
        """Generate login-specific test code."""
        return f'''def {test_name}():
    """
    Test case generated from requirement:
    {original_text}

    Feature: login
    Conditions: {', '.join(conditions)}
    Expected: {expected}
    """
    # Arrange
    username = "valid_user"
    password = "valid_password"

    # Act
    result = login_system(username, password)

    # Assert
    assert result is not None, "Login should return a result"
    assert result.get('status') == 'success', "Login should be successful"
    assert 'user_id' in result, "Login result should contain user_id"

def login_system(username: str, password: str) -> dict:
    """Mock login function - replace with actual implementation"""
    if username and password:
        return {{"status": "success", "user_id": "12345"}}
    return {{"status": "failure", "error": "Invalid credentials"}}
'''

    def _generate_register_test(self, test_name: str, conditions: List[str],
                                expected: str, original_text: str) -> str:
        """Generate registration-specific test code."""
        return f'''def {test_name}():
    """
    Test case generated from requirement:
    {original_text}

    Feature: register/registration
    Conditions: {', '.join(conditions)}
    Expected: {expected}
    """
    # Arrange
    user_data = {{
        "username": "new_user",
        "email": "user@example.com",
        "password": "secure_password"
    }}

    # Act
    result = register_user(user_data)

    # Assert
    assert result is not None, "Registration should return a result"
    assert result.get('status') == 'success', "Registration should be successful"
    assert 'user_id' in result, "Registration result should contain user_id"

def register_user(user_data: dict) -> dict:
    """Mock registration function - replace with actual implementation"""
    if user_data.get('email') and user_data.get('password'):
        return {{"status": "success", "user_id": "67890"}}
    return {{"status": "failure", "error": "Invalid user data"}}
'''

    def _generate_validation_test(self, test_name: str, conditions: List[str],
                                  expected: str, original_text: str) -> str:
        """Generate validation-specific test code."""
        return f'''def {test_name}():
    """
    Test case generated from requirement:
    {original_text}

    Feature: validate/validation
    Conditions: {', '.join(conditions)}
    Expected: {expected}
    """
    # Arrange
    test_data = "sample_input"

    # Act
    result = validate_input(test_data)

    # Assert
    assert result is not None, "Validation should return a result"
    if "valid" in "{expected}":
        assert result.get('is_valid') is True, "Input should be valid"
    else:
        assert result.get('is_valid') is False, "Input should be invalid"

def validate_input(data: str) -> dict:
    """Mock validation function - replace with actual implementation"""
    if data and len(data) > 0:
        return {{"is_valid": True, "message": "Valid input"}}
    return {{"is_valid": False, "message": "Invalid input"}}
'''

    def _generate_search_test(self, test_name: str, conditions: List[str],
                              expected: str, original_text: str) -> str:
        """Generate search-specific test code."""
        return f'''def {test_name}():
    """
    Test case generated from requirement:
    {original_text}

    Feature: search
    Conditions: {', '.join(conditions)}
    Expected: {expected}
    """
    # Arrange
    search_query = "test query"

    # Act
    results = search_function(search_query)

    # Assert
    assert results is not None, "Search should return results"
    assert isinstance(results, list), "Search results should be a list"
    if "relevant" in "{expected}":
        assert len(results) > 0, "Search should return relevant results"

def search_function(query: str) -> list:
    """Mock search function - replace with actual implementation"""
    if query:
        return [{{"title": "Result 1", "relevance": 0.9}}]
    return []
'''

    def _generate_generic_test(self, test_name: str, feature: str, conditions: List[str],
                               expected: str, original_text: str) -> str:
        """Generate generic test code for unknown features."""
        return f'''def {test_name}():
    """
    Test case generated from requirement:
    {original_text}

    Feature: {feature}
    Conditions: {', '.join(conditions)}
    Expected: {expected}
    """
    # Arrange
    # TODO: Set up test data based on your specific feature
    test_input = "sample_input"

    # Act
    # TODO: Replace with actual function call for '{feature}'
    result = {feature}_function(test_input)

    # Assert
    assert result is not None, f"{feature} should return a result"
    # TODO: Add specific assertions based on expected outcome: {expected}

def {feature}_function(input_data):
    """Mock function for {feature} - replace with actual implementation"""
    # TODO: Implement actual {feature} logic
    return {{"status": "success", "data": input_data}}
'''

    def generate_test_file(self, requirements: List[Dict], filename: str = None) -> str:
        """
        Generate a complete pytest file from multiple requirements.

        Args:
            requirements (List[Dict]): List of structured requirements
            filename (str): Optional filename for the test file

        Returns:
            str: Generated test file content
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_generated_{timestamp}.py"

        # Generate file header
        header = f'''"""
Generated Test File
Created on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Number of test cases: {len(requirements)}

This file was automatically generated from structured requirements.
Modify as needed for your specific implementation.
"""

import pytest
from typing import Dict, List, Optional

'''

        # Generate all test cases
        test_cases = []
        for requirement in requirements:
            test_code = self.generate_test_from_requirement(requirement)
            test_cases.append(test_code)

        # Combine everything
        full_content = header + "\n\n".join(test_cases)

        # Save to file
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)

        return full_content

    def generate_multiple_files(self, requirements: List[Dict]) -> List[str]:
        """
        Generate separate test files for different features.

        Args:
            requirements (List[Dict]): List of structured requirements

        Returns:
            List[str]: List of generated file paths
        """
        feature_groups = {}

        # Group requirements by feature
        for req in requirements:
            feature = req.get('feature', 'unknown')
            if feature not in feature_groups:
                feature_groups[feature] = []
            feature_groups[feature].append(req)

        generated_files = []

        # Generate separate files for each feature
        for feature, reqs in feature_groups.items():
            filename = f"test_{feature}.py"
            self.generate_test_file(reqs, filename)
            filepath = os.path.join(self.output_dir, filename)
            generated_files.append(filepath)

        return generated_files


# Example usage and testing
if __name__ == "__main__":
    # Sample requirements (from requirements_parser.py output)
    sample_requirements = [
        {
            "feature": "login",
            "conditions": ["username and password"],
            "expected": "successful login",
            "original_text": "The system should allow login with username and password."
        },
        {
            "feature": "register",
            "conditions": ["valid email address"],
            "expected": "successful registration",
            "original_text": "Users must be able to register using valid email address."
        },
        {
            "feature": "validate",
            "conditions": ["user input"],
            "expected": "display error messages for invalid data",
            "original_text": "The application should validate user input and display error messages for invalid data."
        }
    ]

    # Initialize generator
    generator = TestGenerator()

    # Generate individual test
    print("Individual Test Generation:")
    print("=" * 50)
    single_test = generator.generate_test_from_requirement(sample_requirements[0])
    print(single_test)

    print("\n" + "=" * 50)
    print("Complete Test File Generation:")
    print("=" * 50)

    # Generate complete test file
    test_file_content = generator.generate_test_file(sample_requirements, "test_example.py")
    print(f"Generated test file: tests/generated/test_example.py")

    # Generate separate files by feature
    generated_files = generator.generate_multiple_files(sample_requirements)
    print(f"Generated feature-specific files: {generated_files}")
