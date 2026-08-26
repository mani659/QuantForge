import os
import shutil
import tempfile
import uuid
import pytest
from pathlib import Path
from research.orchestration.event_study_recorder import EventStudyRecorder, sha256_file

@pytest.fixture
def setup_env():
    temp_dir = Path(tempfile.mkdtemp())
    
    # Create mock protocol
    protocol_path = temp_dir / "protocol.md"
    protocol_path.write_text("dummy protocol content")
    protocol_sha = sha256_file(protocol_path)
    
    # Create mock definition lock
    def_lock_path = temp_dir / "def_lock.md"
    def_lock_path.write_text("dummy lock content")
    
    # Create mock script
    script_path = temp_dir / "script.py"
    script_path.write_text("print('hello')")
    
    base_out = temp_dir / "output"
    
    yield {
        "temp_dir": temp_dir,
        "protocol_path": protocol_path,
        "protocol_sha": protocol_sha,
        "def_lock_path": def_lock_path,
        "script_path": script_path,
        "base_out": base_out
    }
    
    shutil.rmtree(temp_dir)

def create_recorder(env, **kwargs):
    default_args = {
        "project_name": "TEST",
        "protocol_version": "V1",
        "protocol_path": env["protocol_path"],
        "protocol_sha": env["protocol_sha"],
        "definition_lock_path": env["def_lock_path"],
        "input_manifest_hash": {"file.csv": "abc"},
        "expected_artifacts": ["output.csv"],
        "entry_script_path": env["script_path"],
        "base_output_dir": env["base_out"]
    }
    default_args.update(kwargs)
    return EventStudyRecorder(**default_args)

def test_a_historical_execution_preserved(setup_env):
    """Test A & J: Existing historical execution directory is preserved and not touched."""
    env = setup_env
    # Create a dummy historical run
    hist_dir = env["base_out"] / "TEST" / "V1" / "EXECUTION_OLD"
    hist_dir.mkdir(parents=True)
    sentinel = hist_dir / "sentinel.txt"
    sentinel.write_text("do not touch")
    orig_stat = sentinel.stat()
    
    recorder = create_recorder(env)
    recorder.preflight()
    recorder.start()
    
    # Assert sentinel untouched
    assert sentinel.read_text() == "do not touch"
    assert sentinel.stat().st_mtime == orig_stat.st_mtime
    assert recorder.output_dir != hist_dir

def test_b_new_execution_unique_directory(setup_env):
    """Test B: New execution receives a unique directory."""
    rec1 = create_recorder(setup_env)
    rec2 = create_recorder(setup_env)
    assert rec1.output_dir != rec2.output_dir

def test_c_collision_fails_closed(setup_env):
    """Test C: Collision at exact execution path fails closed."""
    rec = create_recorder(setup_env)
    rec.execution_dir.mkdir(parents=True)
    with pytest.raises(FileExistsError, match="EXECUTION DIRECTORY ALREADY EXISTS"):
        rec.preflight()

def test_d_historical_sibling_does_not_block(setup_env):
    """Test D: Historical sibling directories do not block new execution."""
    env = setup_env
    hist_dir = env["base_out"] / "TEST" / "V1" / "EXECUTION_OLD"
    hist_dir.mkdir(parents=True)
    
    rec = create_recorder(env)
    rec.preflight()  # Should not raise
    rec.start()      # Should not raise
    assert rec.output_dir.exists()

def test_f_interrupted_creates_record(setup_env):
    """Test F: Interrupted execution creates an immutable execution record."""
    rec = create_recorder(setup_env)
    rec.preflight()
    rec.start()
    rec.interrupt_execution("MemoryError")
    
    assert rec.state == "INTERRUPTED"
    manifest_path = rec.output_dir / "execution_manifest.json"
    assert manifest_path.exists()
    import json
    data = json.loads(manifest_path.read_text())
    assert data["final_state"] == "INTERRUPTED"
    assert "output.csv" in data["missing_artifacts"]

def test_g_implementation_hash_recorded(setup_env):
    """Test G: Implementation hash is recorded."""
    rec = create_recorder(setup_env)
    rec.preflight()
    rec.start()
    
    manifest_path = rec.output_dir / "implementation_manifest.json"
    assert manifest_path.exists()
    import json
    data = json.loads(manifest_path.read_text())
    assert "entry_script_sha256" in data
    assert data["entry_script_sha256"] == sha256_file(setup_env["script_path"])

def test_h_mutation_causes_invalidation(setup_env):
    """Test H: Implementation mutation before finalization causes invalidation/STOP."""
    env = setup_env
    rec = create_recorder(env)
    rec.preflight()
    rec.start()
    
    # Mutate script
    env["script_path"].write_text("print('mutated')")
    
    with pytest.raises(RuntimeError, match="Mutation detected: EXECUTION_IMPLEMENTATION_MUTATED"):
        rec.complete_execution()
        
    assert rec.state == "INVALIDATED"
    import json
    journal = json.loads((rec.output_dir / "execution_journal.json").read_text())
    assert journal["state"] == "INVALIDATED"
    assert journal["reason"] == "EXECUTION_IMPLEMENTATION_MUTATED"

def test_i_artifact_manifest_detects_missing(setup_env):
    """Test I: Artifact manifest detects missing files and fails closed."""
    rec = create_recorder(setup_env)
    rec.preflight()
    rec.start()
    
    # Do not create output.csv
    with pytest.raises(RuntimeError, match="Artifact integrity failure"):
        rec.complete_execution()
        
    assert rec.state == "INVALIDATED"
    import json
    data = json.loads((rec.output_dir / "execution_manifest.json").read_text())
    assert data["final_state"] == "INVALIDATED"
    assert "output.csv" in data["missing_artifacts"]

def test_i_artifact_manifest_detects_unexpected(setup_env):
    """Test I: Artifact manifest detects unexpected files and fails closed."""
    rec = create_recorder(setup_env)
    rec.preflight()
    rec.start()
    
    # Create expected
    (rec.output_dir / "output.csv").write_text("dummy")
    
    # Create unexpected artifact
    (rec.output_dir / "unexpected.txt").write_text("hello")
    
    with pytest.raises(RuntimeError, match="Artifact integrity failure"):
        rec.complete_execution()
        
    assert rec.state == "INVALIDATED"
    import json
    data = json.loads((rec.output_dir / "execution_manifest.json").read_text())
    assert data["final_state"] == "INVALIDATED"
    assert "unexpected.txt" in data["unexpected_artifacts"]

def test_j_protocol_mutation_causes_invalidation(setup_env):
    """Test J: Protocol mutation before finalization causes invalidation."""
    env = setup_env
    rec = create_recorder(env)
    rec.preflight()
    rec.start()
    
    # Create expected output
    (rec.output_dir / "output.csv").write_text("dummy")
    
    # Mutate protocol
    env["protocol_path"].write_text("mutated protocol content")
    
    with pytest.raises(RuntimeError, match="Mutation detected: PROTOCOL_MUTATED_AFTER_PREFLIGHT"):
        rec.complete_execution()
        
    assert rec.state == "INVALIDATED"
    import json
    journal = json.loads((rec.output_dir / "execution_journal.json").read_text())
    assert journal["state"] == "INVALIDATED"
    assert journal["reason"] == "PROTOCOL_MUTATED_AFTER_PREFLIGHT"
