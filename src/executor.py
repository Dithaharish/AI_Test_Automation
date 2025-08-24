import pytest
import os
import json
import subprocess
from typing import Dict, List, Optional
from datetime import datetime
import tempfile
from pathlib import Path


class TestReporter:
    """
    Enhanced test reporting system supporting console, HTML, and JSON outputs.
    Can be extended to integrate with FastAPI backend and React dashboard.
    """

    def __init__(self, test_dir: str = "tests/generated", reports_dir: str = "reports"):
        self.test_dir = test_dir
        self.reports_dir = reports_dir
        self.ensure_directories()

    def ensure_directories(self):
        """Create necessary directories."""
        os.makedirs(self.test_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)

    def run_tests_with_html_report(self, test_files: List[str] = None) -> Dict:
        """
        Run pytest with HTML report generation using pytest-html.

        Installation required: pip install pytest-html
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_report_path = os.path.join(self.reports_dir, f"test_report_{timestamp}.html")

        # Prepare command
        if test_files is None:
            cmd = [
                "python", "-m", "pytest",
                self.test_dir,
                f"--html={html_report_path}",
                "--self-contained-html",  # Single file report
                "-v",
                "--tb=short"
            ]
        else:
            cmd = [
                      "python", "-m", "pytest"
                  ] + test_files + [
                      f"--html={html_report_path}",
                      "--self-contained-html",
                      "-v",
                      "--tb=short"
                  ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            return {
                "timestamp": datetime.now().isoformat(),
                "exit_code": result.returncode,
                "success": result.returncode == 0,
                "html_report_path": html_report_path if os.path.exists(html_report_path) else None,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "report_type": "HTML",
                "message": self._get_status_message(result.returncode)
            }
        except subprocess.TimeoutExpired:
            return {"error": "Test execution timed out", "success": False}
        except Exception as e:
            return {"error": str(e), "success": False}

    def run_tests_with_allure_report(self, test_files: List[str] = None) -> Dict:
        """
        Run pytest with Allure report generation.

        Installation required:
        - pip install allure-pytest
        - Install Allure commandline tool
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        allure_results_dir = os.path.join(self.reports_dir, f"allure-results-{timestamp}")
        allure_report_dir = os.path.join(self.reports_dir, f"allure-report-{timestamp}")

        # Prepare pytest command with allure
        if test_files is None:
            cmd = [
                "python", "-m", "pytest",
                self.test_dir,
                f"--alluredir={allure_results_dir}",
                "--clean-alluredir",
                "-v"
            ]
        else:
            cmd = [
                      "python", "-m", "pytest"
                  ] + test_files + [
                      f"--alluredir={allure_results_dir}",
                      "--clean-alluredir",
                      "-v"
                  ]

        try:
            # Run tests with allure results
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            # Generate allure report
            allure_cmd = ["allure", "generate", allure_results_dir, "-o", allure_report_dir, "--clean"]
            allure_result = subprocess.run(allure_cmd, capture_output=True, text=True)

            return {
                "timestamp": datetime.now().isoformat(),
                "exit_code": result.returncode,
                "success": result.returncode == 0,
                "allure_results_dir": allure_results_dir,
                "allure_report_dir": allure_report_dir if allure_result.returncode == 0 else None,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "allure_generation_success": allure_result.returncode == 0,
                "report_type": "Allure",
                "message": self._get_status_message(result.returncode)
            }
        except subprocess.TimeoutExpired:
            return {"error": "Test execution timed out", "success": False}
        except Exception as e:
            return {"error": str(e), "success": False}

    def run_tests_with_json_report(self, test_files: List[str] = None) -> Dict:
        """
        Run pytest with JSON report generation using pytest-json-report.

        Installation required: pip install pytest-json-report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_report_path = os.path.join(self.reports_dir, f"test_report_{timestamp}.json")

        # Prepare command
        if test_files is None:
            cmd = [
                "python", "-m", "pytest",
                self.test_dir,
                f"--json-report={json_report_path}",
                "--json-report-summary",
                "-v"
            ]
        else:
            cmd = [
                      "python", "-m", "pytest"
                  ] + test_files + [
                      f"--json-report={json_report_path}",
                      "--json-report-summary",
                      "-v"
                  ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            # Load JSON report if it exists
            json_data = None
            if os.path.exists(json_report_path):
                with open(json_report_path, 'r') as f:
                    json_data = json.load(f)

            return {
                "timestamp": datetime.now().isoformat(),
                "exit_code": result.returncode,
                "success": result.returncode == 0,
                "json_report_path": json_report_path if os.path.exists(json_report_path) else None,
                "json_data": json_data,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "report_type": "JSON",
                "message": self._get_status_message(result.returncode)
            }
        except Exception as e:
            return {"error": str(e), "success": False}

    def generate_console_report(self, results: Dict) -> str:
        """Generate formatted console report."""
        report_lines = [
            "🚀 " + "=" * 60,
            "   AI TEST AUTOMATION - EXECUTION REPORT",
            "=" * 64,
            f"⏰ Timestamp: {results.get('timestamp', 'N/A')}",
            f"📊 Report Type: {results.get('report_type', 'Console')}",
            f"✅ Success: {'Yes' if results.get('success') else 'No'}",
            f"🔢 Exit Code: {results.get('exit_code', 'N/A')}",
            ""
        ]

        # Add specific report information
        if results.get('html_report_path'):
            report_lines.append(f"📄 HTML Report: {results['html_report_path']}")

        if results.get('allure_report_dir'):
            report_lines.append(f"📈 Allure Report: {results['allure_report_dir']}/index.html")

        if results.get('json_report_path'):
            report_lines.append(f"📝 JSON Report: {results['json_report_path']}")

        # Add JSON data summary if available
        json_data = results.get('json_data')
        if json_data and 'summary' in json_data:
            summary = json_data['summary']
            report_lines.extend([
                "",
                "📋 TEST SUMMARY:",
                f"   Total: {summary.get('total', 0)}",
                f"   Passed: {summary.get('passed', 0)} ✅",
                f"   Failed: {summary.get('failed', 0)} ❌",
                f"   Skipped: {summary.get('skipped', 0)} ⏭️",
                f"   Duration: {summary.get('duration', 0):.2f}s"
            ])

        # Add message
        if results.get('message'):
            report_lines.extend([
                "",
                f"💬 Status: {results['message']}"
            ])

        report_lines.extend([
            "",
            "=" * 64
        ])

        return "\n".join(report_lines)

    def _get_status_message(self, exit_code: int) -> str:
        """Generate status message based on exit code."""
        if exit_code == 0:
            return "🎉 All tests passed!"
        elif exit_code == 1:
            return "❌ Some tests failed"
        elif exit_code == 5:
            return "⚠️ No tests collected"
        else:
            return f"❓ Unknown exit code: {exit_code}"

    def suggest_improvements(self, results: Dict) -> List[str]:
        """Generate improvement suggestions based on results."""
        suggestions = []

        if results.get('success'):
            suggestions.extend([
                "🎉 Great job! All tests are passing",
                "💡 Consider adding more edge cases",
                "🔍 Review code coverage reports",
                "📈 Monitor test performance trends"
            ])
        else:
            suggestions.extend([
                "🔧 Review failed tests and fix issues",
                "📝 Check test data and assertions",
                "🐛 Look for common patterns in failures",
                "🚀 Consider test parallelization for faster feedback"
            ])

        # Add report-specific suggestions
        if results.get('report_type') == 'HTML':
            suggestions.append("📄 Share HTML report with team members")
        elif results.get('report_type') == 'Allure':
            suggestions.append("📈 Use Allure's advanced features like test history")

        return suggestions


# FastAPI Backend Integration (Future Enhancement)
class TestResultsAPI:
    """
    Future: FastAPI backend to serve test results to React dashboard.
    """

    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = reports_dir

    def get_latest_results(self) -> Dict:
        """Get the most recent test results."""
        # Implementation for serving latest test results
        pass

    def get_test_history(self, limit: int = 10) -> List[Dict]:
        """Get historical test results."""
        # Implementation for test history
        pass

    def get_test_trends(self) -> Dict:
        """Get test execution trends and statistics."""
        # Implementation for trends analysis
        pass


# Example FastAPI routes (for future implementation)
FASTAPI_EXAMPLE = '''
from fastapi import FastAPI, HTTPException
from typing import List, Dict
import json
import os
from pathlib import Path

app = FastAPI(title="AI Test Automation Dashboard")

@app.get("/api/test-results/latest")
async def get_latest_test_results():
    """Get the latest test execution results."""
    reports_dir = Path("reports")
    json_files = list(reports_dir.glob("test_report_*.json"))

    if not json_files:
        raise HTTPException(status_code=404, detail="No test reports found")

    latest_file = max(json_files, key=os.path.getctime)

    with open(latest_file) as f:
        return json.load(f)

@app.get("/api/test-results/history")
async def get_test_history(limit: int = 10):
    """Get test execution history."""
    reports_dir = Path("reports")
    json_files = sorted(
        reports_dir.glob("test_report_*.json"), 
        key=os.path.getctime, 
        reverse=True
    )

    results = []
    for file_path in json_files[:limit]:
        with open(file_path) as f:
            data = json.load(f)
            results.append({
                "timestamp": data.get("created"),
                "success": data.get("summary", {}).get("failed", 0) == 0,
                "total": data.get("summary", {}).get("total", 0),
                "passed": data.get("summary", {}).get("passed", 0),
                "failed": data.get("summary", {}).get("failed", 0)
            })

    return results

@app.get("/api/test-results/trends")
async def get_test_trends():
    """Get test execution trends and statistics."""
    # Implementation for calculating trends
    return {"message": "Trends endpoint - to be implemented"}
'''

# React Dashboard Component Example (Future Enhancement)
REACT_DASHBOARD_EXAMPLE = '''
// TestDashboard.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TestDashboard = () => {
  const [latestResults, setLatestResults] = useState(null);
  const [testHistory, setTestHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLatestResults();
    fetchTestHistory();
  }, []);

  const fetchLatestResults = async () => {
    try {
      const response = await axios.get('/api/test-results/latest');
      setLatestResults(response.data);
    } catch (error) {
      console.error('Error fetching latest results:', error);
    }
  };

  const fetchTestHistory = async () => {
    try {
      const response = await axios.get('/api/test-results/history');
      setTestHistory(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching test history:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading test results...</div>;
  }

  return (
    <div className="dashboard">
      <h1>🚀 AI Test Automation Dashboard</h1>

      {/* Latest Results Card */}
      {latestResults && (
        <div className="results-card">
          <h2>Latest Test Results</h2>
          <div className="summary">
            <div className={`status ${latestResults.summary?.failed === 0 ? 'success' : 'failure'}`}>
              {latestResults.summary?.failed === 0 ? '✅ All Passed' : '❌ Some Failed'}
            </div>
            <div className="stats">
              <span>Total: {latestResults.summary?.total}</span>
              <span>Passed: {latestResults.summary?.passed}</span>
              <span>Failed: {latestResults.summary?.failed}</span>
            </div>
          </div>
        </div>
      )}

      {/* Test History Chart */}
      <div className="history-section">
        <h2>Test History</h2>
        <div className="history-list">
          {testHistory.map((result, index) => (
            <div key={index} className="history-item">
              <div className="timestamp">{new Date(result.timestamp).toLocaleString()}</div>
              <div className={`result ${result.success ? 'success' : 'failure'}`}>
                {result.success ? '✅' : '❌'} {result.passed}/{result.total}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TestDashboard;
'''

# Usage Example
if __name__ == "__main__":
    reporter = TestReporter()

    print("🚀 AI Test Automation Reporter")
    print("=" * 50)

    # Method 1: Console reporting (always available)
    print("1️⃣ Running tests with console reporting...")
    results = {"timestamp": datetime.now().isoformat(), "success": True, "report_type": "Console"}
    console_report = reporter.generate_console_report(results)
    print(console_report)

    # Method 2: HTML reporting (requires pytest-html)
    print("\n2️⃣ Running tests with HTML reporting...")
    try:
        html_results = reporter.run_tests_with_html_report()
        html_report = reporter.generate_console_report(html_results)
        print(html_report)

        if html_results.get('html_report_path'):
            print(f"📄 Open HTML report: {html_results['html_report_path']}")
    except Exception as e:
        print(f"❌ HTML reporting failed: {e}")
        print("💡 Install with: pip install pytest-html")

    # Method 3: JSON reporting (requires pytest-json-report)
    print("\n3️⃣ Running tests with JSON reporting...")
    try:
        json_results = reporter.run_tests_with_json_report()
        json_report = reporter.generate_console_report(json_results)
        print(json_report)

        if json_results.get('json_report_path'):
            print(f"📝 JSON report saved: {json_results['json_report_path']}")
    except Exception as e:
        print(f"❌ JSON reporting failed: {e}")
        print("💡 Install with: pip install pytest-json-report")

    # Method 4: Allure reporting (requires allure-pytest and allure commandline)
    print("\n4️⃣ Running tests with Allure reporting...")
    try:
        allure_results = reporter.run_tests_with_allure_report()
        allure_report = reporter.generate_console_report(allure_results)
        print(allure_report)

        if allure_results.get('allure_report_dir'):
            print(f"📈 Open Allure report: {allure_results['allure_report_dir']}/index.html")
    except Exception as e:
        print(f"❌ Allure reporting failed: {e}")
        print("💡 Install with: pip install allure-pytest")
        print("💡 Install Allure CLI: https://docs.qameta.io/allure/#_installing_a_commandline")

    print("\n🔮 Future Enhancements:")
    print("   📡 FastAPI backend integration")
    print("   ⚛️ React dashboard for real-time monitoring")
    print("   📊 Advanced analytics and trends")
    print("   🔔 Email/Slack notifications")
