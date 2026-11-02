#!/usr/bin/env python3
"""
DevPulse Developer Runner CLI.

A unified runner to set up, develop, test, and run the DevPulse full-stack project.
Usage:
    python dev.py setup     - Install backend and frontend dependencies
    python dev.py backend   - Run FastAPI server with auto-reload (port 8000)
    python dev.py frontend  - Run Vite React frontend dev server (port 5173)
    python dev.py dev       - Run both backend & frontend concurrently
    python dev.py test      - Run backend unit tests
    python dev.py check     - Check environment prerequisites
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Ensure UTF-8 output encoding across Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"
IS_WINDOWS = sys.platform.startswith("win")

# Determine venv python & pip paths
if IS_WINDOWS:
    VENV_PYTHON = ROOT_DIR / ".venv" / "Scripts" / "python.exe"
    VENV_UVICORN = ROOT_DIR / ".venv" / "Scripts" / "uvicorn.exe"
    VENV_PYTEST = ROOT_DIR / ".venv" / "Scripts" / "pytest.exe"
    NPM_CMD = "npm.cmd" if shutil.which("npm.cmd") else "npm"
else:
    VENV_PYTHON = ROOT_DIR / ".venv" / "bin" / "python"
    VENV_UVICORN = ROOT_DIR / ".venv" / "bin" / "uvicorn"
    VENV_PYTEST = ROOT_DIR / ".venv" / "bin" / "pytest"
    NPM_CMD = "npm"


def get_active_python() -> str:
    """Returns path to the venv python if present, else fallback to current python."""
    if VENV_PYTHON.exists():
        return str(VENV_PYTHON)
    return sys.executable


def run_command(cmd, cwd=None, env=None) -> int:
    """Runs a shell command and returns exit code."""
    printable = " ".join(cmd) if isinstance(cmd, list) else cmd
    print(f"\n[*] [DevPulse] Running: {printable}")
    return subprocess.call(cmd, cwd=cwd or ROOT_DIR, env=env)


def cmd_check(args):
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
    print(f"Virtualenv (.venv): {'Ready' if venv_ok else 'Not created (run: python dev.py setup)'}")
    print("==========================================")


def cmd_setup(args):
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
    pip_install = [py_bin, "-m", "pip", "install", "--upgrade", "pip"]
    subprocess.call(pip_install)

    reqs_file = BACKEND_DIR / "requirements.txt"
    res = subprocess.call([py_bin, "-m", "pip", "install", "-r", str(reqs_file)])
    if res != 0:
        print("[!] Backend dependency install finished with warnings or errors.")
    else:
        print("[v] Backend dependencies installed.")

    # 3. Install frontend dependencies if npm is available
    if shutil.which(NPM_CMD):
        print("\n[+] Installing frontend dependencies in frontend/ ...")
        res = subprocess.call([NPM_CMD, "install"], cwd=FRONTEND_DIR)
        if res == 0:
            print("[v] Frontend dependencies installed.")
        else:
            print("[!] Frontend install exited with code", res)
    else:
        print("\n[!] Node/NPM not found. You can still run the FastAPI backend!")

    print("\n[v] Setup complete! To start development:")
    print("   python dev.py dev       (runs backend + frontend)")
    print("   python dev.py backend   (runs backend only at http://localhost:8000)")


def cmd_backend(args):
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


def cmd_frontend(args):
    """Runs Vite dev server."""
    if not shutil.which(NPM_CMD):
        print("[x] npm not found in system PATH. Please install Node.js.")
        return 1
    print("[*] Starting Vite frontend server at http://localhost:5173 ...")
    return subprocess.call([NPM_CMD, "run", "dev"], cwd=FRONTEND_DIR)


def cmd_dev(args):
    """Runs both backend and frontend concurrently."""
    import time

    py_bin = get_active_python()
    processes = []

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
        print(f"[+] Starting Backend on http://{args.host}:{args.port} (Docs: http://{args.host}:{args.port}/docs)")
        p_back = subprocess.Popen(b_cmd, cwd=BACKEND_DIR)
        processes.append(p_back)

        # Launch frontend if npm exists
        if shutil.which(NPM_CMD) and (FRONTEND_DIR / "node_modules").exists():
            print("[+] Starting Frontend on http://localhost:5173")
            p_front = subprocess.Popen([NPM_CMD, "run", "dev"], cwd=FRONTEND_DIR)
            processes.append(p_front)
        else:
            print("[i] Frontend node_modules not detected. Access the embedded dashboard at:")
            print(f"  👉 http://{args.host}:{args.port}")
            print("  (Run 'python dev.py setup' once to install frontend dependencies)")

        print("\n[*] DevPulse is running! Press Ctrl+C to terminate all services.\n")
        while True:
            time.sleep(1)
            for p in processes:
                if p.poll() is not None:
                    break

    except KeyboardInterrupt:
        print("\n[!] Shutting down DevPulse services...")
    finally:
        for p in processes:
            p.terminate()
            try:
                p.wait(timeout=3)
            except Exception:
                p.kill()
        print("[v] All services stopped cleanly.")


def cmd_test(args):
    """Runs backend tests."""
    py_bin = get_active_python()
    cmd = [py_bin, "-m", "pytest", "tests", "-v"]
    return subprocess.call(cmd, cwd=BACKEND_DIR)


def main():
    parser = argparse.ArgumentParser(description="DevPulse Developer CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # setup
    subparsers.add_parser("setup", help="Set up virtualenv and install dependencies")

    # check
    subparsers.add_parser("check", help="Check system prerequisites and tool versions")

    # backend
    p_back = subparsers.add_parser("backend", help="Run FastAPI backend")
    p_back.add_argument("--host", default="127.0.0.1", help="Host interface")
    p_back.add_argument("--port", type=int, default=8000, help="Port")

    # frontend
    subparsers.add_parser("frontend", help="Run Vite React frontend")

    # dev / full
    p_dev = subparsers.add_parser("dev", help="Run both backend and frontend concurrently")
    p_dev.add_argument("--host", default="127.0.0.1", help="Host interface")
    p_dev.add_argument("--port", type=int, default=8000, help="Port")

    # test
    subparsers.add_parser("test", help="Run pytest test suite")

    args = parser.parse_args()

    commands = {
        "setup": cmd_setup,
        "check": cmd_check,
        "backend": cmd_backend,
        "frontend": cmd_frontend,
        "dev": cmd_dev,
        "test": cmd_test,
    }

    if args.command in commands:
        code = commands[args.command](args)
        sys.exit(code or 0)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
