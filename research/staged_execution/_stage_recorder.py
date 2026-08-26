"""Staged economic execution — StageRunRecorder.

A lightweight execution-identity infrastructure for the REPEATABLE stages
(Stage 0 preflight, Stage 1 preparation, Stage 3 verification).  It mirrors the
approved `research/orchestration/event_study_recorder.py` pattern exactly
(isolation, heartbeat, process identity, fail-closed finalization) and writes
the same five infrastructure artifacts, so that
`scripts/reconcile_execution.py` can formally reconcile a crashed stage dir to
CRASHED (PID + create-time + boot-time detection; no resume).

It contains no scientific or economic logic.  Stage 2 continues to use the
approved EventStudyRecorder unmodified.
"""

from __future__ import annotations

import json
import platform
import subprocess
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import psutil

from ._identity import sha256_file

HEARTBEAT_INTERVAL_S = 5.0

_INFRA_ARTIFACTS = [
    "execution_journal.json",
    "implementation_manifest.json",
    "execution_manifest.json",
    "execution_heartbeat.json",
    "process_identity.json",
]


class StageRunRecorder:
    """Stage identity orchestrator for repeatable, non-economic stages."""

    def __init__(
        self,
        directory: Path,
        stage_name: str,
        protocol_sha: str,
        entry_script_path: Path,
        helper_module_paths=None,
        extra_identity: dict | None = None,
    ):
        self.directory = Path(directory)
        self.stage_name = stage_name
        self.protocol_sha = protocol_sha
        self.entry_script_path = Path(entry_script_path)
        self.helper_module_paths = [Path(p) for p in (helper_module_paths or [])]
        self.extra_identity = extra_identity or {}

        self.execution_id = self.directory.name
        self.state = "PRE_FLIGHT"
        self._heartbeat_stop = threading.Event()
        self._heartbeat_thread = None

        p = psutil.Process()
        self.process_identity = {
            "execution_id": self.execution_id,
            "pid": p.pid,
            "process_start_time": p.create_time(),
            "captured_at_utc": datetime.now(timezone.utc).isoformat(),
            "platform": platform.platform(),
            "boot_time": psutil.boot_time(),
        }
        self.implementation_manifest = None

    # ------------------------------------------------------------------
    # lifecycle
    # ------------------------------------------------------------------

    def start(self):
        if self.state != "PRE_FLIGHT":
            raise RuntimeError(f"start() requires PRE_FLIGHT, got {self.state}")
        if self.directory.exists():
            raise FileExistsError(
                f"STOP — STAGE DIRECTORY ALREADY EXISTS: {self.directory}"
            )
        self.directory.mkdir(parents=True, exist_ok=False)

        self.implementation_manifest = self._build_implementation_manifest()
        self.state = "RUNNING"
        self._write_journal()
        with open(self.directory / "implementation_manifest.json", "w", encoding="utf-8") as f:
            json.dump(self.implementation_manifest, f, indent=2)
        with open(self.directory / "process_identity.json", "w", encoding="utf-8") as f:
            json.dump(self.process_identity, f, indent=2)

        self._heartbeat_stop.clear()
        self._heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop, daemon=True
        )
        self._heartbeat_thread.start()

    def _build_implementation_manifest(self):
        git_head, git_dirty = self._get_git_info()
        helper_hashes = {str(hp): sha256_file(hp) for hp in self.helper_module_paths}
        manifest = {
            "stage_name": self.stage_name,
            "execution_id": self.execution_id,
            "protocol_sha256": self.protocol_sha,
            "git_head": git_head,
            "git_dirty_state": git_dirty,
            "python_version": platform.python_version(),
            "entry_script_path": str(self.entry_script_path),
            "entry_script_sha256": sha256_file(self.entry_script_path),
            "imported_stage_helper_hashes": helper_hashes,
            "start_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        }
        manifest.update(self.extra_identity)
        return manifest

    @staticmethod
    def _get_git_info():
        head = "unknown"
        dirty = "unknown"
        try:
            head = subprocess.run(
                ["git", "rev-parse", "HEAD"], capture_output=True, text=True
            ).stdout.strip()
            status = subprocess.run(
                ["git", "status", "--porcelain"], capture_output=True, text=True
            ).stdout.strip()
            dirty = str(bool(status))
        except Exception:
            pass
        return head, dirty

    def _heartbeat_loop(self):
        while not self._heartbeat_stop.is_set():
            try:
                p = psutil.Process()
                heartbeat = {
                    "monotonic_time": time.monotonic(),
                    "utc_time": datetime.now(timezone.utc).isoformat(),
                    "pid": p.pid,
                    "process_start_time": p.create_time(),
                    "rss_bytes": p.memory_info().rss,
                    "execution_id": self.execution_id,
                }
                with open(self.directory / "execution_heartbeat.json", "w", encoding="utf-8") as f:
                    json.dump(heartbeat, f, indent=2)
            except Exception:
                pass
            self._heartbeat_stop.wait(HEARTBEAT_INTERVAL_S)

    def _write_journal(self, reason=None):
        journal = {
            "execution_id": self.execution_id,
            "state": self.state,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        if reason:
            journal["reason"] = reason
        with open(self.directory / "execution_journal.json", "w", encoding="utf-8") as f:
            json.dump(journal, f, indent=2)

    # ------------------------------------------------------------------
    # finalization
    # ------------------------------------------------------------------

    def _verify_mutation_guard(self):
        if self.entry_script_path.is_file():
            if sha256_file(self.entry_script_path) != self.implementation_manifest.get(
                "entry_script_sha256"
            ):
                return "EXECUTION_IMPLEMENTATION_MUTATED"
        for hp in self.helper_module_paths:
            recorded = self.implementation_manifest.get(
                "imported_stage_helper_hashes", {}
            ).get(str(hp))
            if recorded is not None and sha256_file(hp) != recorded:
                return "EXECUTION_IMPLEMENTATION_MUTATED"
        return None

    def _write_artifact_manifest(self, final_state: str, extra: dict | None = None):
        observed = []
        hashes = {}
        for p in self.directory.iterdir():
            if p.is_file() and p.name != "execution_manifest.json":
                observed.append(p.name)
                hashes[p.name] = sha256_file(p)
        manifest = {
            "execution_identity": self.execution_id,
            "stage_name": self.stage_name,
            "final_state": final_state,
            "observed_artifacts": observed,
            "infrastructure_artifacts": _INFRA_ARTIFACTS,
            "artifact_hashes": hashes,
            "scientific_validity": False,
            "economic_evidence": False,
        }
        if extra:
            manifest.update(extra)
        with open(self.directory / "execution_manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

    def complete(self, extra: dict | None = None):
        if self.state != "RUNNING":
            raise RuntimeError(f"Cannot complete stage from {self.state} state.")
        mutation = self._verify_mutation_guard()
        if mutation:
            self.invalidate(reason=mutation)
            raise RuntimeError(f"Mutation detected: {mutation}. Stage INVALIDATED.")
        self.state = "COMPLETED"
        self._stop_heartbeat()
        self._write_artifact_manifest("COMPLETED", extra)
        self._write_journal()

    def invalidate(self, reason: str):
        if self.state in ("COMPLETED", "INVALIDATED", "INTERRUPTED"):
            return
        self.state = "INVALIDATED"
        self._stop_heartbeat()
        self._write_artifact_manifest("INVALIDATED")
        self._write_journal(reason=reason)

    def interrupt(self, reason: str):
        if self.state in ("COMPLETED", "INVALIDATED", "INTERRUPTED"):
            return
        self.state = "INTERRUPTED"
        self._stop_heartbeat()
        self._write_artifact_manifest("INTERRUPTED")
        self._write_journal(reason=reason)

    def _stop_heartbeat(self):
        if self._heartbeat_thread and self._heartbeat_thread.is_alive():
            self._heartbeat_stop.set()
            self._heartbeat_thread.join(timeout=1.0)