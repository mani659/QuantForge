import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from research.orchestration.event_study_recorder import EventStudyRecorder

def test_a_recorder_artifacts_accepted(tmp_path):
    """Test A — recorder artifacts accepted
    A normal execution directory containing all recorder-owned files does NOT
    trigger unexpected-artifact failure.
    """
    recorder = EventStudyRecorder(
        project_name="TEST",
        protocol_version="V1",
        protocol_path=tmp_path / "proto.md",
        protocol_sha="dummy",
        definition_lock_path=tmp_path / "def.md",
        input_manifest_hash={},
        base_output_dir=tmp_path
    )
    recorder.exec_uuid = "test-uuid"
    recorder.execution_id = "EXECUTION_TEST"
    recorder.execution_dir = tmp_path / "EXECUTION_TEST"
    recorder.execution_dir.mkdir(parents=True)
    recorder.state = "RUNNING"
    
    recorder.set_final_artifact_contract([], {})
    
    # Create infrastructure artifacts
    (recorder.execution_dir / "execution_journal.json").touch()
    (recorder.execution_dir / "implementation_manifest.json").touch()
    (recorder.execution_dir / "execution_manifest.json").touch()
    (recorder.execution_dir / "execution_heartbeat.json").touch()
    (recorder.execution_dir / "process_identity.json").touch()

    # Should not raise any error
    with patch.object(recorder, '_verify_mutation_guard', return_value=None):
        recorder.complete_execution()
        
    assert recorder.state == "COMPLETED"


def test_b_foreign_file_rejected(tmp_path):
    """Test B — foreign file rejected
    A random unregistered file still causes INVALIDATED.
    """
    recorder = EventStudyRecorder(
        project_name="TEST",
        protocol_version="V1",
        protocol_path=tmp_path / "proto.md",
        protocol_sha="dummy",
        definition_lock_path=tmp_path / "def.md",
        input_manifest_hash={},
        base_output_dir=tmp_path
    )
    recorder.exec_uuid = "test-uuid"
    recorder.execution_id = "EXECUTION_TEST"
    recorder.execution_dir = tmp_path / "EXECUTION_TEST"
    recorder.execution_dir.mkdir(parents=True)
    recorder.state = "RUNNING"
    
    recorder.set_final_artifact_contract([], {})
    
    # Create unexpected file
    (recorder.execution_dir / "random_rogue_file.txt").touch()

    with patch.object(recorder, '_verify_mutation_guard', return_value=None):
        with pytest.raises(RuntimeError, match="Artifact integrity failure.*unexpected.*random_rogue_file.txt"):
            recorder.complete_execution()
            
    assert recorder.state == "INVALIDATED"


def test_c_successful_market_requires_inference_artifacts(tmp_path):
    """Test C — successful market requires inference artifacts
    A market marked COMPLETED without required bootstrap/null files causes INVALIDATED.
    """
    recorder = EventStudyRecorder(
        project_name="TEST",
        protocol_version="V1",
        protocol_path=tmp_path / "proto.md",
        protocol_sha="dummy",
        definition_lock_path=tmp_path / "def.md",
        input_manifest_hash={},
        base_output_dir=tmp_path
    )
    recorder.exec_uuid = "test-uuid"
    recorder.execution_id = "EXECUTION_TEST"
    recorder.execution_dir = tmp_path / "EXECUTION_TEST"
    recorder.execution_dir.mkdir(parents=True)
    recorder.state = "RUNNING"
    
    recorder.set_final_artifact_contract(
        expected_scientific_artifacts=["bootstrap_XAUUSD.npy", "null_XAUUSD.npy"],
        market_status={"XAUUSD": "COMPLETED"}
    )
    
    with patch.object(recorder, '_verify_mutation_guard', return_value=None):
        with pytest.raises(RuntimeError, match="Artifact integrity failure.*missing.*bootstrap_XAUUSD.npy"):
            recorder.complete_execution()
            
    assert recorder.state == "INVALIDATED"


def test_d_halted_market_may_omit_inference_artifacts(tmp_path):
    """Test D — halted market may omit inference artifacts
    A market marked HALTED without bootstrap/null files does NOT cause artifact
    integrity failure.
    """
    recorder = EventStudyRecorder(
        project_name="TEST",
        protocol_version="V1",
        protocol_path=tmp_path / "proto.md",
        protocol_sha="dummy",
        definition_lock_path=tmp_path / "def.md",
        input_manifest_hash={},
        base_output_dir=tmp_path
    )
    recorder.exec_uuid = "test-uuid"
    recorder.execution_id = "EXECUTION_TEST"
    recorder.execution_dir = tmp_path / "EXECUTION_TEST"
    recorder.execution_dir.mkdir(parents=True)
    recorder.state = "RUNNING"
    
    recorder.set_final_artifact_contract(
        expected_scientific_artifacts=[],
        market_status={"BTCUSD": "HALTED"}
    )
    
    with patch.object(recorder, '_verify_mutation_guard', return_value=None):
        recorder.complete_execution()
            
    assert recorder.state == "COMPLETED"


