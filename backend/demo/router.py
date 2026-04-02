import subprocess
import sys
import threading
from pathlib import Path

from fastapi import APIRouter

router = APIRouter(prefix="/demo", tags=["demo"])

SIMULATOR_PATH = str(Path(__file__).parent.parent.parent / "simulator" / "main.py")

_lock = threading.Lock()
_proc: subprocess.Popen | None = None


def _is_running() -> bool:
    return _proc is not None and _proc.poll() is None


@router.post("/start", summary="Start the device simulator")
def start_demo():
    global _proc
    with _lock:
        if _is_running():
            return {"success": False, "message": "Simulator already running"}
        _proc = subprocess.Popen(
            [sys.executable, SIMULATOR_PATH],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    return {"success": True, "message": "Simulator started"}


@router.post("/stop", summary="Stop the device simulator")
def stop_demo():
    global _proc
    with _lock:
        if not _is_running():
            return {"success": False, "message": "Simulator not running"}
        _proc.terminate()
        try:
            _proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            _proc.kill()
        _proc = None
    return {"success": True, "message": "Simulator stopped"}


@router.get("/status", summary="Check simulator status")
def demo_status():
    with _lock:
        return {"running": _is_running()}
