#!/usr/bin/env python3
"""
Script to run integration tests for LlamaPackages.

This script sets up the environment for integration testing, runs the tests,
and performs any necessary cleanup.

Usage:
    python run_integration_tests.py [--registry URL] [--debug]
"""

import os
import sys
import argparse
import subprocess
import tempfile
import shutil
import time
from pathlib import Path

# Ensure the current directory is in the path so we can import local modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def setup_test_environment(registry_url=None, debug=False):
    """
    Set up the environment for running integration tests.
    
    Args:
        registry_url: URL of the registry to use for testing
        debug: Flag to enable debug output
    
    Returns:
        dict: Environment variables dictionary
    """
    env = os.environ.copy()
    
    # Set environment variables for tests
    env["LLAMA_RUN_INTEGRATION_TESTS"] = "1"
    
    if registry_url:
        env["LLAMA_TEST_REGISTRY_URL"] = registry_url
    else:
        # Use default test registry if none provided
        env["LLAMA_TEST_REGISTRY_URL"] = "http://localhost:8000"
    
    # Set up a temporary config directory for tests
    env["LLAMA_CONFIG_DIR"] = tempfile.mkdtemp()
    
    # Set debug mode if requested
    if debug:
        env["LLAMA_DEBUG"] = "1"
    
    return env

def cleanup_environment(env):
    """
    Clean up the test environment.
    
    Args:
        env: Environment variables dictionary
    """
    if "LLAMA_CONFIG_DIR" in env and os.path.exists(env["LLAMA_CONFIG_DIR"]):
        shutil.rmtree(env["LLAMA_CONFIG_DIR"])

