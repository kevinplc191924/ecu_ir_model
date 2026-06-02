import subprocess
import sys
from pathlib import Path

CLI_PATH = Path(__file__).resolve().parent.parent / "src" / "cli.py"

def test_cli_runs_with_args():
    """Test that the CLI runs with valid arguments and produces output."""
    result = subprocess.run(
        [sys.executable, str(CLI_PATH), "20000", "225.90"],
        capture_output=True,
        text=True
    )

    # The process should exit successfully
    assert result.returncode == 0  # Standard way to test successful executions
    # Output should contain expected keys
    assert "Impuesto real" in result.stdout or "Valores" in result.stdout

def test_cli_invalid_args():
    """Test that the CLI handles invalid arguments."""
    result = subprocess.run(
        [sys.executable, str(CLI_PATH), "abc", "xyz"],
        capture_output=True,
        text=True
    )

    # Should not crash, but exit with non-zero or error message
    assert result.returncode != 0 or "Invalid inputs" in result.stdout
