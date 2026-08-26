import hashlib
import json
import os
import platform
import subprocess
import sys
import uuid
import threading
import time
import psutil
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Optional


def sha256_file(path: Path) -> Optional[str]:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class EventStudyRecorder:
    """
    Research execution infrastructure for Event Studies.
    Owns execution identity, lifecycle, artifact provenance, and fail-closed persistence.
    Does not contain any scientific logic.
    """

    def __init__(
        self,
        project_name: str,
        protocol_version: str,
        protocol_path: Path,
        protocol_sha: str,
        definition_lock_path: Path,
        input_manifest_hash: Dict[str, str],
        expected_artifacts: List[str] = None,
        entry_script_path: Path = None,
        helper_module_paths: List[Path] = None,
        base_output_dir: Path = Path("output/research_discovery"),
    ):
        self.project_name = project_name
        self.protocol_version = protocol_version
        self.protocol_path = Path(protocol_path)
        self.protocol_sha = protocol_sha
        self.definition_lock_path = Path(definition_lock_path)
        self.input_manifest_hash = input_manifest_hash
        self.expected_artifacts = expected_artifacts or []
        self.market_status = {}
        self.entry_script_path = Path(entry_script_path) if entry_script_path else None
        self.helper_module_paths = [Path(p) for p in (helper_module_paths or [])]
        self.base_output_dir = Path(base_output_dir)

        # Generate Immutable Execution ID
        timestamp_utc = datetime.now(timezone.utc)
        self.start_timestamp = timestamp_utc.isoformat()
        ts_str = timestamp_utc.strftime("%Y%m%dT%H%M%SZ")
        self.exec_uuid = str(uuid.uuid4())
        self.execution_id = f"EXECUTION_{ts_str}_{self.exec_uuid}"

        self.execution_dir = self.base_output_dir / self.project_name / self.protocol_version / self.execution_id

        self.state = "PRE_FLIGHT"
        self.implementation_manifest = {}
        self.process_identity = {}
        self._heartbeat_stop_event = threading.Event()
        self._heartbeat_thread = None

    def _get_git_info(self):
        head = "unknown"
        dirty = "unknown"
        try:
            head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
            status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True).stdout.strip()
            dirty = str(bool(status))
        except Exception:
            pass
        return head, dirty

    def _build_implementation_manifest(self):
        git_head, git_dirty = self._get_git_info()
        helper_hashes = {}
        for hp in self.helper_module_paths:
            helper_hashes[str(hp)] = sha256_file(hp)

        return {
            "execution_id": self.execution_id,
            "protocol_version": self.protocol_version,
            "protocol_sha256": self.protocol_sha,
            "definition_lock_identity": sha256_file(self.definition_lock_path),
            "git_head": git_head,
            "git_dirty_state": git_dirty,
            "python_version": platform.python_version(),
            "package_versions": {
                "pandas": self._get_pkg_version("pandas"),
                "numpy": self._get_pkg_version("numpy"),
            },
            "entry_script_path": str(self.entry_script_path),
            "entry_script_sha256": sha256_file(self.entry_script_path),
            "imported_execution_helper_hashes": helper_hashes,
            "input_manifest_hash": self.input_manifest_hash,
            "start_timestamp": self.start_timestamp,
        }
        
    def _get_git_info(self):
        head = "unknown"
        dirty = "unknown"
        try:
            head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
            status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
            dirty = str(bool(status))
        except Exception:
            pass
        return head, dirty

    def _get_pkg_version(self, pkg_name):
        try:
            import importlib
            return importlib.import_module(pkg_name).__version__
        except Exception:
            return "unknown"

    def preflight(self):
        if self.state != "PRE_FLIGHT":
            raise RuntimeError("preflight() must be called in PRE_FLIGHT state.")

        # Check collision
        if self.execution_dir.exists():
            raise FileExistsError(f"STOP — EXECUTION DIRECTORY ALREADY EXISTS: {self.execution_dir}")

        # Verify Protocol
        if not self.protocol_path.is_file():
            raise FileNotFoundError(f"Protocol file not found: {self.protocol_path}")
        
        actual_protocol_sha = sha256_file(self.protocol_path)
        if actual_protocol_sha != self.protocol_sha:
            raise ValueError(f"Protocol SHA mismatch. Expected: {self.protocol_sha}, Actual: {actual_protocol_sha}")

        # Verify Definition Lock
        if not self.definition_lock_path.is_file():
            raise FileNotFoundError(f"Definition lock file not found: {self.definition_lock_path}")

        # Build and freeze implementation manifest
        self.implementation_manifest = self._build_implementation_manifest()

        # Build process identity
        try:
            p = psutil.Process()
            self.process_identity = {
                "execution_id": self.execution_id,
                "pid": p.pid,
                "process_start_time": p.create_time(),
                "captured_at_utc": datetime.now(timezone.utc).isoformat(),
                "platform": platform.platform(),
                "boot_time": psutil.boot_time()
            }
        except Exception as e:
            raise RuntimeError(f"Fail closed: unable to capture robust process identity. {e}")

    def start(self):
        if self.state != "PRE_FLIGHT":
            raise RuntimeError("start() must be called after preflight() from PRE_FLIGHT state.")
        if not self.implementation_manifest:
            raise RuntimeError("Implementation manifest is empty. Call preflight() first.")

        # Create directory
        self.execution_dir.mkdir(parents=True, exist_ok=False)

        # Write initial journal
        self.state = "RUNNING"
        self._write_journal()
        
        # Write implementation manifest and process identity
        with open(self.execution_dir / "implementation_manifest.json", "w", encoding="utf-8") as f:
            json.dump(self.implementation_manifest, f, indent=2)
            
        with open(self.execution_dir / "process_identity.json", "w", encoding="utf-8") as f:
            json.dump(self.process_identity, f, indent=2)

        # Start heartbeat
        self._heartbeat_stop_event.clear()
        self._heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self._heartbeat_thread.start()

    def _heartbeat_loop(self):
        while not self._heartbeat_stop_event.is_set():
            try:
                p = psutil.Process()
                mem_info = p.memory_info()
                heartbeat = {
                    "monotonic_time": time.monotonic(),
                    "utc_time": datetime.now(timezone.utc).isoformat(),
                    "pid": p.pid,
                    "process_start_time": p.create_time(),
                    "rss_bytes": mem_info.rss,
                    "execution_id": self.execution_id
                }
                with open(self.execution_dir / "execution_heartbeat.json", "w", encoding="utf-8") as f:
                    json.dump(heartbeat, f, indent=2)
            except Exception:
                pass  # observational only, do not terminate execution
            self._heartbeat_stop_event.wait(5.0)

    def _write_journal(self, reason=None):
        journal = {
            "execution_id": self.execution_id,
            "state": self.state,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        if reason:
            journal["reason"] = reason

        with open(self.execution_dir / "execution_journal.json", "w", encoding="utf-8") as f:
            json.dump(journal, f, indent=2)

    def set_final_artifact_contract(self, expected_scientific_artifacts: List[str], market_status: Dict[str, str]):
        self.expected_artifacts = expected_scientific_artifacts
        self.market_status = market_status

    def _write_artifact_manifest(self, final_state: str):
        observed = []
        hashes = {}
        for p in self.execution_dir.iterdir():
            if p.is_file():
                observed.append(p.name)
                hashes[p.name] = sha256_file(p)
                
        # Do not include the manifest itself in expected calculation
        if "execution_manifest.json" in observed:
            observed.remove("execution_manifest.json")
            
        missing = [a for a in self.expected_artifacts if a not in observed]
        infrastructure_artifacts = [
            "execution_journal.json", 
            "implementation_manifest.json", 
            "execution_manifest.json",
            "execution_heartbeat.json",
            "process_identity.json"
        ]
        unexpected = [a for a in observed if a not in self.expected_artifacts and a not in infrastructure_artifacts]
        
        manifest = {
            "execution_identity": self.execution_id,
            "final_state": final_state,
            "market_status": getattr(self, "market_status", {}),
            "expected_artifacts": self.expected_artifacts,
            "infrastructure_expected_artifacts": infrastructure_artifacts,
            "observed_artifacts": observed,
            "missing_artifacts": missing,
            "unexpected_artifacts": unexpected,
            "artifact_hashes": hashes
        }
        with open(self.execution_dir / "execution_manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

    def _verify_mutation_guard(self) -> str:
        current_script_sha = sha256_file(self.entry_script_path)
        if current_script_sha != self.implementation_manifest["entry_script_sha256"]:
            return "EXECUTION_IMPLEMENTATION_MUTATED"
            
        for hp in self.helper_module_paths:
            if sha256_file(hp) != self.implementation_manifest["imported_execution_helper_hashes"][str(hp)]:
                return "EXECUTION_IMPLEMENTATION_MUTATED"
                
        actual_protocol_sha = sha256_file(self.protocol_path)
        if actual_protocol_sha != self.protocol_sha:
            return "PROTOCOL_MUTATED_AFTER_PREFLIGHT"
            
        return None

    def _stop_heartbeat(self):
        if self._heartbeat_thread and self._heartbeat_thread.is_alive():
            self._heartbeat_stop_event.set()
            self._heartbeat_thread.join(timeout=1.0)

    def complete_execution(self):
        if self.state != "RUNNING":
            raise RuntimeError(f"Cannot complete execution from {self.state} state.")
            
        mutation_reason = self._verify_mutation_guard()
        if mutation_reason:
            self.invalidate_execution(reason=mutation_reason)
            raise RuntimeError(f"Mutation detected: {mutation_reason}. State set to INVALIDATED.")

        # Check artifact invariants before completing
        observed = []
        for p in self.execution_dir.iterdir():
            if p.is_file():
                observed.append(p.name)
        if "execution_manifest.json" in observed:
            observed.remove("execution_manifest.json")
            
        missing = [a for a in self.expected_artifacts if a not in observed]
        infrastructure_artifacts = [
            "execution_journal.json", 
            "implementation_manifest.json", 
            "execution_manifest.json",
            "execution_heartbeat.json",
            "process_identity.json"
        ]
        unexpected = [a for a in observed if a not in self.expected_artifacts and a not in infrastructure_artifacts]
        
        if missing or unexpected:
            reason = "ARTIFACT_INTEGRITY_FAILURE"
            self.state = "INVALIDATED"
            self._write_artifact_manifest(final_state="INVALIDATED")
            self._write_journal(reason=reason)
            raise RuntimeError(f"Artifact integrity failure: missing={missing}, unexpected={unexpected}")

        self.state = "COMPLETED"
        self._stop_heartbeat()
        self._write_artifact_manifest(final_state="COMPLETED")
        self._write_journal()

    def interrupt_execution(self, reason: str):
        if self.state in ("COMPLETED", "INVALIDATED", "INTERRUPTED"):
            return
        self.state = "INTERRUPTED"
        self._stop_heartbeat()
        self._write_artifact_manifest(final_state="INTERRUPTED")
        self._write_journal(reason=reason)

    def invalidate_execution(self, reason: str):
        if self.state in ("COMPLETED", "INVALIDATED", "INTERRUPTED"):
            return
        self.state = "INVALIDATED"
        self._stop_heartbeat()
        self._write_artifact_manifest(final_state="INVALIDATED")
        self._write_journal(reason=reason)

    @property
    def output_dir(self) -> Path:
        return self.execution_dir
