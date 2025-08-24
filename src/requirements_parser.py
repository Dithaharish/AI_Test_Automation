import json
import re
from typing import Dict, List, Optional


class RequirementsParser:
    """
    Simple NLP-based requirement parser that converts plain text requirements
    into structured JSON format for test case generation.
    """

    def __init__(self):
        # Keywords for identifying different requirement components
        self.action_keywords = ['login', 'register', 'validate', 'authenticate', 'create', 'delete', 'update', 'view',
                                'display', 'search']
        self.condition_keywords = ['with', 'using', 'when', 'if', 'valid', 'invalid', 'correct', 'incorrect']
        self.expectation_keywords = ['should', 'must', 'will', 'expected', 'successful', 'failure']

    def parse_requirement(self, requirement_text: str) -> Dict:
        """
        Parse a plain text requirement into structured JSON format.

        Args:
            requirement_text (str): Plain text requirement

        Returns:
            Dict: Structured requirement in JSON format
        """
        # Clean and normalize the input text
        text = requirement_text.lower().strip()

        # Extract feature/action
        feature = self._extract_feature(text)

        # Extract conditions
        conditions = self._extract_conditions(text)

        # Extract expected outcome
        expected = self._extract_expected_outcome(text)

        # Create structured output
        parsed_requirement = {
            "feature": feature,
            "conditions": conditions,
            "expected": expected,
            "original_text": requirement_text
        }

        return parsed_requirement

    def _extract_feature(self, text: str) -> str:
        """Extract the main feature/action from the requirement text."""
        # Look for common action keywords
        for keyword in self.action_keywords:
            if keyword in text:
                return keyword

        # If no keyword found, try to extract from "should" patterns
        should_match = re.search(r'should\s+(\w+)', text)
        if should_match:
            return should_match.group(1)

        # Default fallback
        return "unknown_feature"

    def _extract_conditions(self, text: str) -> List[str]:
        """Extract conditions from the requirement text."""
        conditions = []

        # Look for "with" patterns
        with_match = re.findall(r'with\s+([^.]+?)(?:\s+and|\s*\.|\s*$)', text)
        for match in with_match:
            conditions.append(match.strip())

        # Look for "using" patterns
        using_match = re.findall(r'using\s+([^.]+?)(?:\s+and|\s*\.|\s*$)', text)
        for match in using_match:
            conditions.append(match.strip())

        # Look for "valid/invalid" patterns
        valid_match = re.findall(r'(valid\s+\w+)', text)
        conditions.extend(valid_match)

        invalid_match = re.findall(r'(invalid\s+\w+)', text)
        conditions.extend(invalid_match)

        return conditions if conditions else ["no specific conditions"]

    def _extract_expected_outcome(self, text: str) -> str:
        """Extract the expected outcome from the requirement text."""
        # Look for explicit expectations
        if 'successful' in text:
            feature = self._extract_feature(text)
            return f"successful {feature}"

        if 'failure' in text or 'error' in text:
            return "failure or error message"

        # Look for "should" outcomes
        should_match = re.search(r'should\s+(.+?)(?:\s*\.|\s*$)', text)
        if should_match:
            return should_match.group(1).strip()

        # Default expectation
        return "system responds appropriately"

    def parse_multiple_requirements(self, requirements_list: List[str]) -> List[Dict]:
        """
        Parse multiple requirements at once.

        Args:
            requirements_list (List[str]): List of requirement texts

        Returns:
            List[Dict]: List of parsed requirements
        """
        return [self.parse_requirement(req) for req in requirements_list]

    def save_parsed_requirements(self, parsed_requirements: List[Dict], filename: str) -> None:
        """
        Save parsed requirements to a JSON file.

        Args:
            parsed_requirements (List[Dict]): Parsed requirements
            filename (str): Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(parsed_requirements, f, indent=4, ensure_ascii=False)

    def load_requirements_from_file(self, filename: str) -> List[str]:
        """
        Load requirements from a text file (one requirement per line).

        Args:
            filename (str): Input filename

        Returns:
            List[str]: List of requirement texts
        """
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]


# Example usage and testing
if __name__ == "__main__":
    parser = RequirementsParser()

    # Test with the example requirement
    test_requirement = "The system should allow login with username and password."
    result = parser.parse_requirement(test_requirement)

    print("Parsed Requirement:")
    print(json.dumps(result, indent=2))

    # Test with multiple requirements
    test_requirements = [
        "The system should allow login with username and password.",
        "Users must be able to register using valid email address.",
        "The application should validate user input and display error messages for invalid data.",
        "Search functionality should return relevant results when user enters keywords."
    ]

    print("\n" + "=" * 50)
    print("Multiple Requirements Parsing:")

    parsed_results = parser.parse_multiple_requirements(test_requirements)
    for i, result in enumerate(parsed_results, 1):
        print(f"\nRequirement {i}:")
        print(json.dumps(result, indent=2))