def check_registry_available(registry_url):
    """
    Check if the registry is available.
    
    Args:
        registry_url: URL of the registry to check
    
    Returns:
        bool: True if the registry is available, False otherwise
    """
    try:
        import requests
        response = requests.get(registry_url, timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def run_tests(env, tests_path=None, verbose=False):
    """
    Run integration tests.
    
    Args:
        env: Environment variables dictionary
        tests_path: Path to the test files
        verbose: Flag to enable verbose output
    
    Returns:
        int: Test exit code
    """
    # Set up the test command
    pytest_args = ["-xvs"] if verbose else ["-v"]
    
    # Add the integration test marker
    pytest_args.append("-m")
    pytest_args.append("integration")
    
    # Add the tests path if specified
    if tests_path:
        pytest_args.append(tests_path)
    else:
        # Default to the integration tests directory
        tests_dir = Path(__file__).parent / "integration"
        pytest_args.append(str(tests_dir))
    
    # Run pytest
    try:
        import pytest
        return pytest.main(pytest_args)
    except ImportError:
        print("pytest is not installed. Please install it with 'pip install pytest'")
        return 1

def start_mock_registry(port=8000):
    """
    Start a mock registry for testing.
    
    Args:
        port: Port to run the mock registry on
    
    Returns:
        subprocess.Popen: Process object for the mock registry
    """
    script_dir = Path(__file__).parent
    mock_registry_path = script_dir / "mock_registry.py"
    
    # Check if mock registry script exists
    if not mock_registry_path.exists():
        print("Mock registry script not found. Creating one...")
        create_mock_registry_script(mock_registry_path)
    
    # Start the mock registry
    cmd = [sys.executable, str(mock_registry_path), "--port", str(port)]
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    
    # Give it a moment to start up
    time.sleep(2)
    
    return process

def create_mock_registry_script(file_path):
    """
    Create a mock registry script for testing.
    
    Args:
        file_path: Path to write the script to
    """
    with open(file_path, "w") as f:
        f.write("""#!/usr/bin/env python3
\"\"\"
Mock registry server for LlamaPackages integration testing.

This provides a simple HTTP server that mimics the behavior of the LlamaPackages registry
for integration testing purposes.
\"\"\"

import os
import sys
import json
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# Sample package data for testing
SAMPLE_PACKAGES = {
    "llamatext": {
        "name": "llamatext",
        "description": "Text processing utilities",
        "author": "LlamaSearch.ai",
        "homepage": "https://llamasearch.ai/packages/llamatext",
        "license": "MIT",
        "latest_version": "1.0.0",
        "versions": ["0.9.0", "1.0.0"]
    },
    "llamamath": {
        "name": "llamamath",
        "description": "Mathematics utilities",
        "author": "LlamaSearch.ai",
        "homepage": "https://llamasearch.ai/packages/llamamath",
        "license": "MIT",
        "latest_version": "0.5.0",
        "versions": ["0.1.0", "0.5.0"]
    },
    "test-package": {
        "name": "test-package",
        "description": "A test package for integration testing",
        "author": "Test Author",
        "homepage": "https://example.com/test-package",
        "license": "MIT",
        "latest_version": "0.1.0",
        "versions": ["0.1.0"]
    },
    "package-a": {
        "name": "package-a",
        "description": "Package A for conflict testing",
        "author": "Test Author",
        "homepage": "https://example.com/package-a",
        "license": "MIT",
        "latest_version": "1.0.0",
        "versions": ["1.0.0"]
    },
    "package-b": {
        "name": "package-b",
        "description": "Package B for conflict testing",
        "author": "Test Author",
        "homepage": "https://example.com/package-b",
        "license": "MIT",
        "latest_version": "1.0.0",
        "versions": ["1.0.0"]
    }
}

# Authenticated users
USERS = {
    "test_user": {
        "password": "test_password",
        "token": "test-token-123"
    }
}

class MockRegistryHandler(BaseHTTPRequestHandler):
    \"\"\"HTTP request handler for mock registry.\"\"\"
    
    def do_GET(self):
        \"\"\"Handle GET requests.\"\"\"
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)
        
        # API endpoints
        if path == "/api/v1/packages":
            self.handle_package_list(query)
        elif path.startswith("/api/v1/packages/"):
            package_name = path.split("/")[-1]
            self.handle_package_get(package_name)
        elif path == "/api/v1/auth/validate":
            self.handle_validate_token()
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("Mock LlamaPackages Registry".encode())
    
    def do_POST(self):
        \"\"\"Handle POST requests.\"\"\"
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        
        try:
            data = json.loads(post_data) if post_data else {}
        except json.JSONDecodeError:
            data = {}
        
        # API endpoints
        if self.path == "/api/v1/auth/login":
            self.handle_login(data)
        elif self.path == "/api/v1/packages/publish":
            self.handle_publish(data)
        elif self.path == "/api/v1/packages/install":
            self.handle_install(data)
        elif self.path == "/api/v1/packages/uninstall":
            self.handle_uninstall(data)
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())
    
    def handle_package_list(self, query):
        \"\"\"Handle GET /api/v1/packages endpoint.\"\"\"
        search_query = query.get("q", [""])[0].lower()
        
        # Filter packages by search query
        results = []
        for pkg_name, pkg_data in SAMPLE_PACKAGES.items():
            if search_query in pkg_name.lower() or search_query in pkg_data["description"].lower():
                results.append(pkg_data)
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"packages": results}).encode())
    
    def handle_package_get(self, package_name):
        \"\"\"Handle GET /api/v1/packages/{name} endpoint.\"\"\"
        if package_name in SAMPLE_PACKAGES:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "package": SAMPLE_PACKAGES[package_name],
                "versions": [
                    {"version": v, "release_date": "2023-01-01", "description": "Version " + v}
                    for v in SAMPLE_PACKAGES[package_name]["versions"]
                ]
            }).encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Package {package_name} not found"}).encode())
    
    def handle_login(self, data):
        \"\"\"Handle POST /api/v1/auth/login endpoint.\"\"\"
        username = data.get("username", "")
        password = data.get("password", "")
        
        if username in USERS and USERS[username]["password"] == password:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "token": USERS[username]["token"],
                "user": {"username": username, "email": f"{username}@example.com"}
            }).encode())
        else:
            self.send_response(401)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid credentials"}).encode())
    
    def handle_validate_token(self):
        \"\"\"Handle GET /api/v1/auth/validate endpoint.\"\"\"
        token = self.headers.get("Authorization", "").replace("Bearer ", "")
        
        valid = False
        for user_data in USERS.values():
            if user_data["token"] == token:
                valid = True
                break
        
        if valid:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"valid": True}).encode())
        else:
            self.send_response(401)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"valid": False, "error": "Invalid token"}).encode())
    
    def handle_publish(self, data):
        \"\"\"Handle POST /api/v1/packages/publish endpoint.\"\"\"
        token = self.headers.get("Authorization", "").replace("Bearer ", "")
        
        # Check token validity
        valid = False
        for user_data in USERS.values():
            if user_data["token"] == token:
                valid = True
                break
        
        if not valid:
            self.send_response(401)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Unauthorized"}).encode())
            return
        
        # Handle publish
        package_name = data.get("name", "")
        package_version = data.get("version", "")
        
        if not package_name or not package_version:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing name or version"}).encode())
            return
        
        # Add to sample packages if not exists
        if package_name not in SAMPLE_PACKAGES:
            SAMPLE_PACKAGES[package_name] = {
                "name": package_name,
                "description": data.get("description", ""),
                "author": data.get("author", ""),
                "homepage": data.get("homepage", ""),
                "license": data.get("license", ""),
                "latest_version": package_version,
                "versions": [package_version]
            }
        else:
            # Update existing package
            pkg = SAMPLE_PACKAGES[package_name]
            if package_version not in pkg["versions"]:
                pkg["versions"].append(package_version)
            pkg["latest_version"] = package_version
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "name": package_name,
            "version": package_version,
            "success": True
        }).encode())
    
    def handle_install(self, data):
        \"\"\"Handle POST /api/v1/packages/install endpoint.\"\"\"
        token = self.headers.get("Authorization", "").replace("Bearer ", "")
        
        # Check token validity
        valid = False
        for user_data in USERS.values():
            if user_data["token"] == token:
                valid = True
                break
        
        if not valid:
            self.send_response(401)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Unauthorized"}).encode())
            return
        
        # Handle install
        package_name = data.get("name", "")
        package_version = data.get("version", "")
        
        if not package_name:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing package name"}).encode())
            return
        
        if package_name not in SAMPLE_PACKAGES:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Package {package_name} not found"}).encode())
            return
        
        # If version not specified, use latest
        if not package_version:
            package_version = SAMPLE_PACKAGES[package_name]["latest_version"]
        elif package_version not in SAMPLE_PACKAGES[package_name]["versions"]:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(
                {"error": f"Version {package_version} not found for package {package_name}"}
            ).encode())
            return
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "name": package_name,
            "version": package_version,
            "success": True
        }).encode())
    
    def handle_uninstall(self, data):
        \"\"\"Handle POST /api/v1/packages/uninstall endpoint.\"\"\"
        token = self.headers.get("Authorization", "").replace("Bearer ", "")
        
        # Check token validity
        valid = False
        for user_data in USERS.values():
            if user_data["token"] == token:
                valid = True
                break
        
        if not valid:
            self.send_response(401)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Unauthorized"}).encode())
            return
        
        # Handle uninstall
        package_name = data.get("name", "")
        
        if not package_name:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing package name"}).encode())
            return
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "name": package_name,
            "success": True
        }).encode())

def run_server(port=8000):
    \"\"\"Run the mock registry server.\"\"\"
    server_address = ("", port)
    httpd = HTTPServer(server_address, MockRegistryHandler)
    print(f"Starting mock registry on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Stopping server...")
        httpd.server_close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a mock LlamaPackages registry server")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    args = parser.parse_args()
    
    run_server(args.port)
""")

def main():
    """Main function to run the integration tests."""
    parser = argparse.ArgumentParser(description="Run LlamaPackages integration tests")
    parser.add_argument("--registry", help="URL of the registry to use for testing")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    parser.add_argument("--no-mock", action="store_true", help="Don't use mock registry")
    parser.add_argument("--test-path", help="Path to specific test file or directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    # Set up the test environment
    env = setup_test_environment(args.registry, args.debug)
    mock_registry_process = None
    
    try:
        # If registry URL not specified and not using no-mock flag, start a mock registry
        if not args.registry and not args.no_mock:
            mock_registry_process = start_mock_registry()
            env["LLAMA_TEST_REGISTRY_URL"] = "http://localhost:8000"
            
            # Check if mock registry is available
            if not check_registry_available(env["LLAMA_TEST_REGISTRY_URL"]):
                print("Failed to start mock registry. Exiting.")
                return 1
        
        # Run the tests
        exit_code = run_tests(env, args.test_path, args.verbose)
        return exit_code
    
    finally:
        # Clean up
        cleanup_environment(env)
        
        # Stop mock registry if started
        if mock_registry_process:
            print("Stopping mock registry...")
            mock_registry_process.terminate()
            mock_registry_process.wait()

if __name__ == "__main__":
    sys.exit(main()) 