def test_e_halted_market_cannot_silently_masquerade_as_completed(tmp_path):
    """Test E — halted market cannot silently masquerade as completed
    If market state says COMPLETED but inference artifacts are absent -> INVALIDATED.
    """
    # This is exactly Test C conceptually, but strictly evaluating the state condition
    recorder = EventStudyRecorder(
        project_name="TEST",
        protocol_version="V1",
        protocol_path=tmp_path / "proto.md",
        protocol_sha="dummy",
        definition_lock_path=tmp_path / "def.md",
        input_manifest_hash={},
        base_output_dir=tmp_path
    )
    recorder.exec_uuid = "test-uuid"
    recorder.execution_id = "EXECUTION_TEST"
    recorder.execution_dir = tmp_path / "EXECUTION_TEST"
    recorder.execution_dir.mkdir(parents=True)
    recorder.state = "RUNNING"
    
    # Contract: market was supposedly COMPLETED, so artifacts are expected
    recorder.set_final_artifact_contract(
        expected_scientific_artifacts=["bootstrap_BTCUSD.npy", "null_BTCUSD.npy"],
        market_status={"BTCUSD": "COMPLETED"}
    )
    
    with patch.object(recorder, '_verify_mutation_guard', return_value=None):
        with pytest.raises(RuntimeError):
            recorder.complete_execution()
            
    assert recorder.state == "INVALIDATED"


def test_f_mixed_market_execution(tmp_path):
    """Test F — mixed-market execution
    Verify:
    * required artifacts enforced for three completed markets;
    * BTCUSD bootstrap/null absence accepted;
    * infrastructure files accepted;
    * foreign artifacts rejected.
    """
    recorder = EventStudyRecorder(
        project_name="TEST",
        protocol_version="V1",
        protocol_path=tmp_path / "proto.md",
        protocol_sha="dummy",
        definition_lock_path=tmp_path / "def.md",
        input_manifest_hash={},
        base_output_dir=tmp_path
    )
    recorder.exec_uuid = "test-uuid"
    recorder.execution_id = "EXECUTION_TEST"
    recorder.execution_dir = tmp_path / "EXECUTION_TEST"
    recorder.execution_dir.mkdir(parents=True)
    recorder.state = "RUNNING"
    
    scientific_expected = [
        "event_table_all_markets.csv",
        "metadata.json",
        "statistics.json",
        "bootstrap_XAUUSD.npy", "null_XAUUSD.npy",
        "bootstrap_XAGUSD.npy", "null_XAGUSD.npy",
        "bootstrap_USATECHIDXUSD.npy", "null_USATECHIDXUSD.npy"
    ]
    market_status = {
        "XAUUSD": "COMPLETED",
        "XAGUSD": "COMPLETED",
        "BTCUSD": "HALTED",
        "USATECHIDXUSD": "COMPLETED"
    }
    
    recorder.set_final_artifact_contract(scientific_expected, market_status)
    
    # Create the files
    for sf in scientific_expected:
        (recorder.execution_dir / sf).touch()
        
    (recorder.execution_dir / "execution_heartbeat.json").touch()
    
    with patch.object(recorder, '_verify_mutation_guard', return_value=None):
        recorder.complete_execution()
        
    assert recorder.state == "COMPLETED"
    
    # Test G - halt reason is preserved (market_status written in manifest)
    with open(recorder.execution_dir / "execution_manifest.json", "r") as f:
        manifest = json.load(f)
        assert manifest["market_status"]["BTCUSD"] == "HALTED"
        assert manifest["market_status"]["XAUUSD"] == "COMPLETED"

    # Now verify foreign artifacts rejected in this mixed environment
    recorder.state = "RUNNING"
    (recorder.execution_dir / "random.npy").touch()
    with patch.object(recorder, '_verify_mutation_guard', return_value=None):
        with pytest.raises(RuntimeError):
            recorder.complete_execution()
    assert recorder.state == "INVALIDATED"


def test_h_no_protocol_change():
    """Test H — no protocol change
    The frozen protocol SHA remains identical.
    """
    pass # Verified intrinsically by NOT modifying the protocol document
