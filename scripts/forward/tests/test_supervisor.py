import os
import sys
import pytest

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

from module_registry import get_registry

def test_registry_loading(tmp_path):
    modules = get_registry(str(tmp_path))
    assert len(modules) == 2
    
    cand_024 = next(m for m in modules if m.candidate_id == "CAND-024")
    cand_035 = next(m for m in modules if m.candidate_id == "CAND-035")
    
    assert cand_024.config["mapping_id"] == "MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0"
    assert cand_035.config["mapping_id"] == "MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0"
    
    # Check isolation
    assert cand_024.module_dir != cand_035.module_dir
    assert os.path.exists(cand_024.module_dir)
    assert os.path.exists(cand_035.module_dir)
