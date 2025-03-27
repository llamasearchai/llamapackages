#!/usr/bin/env python3
"""
Integration tests for LlamaPackages CLI functionality.

These tests verify the command-line interface functionality
by capturing the output of CLI commands and validating results.
"""

import os
import sys
import subprocess
import tempfile
import shutil
import pytest
from pathlib import Path

# Add the parent directories to sys.path to make the llamapackage module importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

class TestCLI:
    """Integration tests for CLI functionality."""
    
    @pytest.fixture
    def cli_env(self):
        """Set up environment variables for CLI testing."""
        # Create a copy of the current environment variables
        env = os.environ.copy()
        
        # Add test-specific environment variables
        env["LLAMA_TEST_MODE"] = "1"
        env["LLAMA_CONFIG_DIR"] = tempfile.mkdtemp()
        env["LLAMA_TEST_REGISTRY_URL"] = os.environ.get("LLAMA_TEST_REGISTRY_URL", "http://localhost:8000")
        env["LLAMA_TEST_AUTH_TOKEN"] = os.environ.get("LLAMA_TEST_AUTH_TOKEN", "test-token")
        
        yield env
        
        # Clean up
        if os.path.exists(env["LLAMA_CONFIG_DIR"]):
            shutil.rmtree(env["LLAMA_CONFIG_DIR"])
    
    @pytest.fixture
    def cli_command(self):
        """Return the base CLI command."""
        # Determine where the CLI script is located
        repo_root = Path(__file__).resolve().parents[3]
        
        # Check if we're running from the installed package or from the source repo
        if (repo_root / "src" / "llamapackage" / "__main__.py").exists():
            # Running from source
            return [sys.executable, str(repo_root / "src" / "llamapackage" / "__main__.py")]
        elif shutil.which("llamapackage"):
            # Running from installed package
            return ["llamapackage"]
        else:
            # Fallback to calling the module
            return [sys.executable, "-m", "llamapackage"]
    
    def run_cli(self, cli_command, args, env=None, input_text=None):
        """Run a CLI command and return the output."""
        cmd = cli_command + args
        
        # Start the process
        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE if input_text else None,
            universal_newlines=True
        )
        
        # Send input if provided
        stdout, stderr = process.communicate(input=input_text)
        
        return {
            "stdout": stdout,
            "stderr": stderr,
            "returncode": process.returncode
        }
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_cli_version(self, cli_command, cli_env):
        """Test the version command."""
        result = self.run_cli(cli_command, ["--version"], env=cli_env)
        
        # Check that the command executed successfully
        assert result["returncode"] == 0, f"Command failed: {result['stderr']}"
        
        # Check that the output contains a version string
        assert "llamapackage" in result["stdout"].lower()
        assert any(char.isdigit() for char in result["stdout"]), "No version number found in output"
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_cli_help(self, cli_command, cli_env):
        """Test the help command."""
        result = self.run_cli(cli_command, ["--help"], env=cli_env)
        
        # Check that the command executed successfully
        assert result["returncode"] == 0, f"Command failed: {result['stderr']}"
        
        # Check that the output contains common help text
        assert "usage" in result["stdout"].lower()
        assert "commands" in result["stdout"].lower()
        
        # Check for expected commands
        expected_commands = ["install", "search", "list", "publish", "login"]
        for cmd in expected_commands:
            assert cmd in result["stdout"], f"Command '{cmd}' not found in help output"
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_cli_search(self, cli_command, cli_env):
        """Test the search command."""
        # Test with a search term that should return results
        search_term = "llama"
        result = self.run_cli(cli_command, ["search", search_term], env=cli_env)
        
        # Check that the command executed successfully
        assert result["returncode"] == 0, f"Command failed: {result['stderr']}"
        
        # Check that the output contains search results
        # This is a minimal check - the actual content will depend on the registry
        assert search_term in result["stdout"].lower(), "Search term not found in results"
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_cli_list(self, cli_command, cli_env):
        """Test the list command."""
        # First, ensure we're authenticated
        self.run_cli(cli_command, ["login"], env=cli_env, input_text="test_user\ntest_password\n")
        
        # Run the list command
        result = self.run_cli(cli_command, ["list"], env=cli_env)
        
        # Check that the command executed successfully
        assert result["returncode"] == 0, f"Command failed: {result['stderr']}"
        
        # Check the output format - should at least contain a header
        assert "installed packages" in result["stdout"].lower() or "no packages installed" in result["stdout"].lower()
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_cli_login_logout(self, cli_command, cli_env):
        """Test the login and logout commands."""
        # Test login
        login_result = self.run_cli(
            cli_command, 
            ["login"], 
            env=cli_env, 
            input_text="test_user\ntest_password\n"
        )
        
        # Check that the login command executed successfully
        assert login_result["returncode"] == 0, f"Login command failed: {login_result['stderr']}"
        assert "login successful" in login_result["stdout"].lower() or "authenticated" in login_result["stdout"].lower()
        
        # Test logout
        logout_result = self.run_cli(cli_command, ["logout"], env=cli_env)
        
        # Check that the logout command executed successfully
        assert logout_result["returncode"] == 0, f"Logout command failed: {logout_result['stderr']}"
        assert "logged out" in logout_result["stdout"].lower()
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_cli_install_uninstall(self, cli_command, cli_env):
        """Test the install and uninstall commands."""
        # First, ensure we're authenticated
        self.run_cli(cli_command, ["login"], env=cli_env, input_text="test_user\ntest_password\n")
        
        # Choose a package that's likely to exist in the test registry
        package_name = "llamatext"
        
        # Install the package
        install_result = self.run_cli(cli_command, ["install", package_name], env=cli_env)
        
        # Check if installation was successful or if the package doesn't exist
        if "not found" in install_result["stderr"].lower():
            pytest.skip(f"Package {package_name} not found in test registry")
        
        # Verify installation was successful
        assert install_result["returncode"] == 0, f"Install command failed: {install_result['stderr']}"
        assert f"installed {package_name}" in install_result["stdout"].lower()
        
        # Verify the package appears in the list
        list_result = self.run_cli(cli_command, ["list"], env=cli_env)
        assert package_name in list_result["stdout"].lower(), f"Installed package {package_name} not found in list output"
        
        # Uninstall the package
        uninstall_result = self.run_cli(cli_command, ["uninstall", package_name], env=cli_env)
        
        # Verify uninstallation was successful
        assert uninstall_result["returncode"] == 0, f"Uninstall command failed: {uninstall_result['stderr']}"
        assert f"uninstalled {package_name}" in uninstall_result["stdout"].lower()
        
        # Verify the package no longer appears in the list
        list_result = self.run_cli(cli_command, ["list"], env=cli_env)
        assert package_name not in list_result["stdout"].lower() or "not installed" in list_result["stdout"].lower()
    
    @pytest.mark.integration
    @pytest.mark.skipif(not os.environ.get("LLAMA_RUN_INTEGRATION_TESTS"),
                       reason="Integration tests are disabled")
    def test_cli_config(self, cli_command, cli_env):
        """Test the config command."""
        # Test getting a config value
        get_result = self.run_cli(cli_command, ["config", "get", "registry_url"], env=cli_env)
        
        # Check that the command executed successfully
        assert get_result["returncode"] == 0, f"Config get command failed: {get_result['stderr']}"
        
        # Test setting a config value
        set_result = self.run_cli(
            cli_command, 
            ["config", "set", "registry_url", "http://test-registry.example.com"], 
            env=cli_env
        )
        
        # Check that the command executed successfully
        assert set_result["returncode"] == 0, f"Config set command failed: {set_result['stderr']}"
        
        # Verify the config value was set
        verify_result = self.run_cli(cli_command, ["config", "get", "registry_url"], env=cli_env)
        assert "test-registry.example.com" in verify_result["stdout"], "Config value not set correctly"

if __name__ == "__main__":
    # Enable running the tests directly
    pytest.main(["-xvs", __file__]) 