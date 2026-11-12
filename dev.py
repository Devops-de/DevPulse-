#!/usr/bin/env python3
"""
DevPulse Developer Runner CLI.

A unified runner to set up, develop, test, lint, and run the DevPulse full-stack project.
Usage:
    python dev.py setup     - Install backend and frontend dependencies
    python dev.py backend   - Run FastAPI server with auto-reload (port 8000)
    python dev.py frontend  - Run Vite React frontend dev server (port 5173)
    python dev.py dev       - Run both backend & frontend concurrently
    python dev.py test      - Run backend unit tests
    python dev.py lint      - Run backend linter (ruff) & frontend typecheck (tsc)
    python dev.py check     - Check environment prerequisites
"""

import argparse
import contextlib
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Ensure UTF-8 output encoding across Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    with contextlib.suppress(Exception):
        sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"
IS_WINDOWS = sys.platform.startswith("win")

if IS_WINDOWS:
    VENV_PYTHON = ROOT_DIR / ".venv" / "Scripts" / "python.exe"
    NPM_CMD = "npm.cmd" if shutil.which("npm.cmd") else "npm"
else:
    VENV_PYTHON = ROOT_DIR / ".venv" / "bin" / "python"
    NPM_CMD = "npm"


def get_active_python() -> str:
    """Returns path to the venv python if present, else fallback to current python."""
    if VENV_PYTHON.exists():
        return str(VENV_PYTHON)
    return sys.executable


def cmd_check(_args: argparse.Namespace) -> int:
    """Checks system prerequisites."""
    print("==========================================")
    print(" [*] DevPulse Environment Diagnostic Check ")
    print("==========================================")
    print(f"OS: {sys.platform}")
    print(f"System Python: {sys.version.split()[0]} ({sys.executable})")

    node_path = shutil.which("node")
    print(f"Node.js: {'Installed (' + node_path + ')' if node_path else 'Not found'}")

    npm_path = shutil.which(NPM_CMD)
    print(f"NPM: {'Installed (' + npm_path + ')' if npm_path else 'Not found'}")

    venv_ok = VENV_PYTHON.exists()
    venv_status = "Ready" if venv_ok else "Not created (run: python dev.py setup)"
    print(f"Virtualenv (.venv): {venv_status}")
    print("==========================================")
    return 0


def cmd_setup(_args: argparse.Namespace) -> int:
    """Sets up Python virtual environment and installs dependencies."""
    print("\n[*] Setting up DevPulse...")

    # 1. Create Virtualenv if needed
    if not (ROOT_DIR / ".venv").exists():
        print("[+] Creating virtual environment in .venv ...")
        res = subprocess.call([sys.executable, "-m", "venv", str(ROOT_DIR / ".venv")])
        if res != 0:
            print("[x] Failed to create virtual environment.")
            return res
    else:
        print("[v] Virtual environment already exists.")

    py_bin = get_active_python()

    # 2. Upgrade pip and install backend dependencies
    print("\n[+] Installing backend dependencies from backend/requirements.txt ...")
    subprocess.call([py_bin, "-m", "pip", "install", "--upgrade", "pip"])

    reqs_file = BACKEND_DIR / "requirements.txt"
    backend_res = subprocess.call([py_bin, "-m", "pip", "install", "-r", str(reqs_file)])
    if backend_res != 0:
        print("[!] Backend dependency install finished with warnings or errors.")
        return backend_res
    print("[v] Backend dependencies installed.")

    # 3. Install frontend dependencies if npm is available
    if shutil.which(NPM_CMD):
        print("\n[+] Installing frontend dependencies in frontend/ ...")
        frontend_res = subprocess.call([NPM_CMD, "install"], cwd=FRONTEND_DIR)
        if frontend_res != 0:
            print("[!] Frontend install exited with code", frontend_res)
            return frontend_res
        print("[v] Frontend dependencies installed.")
    else:
        print("\n[!] Node/NPM not found. You can still run the FastAPI backend!")

    print("\n[v] Setup complete! To start development:")
    print("   python dev.py dev       (runs backend + frontend)")
    print("   python dev.py backend   (runs backend only at http://localhost:8000)")
    return 0


def cmd_backend(args: argparse.Namespace) -> int:
    """Runs FastAPI backend with uvicorn."""
    py_bin = get_active_python()
    cmd = [
        py_bin,
        "-m",
        "uvicorn",
        "app.main:app",
        "--reload",
        "--host",
        args.host,
        "--port",
        str(args.port),
    ]
    print(f"[*] Starting FastAPI backend at http://{args.host}:{args.port} ...")
    print(f"[*] Swagger Documentation: http://{args.host}:{args.port}/docs")
    return subprocess.call(cmd, cwd=BACKEND_DIR)


def cmd_frontend(_args: argparse.Namespace) -> int:
    """Runs Vite dev server."""
    if not shutil.which(NPM_CMD):
        print("[x] npm not found in system PATH. Please install Node.js.")
        return 1
    print("[*] Starting Vite frontend server at http://localhost:5173 ...")
    return subprocess.call([NPM_CMD, "run", "dev"], cwd=FRONTEND_DIR)


def cmd_dev(args: argparse.Namespace) -> int:
    """Runs both backend and frontend concurrently."""
    py_bin = get_active_python()
    processes: list[subprocess.Popen[bytes]] = []

    print("[*] Booting DevPulse Full-Stack Development Environment...")

    try:
        # Launch backend
        b_cmd = [
            py_bin,
            "-m",
            "uvicorn",
            "app.main:app",
            "--reload",
            "--host",
            args.host,
            "--port",
            str(args.port),
        ]
        print(
            f"[+] Starting Backend on http://{args.host}:{args.port} "
            f"(Docs: http://{args.host}:{args.port}/docs)"
        )
        p_back = subprocess.Popen(b_cmd, cwd=BACKEND_DIR)
        processes.append(p_back)

        # Launch frontend if npm exists
        if shutil.which(NPM_CMD) and (FRONTEND_DIR / "node_modules").exists():
            print("[+] Starting Frontend on http://localhost:5173")
            p_front = subprocess.Popen([NPM_CMD, "run", "dev"], cwd=FRONTEND_DIR)
            processes.append(p_front)
        else:
            print("[i] Frontend node_modules not detected. Access the embedded dashboard at:")
            print(f"  -> http://{args.host}:{args.port}")
            print("  (Run 'python dev.py setup' once to install frontend dependencies)")

        print("\n[*] DevPulse is running! Press Ctrl+C to terminate all services.\n")
        while not any(p.poll() is not None for p in processes):
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[!] Shutting down DevPulse services...")
    finally:
        for p in processes:
            if p.poll() is None:
                p.terminate()
                try:
                    p.wait(timeout=3)
                except Exception:
                    p.kill()
        print("[v] All services stopped cleanly.")
    return 0


def cmd_test(_args: argparse.Namespace) -> int:
    """Runs backend tests."""
    py_bin = get_active_python()
    cmd = [py_bin, "-m", "pytest", "tests", "-v"]
    return subprocess.call(cmd, cwd=BACKEND_DIR)


def cmd_lint(_args: argparse.Namespace) -> int:
    """Runs backend Ruff linter and frontend TypeScript typecheck."""
    py_bin = get_active_python()
    ruff_cmd = [
        py_bin,
        "-m",
        "ruff",
        "check",
        "--config",
        str(BACKEND_DIR / "pyproject.toml"),
        "backend",
        "dev.py",
    ]
    ruff_code = subprocess.call(ruff_cmd, cwd=ROOT_DIR)
    ts_code = 0
    if shutil.which(NPM_CMD) and (FRONTEND_DIR / "node_modules").exists():
        ts_code = subprocess.call([NPM_CMD, "run", "typecheck"], cwd=FRONTEND_DIR)
    return 0 if (ruff_code == 0 and ts_code == 0) else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="DevPulse Developer CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    subparsers.add_parser("setup", help="Set up virtualenv and install dependencies")
    subparsers.add_parser("check", help="Check system prerequisites and tool versions")

    p_back = subparsers.add_parser("backend", help="Run FastAPI backend")
    p_back.add_argument("--host", default="127.0.0.1", help="Host interface")
    p_back.add_argument("--port", type=int, default=8000, help="Port")

    subparsers.add_parser("frontend", help="Run Vite React frontend")

    p_dev = subparsers.add_parser("dev", help="Run both backend and frontend concurrently")
    p_dev.add_argument("--host", default="127.0.0.1", help="Host interface")
    p_dev.add_argument("--port", type=int, default=8000, help="Port")

    subparsers.add_parser("test", help="Run pytest test suite")
    subparsers.add_parser("lint", help="Run code quality linters and type checks")

    args = parser.parse_args()

    commands = {
        "setup": cmd_setup,
        "check": cmd_check,
        "backend": cmd_backend,
        "frontend": cmd_frontend,
        "dev": cmd_dev,
        "test": cmd_test,
        "lint": cmd_lint,
    }

    if args.command in commands:
        code = commands[args.command](args)
        sys.exit(code or 0)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
