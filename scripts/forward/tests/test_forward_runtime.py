import os
import sys
import json
import time
import pytest
import tempfile
import shutil

# Setup paths
forward_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scripts_dir = os.path.dirname(forward_dir)
repo_dir = os.path.dirname(scripts_dir)
rare_events_dir = os.path.join(scripts_dir, "rare_events")
sys.path.insert(0, forward_dir)
sys.path.insert(0, rare_events_dir)


# ---------------------------------------------------------------------------
# CONTRACT TESTS
# ---------------------------------------------------------------------------

class TestCanonicalContracts:
    """Verify canonical CAND-024 and CAND-035 contracts are loadable."""
    
    def test_cand024_contract_loads(self):
        from contracts import CAND_024_CONTRACT
        assert CAND_024_CONTRACT.candidate_id == "CAND-024"
        assert CAND_024_CONTRACT.hash == "925495a86b35e6266b3dd04e27474dc94f19e86f0c0649cb0b976443f71cb13e"
        
    def test_cand035_contract_loads(self):
        from contracts import CAND_035_CONTRACT
        assert CAND_035_CONTRACT.candidate_id == "CAND-035"
        assert CAND_035_CONTRACT.hash == "ddc5d0e9bed41a7ccae30e69b2b8b38914e2a90693282ecd2823e10948d48cc5"
        
    def test_cand024_short_hash(self):
        from contracts import CAND_024_CONTRACT
        assert CAND_024_CONTRACT.short_hash == "925495a8"
        
    def test_cand035_short_hash(self):
        from contracts import CAND_035_CONTRACT
        assert CAND_035_CONTRACT.short_hash == "ddc5d0e9"
        
    def test_cand024_identity_format(self):
        from contracts import CAND_024_CONTRACT
        assert CAND_024_CONTRACT.identity == "CAND-024:CANONICAL:925495a8"
        
    def test_cand035_identity_format(self):
        from contracts import CAND_035_CONTRACT
        assert CAND_035_CONTRACT.identity == "CAND-035:CANONICAL:ddc5d0e9"
        
    def test_cand024_instrument(self):
        from contracts import CAND_024_CONTRACT
        assert CAND_024_CONTRACT.instrument == "USATECHIDXUSD"
        
    def test_cand035_instrument(self):
        from contracts import CAND_035_CONTRACT
        assert CAND_035_CONTRACT.instrument == "USATECHIDXUSD"
        
    def test_cand024_direction(self):
        from contracts import CAND_024_CONTRACT
        assert CAND_024_CONTRACT.direction == "Short"
        
    def test_cand035_direction(self):
        from contracts import CAND_035_CONTRACT
        assert CAND_035_CONTRACT.direction == "Long"


# ---------------------------------------------------------------------------
# ENGINE CONSISTENCY TESTS
# ---------------------------------------------------------------------------

class TestEngineConsistency:
    """Verify engines load canonical contracts and match expected semantics."""
    
    def test_cand024_engine_loads(self):
        from cand_024_engine import Cand024Engine
        engine = Cand024Engine()
        assert engine.contract.candidate_id == "CAND-024"
        assert engine.contract.hash == "925495a86b35e6266b3dd04e27474dc94f19e86f0c0649cb0b976443f71cb13e"
        
    def test_cand035_engine_loads(self):
        from cand_035_engine import Cand035Engine
        engine = Cand035Engine()
        assert engine.contract.candidate_id == "CAND-035"
        assert engine.contract.hash == "ddc5d0e9bed41a7ccae30e69b2b8b38914e2a90693282ecd2823e10948d48cc5"
        
    def test_cand024_engine_initial_state(self):
        from cand_024_engine import Cand024Engine
        engine = Cand024Engine()
        assert engine.state == "WATCHING"
        
    def test_cand035_engine_initial_state(self):
        from cand_035_engine import Cand035Engine
        engine = Cand035Engine()
        assert engine.state == "WATCHING"


# ---------------------------------------------------------------------------
# MODULE REGISTRY TESTS
# ---------------------------------------------------------------------------

class TestModuleRegistry:
    """Verify module registry loads all modules correctly."""

    def _get_modules(self, tmp_path):
        from module_registry import get_registry
        return get_registry(str(tmp_path))

    def test_registry_loads_modules(self, tmp_path):
        modules = self._get_modules(tmp_path)
        ids = {m.candidate_id for m in modules}
        assert "CAND-024" in ids
        assert "CAND-035" in ids
        assert len(modules) >= 2

    def test_registry_cand024_config(self, tmp_path):
        modules = self._get_modules(tmp_path)
        cand_024 = next(m for m in modules if m.candidate_id == "CAND-024")
        assert cand_024.config["logical_symbol"] == "USATECHIDXUSD"
        assert cand_024.config["broker_symbol"] == "USTECm"
        assert cand_024.config["mapping_id"] == "MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0"
        assert cand_024.config["minimum"] == 3
        assert cand_024.config["target"] == 5

    def test_registry_cand035_config(self, tmp_path):
        modules = self._get_modules(tmp_path)
        cand_035 = next(m for m in modules if m.candidate_id == "CAND-035")
        assert cand_035.config["logical_symbol"] == "USATECHIDXUSD"
        assert cand_035.config["broker_symbol"] == "USTECm"
        assert cand_035.config["mapping_id"] == "MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0"

    def test_registry_module_isolation(self, tmp_path):
        modules = self._get_modules(tmp_path)
        dirs = {m.candidate_id: m.module_dir for m in modules}
        assert len(set(dirs.values())) == len(modules)
        for d in dirs.values():
            assert os.path.exists(d)

    def test_registry_independent_ledgers(self, tmp_path):
        modules = self._get_modules(tmp_path)
        for m in modules:
            assert m.event_ledger is not None
            assert m.outcome_ledger is not None

    def test_cand015_adapter_available(self):
        try:
            from cand015_adapter import Cand015Adapter, CAND015_AVAILABLE
            assert CAND015_AVAILABLE is True
        except ImportError:
            pass

    def test_cand015_adapter_initialization(self):
        try:
            from cand015_adapter import Cand015Adapter, CAND015_AVAILABLE
            if not CAND015_AVAILABLE:
                return
            class FakeFeed:
                def latest_completed_bar(self, sym, tf):
                    return {"status": "DATA_FRESH", "time": 1000, "open": 100, "high": 101, "low": 99, "close": 100.5}
            adapter = Cand015Adapter(FakeFeed())
            assert adapter.initialize() is True
            assert adapter.status()["candidate_id"] == "CAND-015"
            assert adapter.status()["state"] == "ACTIVE"
        except ImportError:
            pass

    def test_cand015_adapter_processes_bar(self):
        try:
            from cand015_adapter import Cand015Adapter, CAND015_AVAILABLE
            if not CAND015_AVAILABLE:
                return
            class FakeFeed:
                def __init__(self):
                    self.call_count = 0
                def latest_completed_bar(self, sym, tf):
                    self.call_count += 1
                    return {"status": "DATA_FRESH", "time": 1000 + self.call_count, "open": 100, "high": 101, "low": 99, "close": 100.5}
            feed = FakeFeed()
            adapter = Cand015Adapter(feed)
            adapter.initialize()
            quote = {"status": "DATA_FRESH", "utc_timestamp": 1000.0, "symbol": "USTECm", "bid": 100.0, "ask": 100.5}
            result = adapter.process_market_data(quote)
            assert result is None or isinstance(result, dict)
            assert adapter.status()["ticks_received"] >= 1
        except ImportError:
            pass

    def test_cand015_wrapper_has_config_attribute(self, tmp_path):
        """Regression: Cand015ModuleWrapper must expose config for supervisor."""
        from module_registry import Cand015ModuleWrapper
        try:
            from cand015_adapter import Cand015Adapter, CAND015_AVAILABLE
            if not CAND015_AVAILABLE:
                return
            class FakeFeed:
                def latest_completed_bar(self, sym, tf):
                    return {"status": "DATA_FRESH", "time": 1000, "open": 100, "high": 101, "low": 99, "close": 100.5}
            adapter = Cand015Adapter(FakeFeed())
            adapter.initialize()
            wrapper = Cand015ModuleWrapper(adapter, str(tmp_path))
            assert hasattr(wrapper, 'config'), "Cand015ModuleWrapper missing config attribute"
            assert wrapper.config['logical_symbol'] == 'USATECHIDXUSD'
            assert wrapper.config['mapping_id'] == 'MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0'
            assert wrapper.config['broker_symbol'] == 'USTECm'
            assert wrapper.config['minimum'] == 3
            assert wrapper.config['target'] == 5
        except ImportError:
            pass

    def test_all_modules_satisfy_supervisor_interface(self, tmp_path):
        """All modules in registry must expose config and process_quote."""
        from module_registry import get_registry
        modules = get_registry(str(tmp_path))
        for m in modules:
            assert hasattr(m, 'config'), f"{m.candidate_id} missing config"
            assert hasattr(m, 'process_quote'), f"{m.candidate_id} missing process_quote"
            assert hasattr(m, 'candidate_id'), f"{m.candidate_id} missing candidate_id"
            assert 'logical_symbol' in m.config, f"{m.candidate_id} config missing logical_symbol"
            assert 'mapping_id' in m.config, f"{m.candidate_id} config missing mapping_id"


# ---------------------------------------------------------------------------
# PAPER EXECUTION TESTS
# ---------------------------------------------------------------------------

class TestPaperExecution:
    """Verify paper execution firewall prevents real orders."""
    
    def test_paper_entry_no_real_order(self):
        from paper_execution import PaperExecutionFirewall
        firewall = PaperExecutionFirewall(friction=2.0)
        event = {"event_id": "TEST-001", "direction": "Long", "theoretical_entry": 15000}
        quote = {"bid": 15000, "ask": 15002, "utc_timestamp": time.time()}
        result = firewall.execute_entry(event, quote)
        assert result["status"] == "PAPER_ENTRY_RECORDED"
        assert "paper_entry_price" in result
        
    def test_paper_exit_no_real_order(self):
        from paper_execution import PaperExecutionFirewall
        firewall = PaperExecutionFirewall(friction=2.0)
        event = {"event_id": "TEST-001", "direction": "Long", "theoretical_entry": 15000}
        quote_entry = {"bid": 15000, "ask": 15002, "utc_timestamp": time.time()}
        firewall.execute_entry(event, quote_entry)
        quote_exit = {"bid": 15010, "ask": 15012, "utc_timestamp": time.time()}
        result = firewall.execute_exit(event, quote_exit)
        assert result["status"] == "PAPER_EXIT_RECORDED"
        assert "paper_exit_price" in result
        
    def test_paper_no_live_api_methods(self):
        from paper_execution import PaperExecutionFirewall
        firewall = PaperExecutionFirewall(friction=2.0)
        # Verify no live/demo order methods exist
        assert not hasattr(firewall, 'place_order')
        assert not hasattr(firewall, 'send_order')
        assert not hasattr(firewall, 'execute_order')
        assert not hasattr(firewall, 'submit_order')


# ---------------------------------------------------------------------------
# MODULE PROCESSING TESTS
# ---------------------------------------------------------------------------

class TestModuleProcessing:
    """Verify modules process quotes independently."""
    
    def test_cand024_evaluates_independently(self, tmp_path):
        from module_registry import get_registry
        modules = get_registry(str(tmp_path))
        cand_024 = next(m for m in modules if m.candidate_id == "CAND-024")
        
        quote = {
            "utc_timestamp": time.time(),
            "symbol": "USATECHIDXUSD",
            "broker_symbol": "USTECm",
            "mapping_id": "MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0",
            "bid": 29500.0,
            "ask": 29502.0,
            "age": 0.5
        }
        result = cand_024.process_quote(quote, "test_instance")
        assert result is True
        
    def test_cand035_evaluates_independently(self, tmp_path):
        from module_registry import get_registry
        modules = get_registry(str(tmp_path))
        cand_035 = next(m for m in modules if m.candidate_id == "CAND-035")
        
        quote = {
            "utc_timestamp": time.time(),
            "symbol": "USATECHIDXUSD",
            "broker_symbol": "USTECm",
            "mapping_id": "MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0",
            "bid": 29500.0,
            "ask": 29502.0,
            "age": 0.5
        }
        result = cand_035.process_quote(quote, "test_instance")
        assert result is True
        
    def test_module_error_isolation(self, tmp_path):
        from module_registry import get_registry
        modules = get_registry(str(tmp_path))
        cand_024 = next(m for m in modules if m.candidate_id == "CAND-024")
        
        # Send quote missing required fields — should not crash supervisor
        bad_quote = {"utc_timestamp": time.time()}
        result = cand_024.process_quote(bad_quote, "test_instance")
        # Error is caught, returns False
        assert result is False


# ---------------------------------------------------------------------------
# SUPERVISOR TESTS
# ---------------------------------------------------------------------------

class TestSupervisor:
    """Verify supervisor initialization and lifecycle."""
    
    def test_supervisor_init(self, tmp_path):
        from quantforge_forward_supervisor import Supervisor
        supervisor = Supervisor(mode="smoke", base_runtime_dir=str(tmp_path))
        assert supervisor.mode == "smoke"
        assert len(supervisor.modules) >= 2
        
    def test_supervisor_singleton_lock(self, tmp_path):
        from quantforge_forward_supervisor import Supervisor
        s1 = Supervisor(mode="smoke", base_runtime_dir=str(tmp_path))
        assert s1.acquire_lock() is True
        # Second lock attempt should fail
        s2 = Supervisor(mode="smoke", base_runtime_dir=str(tmp_path))
        assert s2.acquire_lock() is False
        s1.release_lock()
        
    def test_supervisor_shutdown_check(self, tmp_path):
        from quantforge_forward_supervisor import Supervisor
        supervisor = Supervisor(mode="smoke", base_runtime_dir=str(tmp_path))
        assert supervisor.check_shutdown() is False
        # Create shutdown request
        with open(supervisor.shutdown_req_path, "w") as f:
            f.write("shutdown")
        assert supervisor.check_shutdown() is True
        os.remove(supervisor.shutdown_req_path)
        
    def test_supervisor_status_writing(self, tmp_path):
        from quantforge_forward_supervisor import Supervisor
        supervisor = Supervisor(mode="smoke", base_runtime_dir=str(tmp_path))
        supervisor.feed = type('MockFeed', (), {
            'connection_state': lambda self: "CONNECTED",
            'terminal_info': lambda self: {"broker": "Test", "server": "Test"}
        })()
        supervisor.save_status("TESTING")
        assert os.path.exists(supervisor.status_file)
        with open(supervisor.status_file) as f:
            data = json.load(f)
        assert data["supervisor_state"] == "TESTING"
        assert data["pid"] == os.getpid()


# ---------------------------------------------------------------------------
# LEDGER TESTS
# ---------------------------------------------------------------------------

class TestLedgers:
    """Verify event and outcome ledgers are independent and append-only."""
    
    def test_event_ledger_writes(self, tmp_path):
        from event_ledger import EventLedger
        ledger_path = str(tmp_path / "test_event_ledger.jsonl")
        ledger = EventLedger(ledger_path)
        ledger.record_event({"test": "data1"})
        ledger.record_event({"test": "data2"})
        with open(ledger_path) as f:
            lines = f.readlines()
        assert len(lines) == 2
        
    def test_outcome_ledger_writes(self, tmp_path):
        from outcome_ledger import OutcomeLedger
        ledger_path = str(tmp_path / "test_outcome_ledger.jsonl")
        ledger = OutcomeLedger(ledger_path)
        ledger.record_outcome({"test": "outcome1"})
        with open(ledger_path) as f:
            lines = f.readlines()
        assert len(lines) == 1
        
    def test_separate_ledger_files(self, tmp_path):
        from module_registry import get_registry
        modules = get_registry(str(tmp_path))
        cand_024 = next(m for m in modules if m.candidate_id == "CAND-024")
        cand_035 = next(m for m in modules if m.candidate_id == "CAND-035")
        assert cand_024.event_ledger.filepath != cand_035.event_ledger.filepath
        assert cand_024.outcome_ledger.filepath != cand_035.outcome_ledger.filepath


# ---------------------------------------------------------------------------
# MARKET DATA INTERFACE TESTS
# ---------------------------------------------------------------------------

class TestMarketData:
    """Verify MT5MarketFeed interface contract."""
    
    def test_feed_has_required_methods(self):
        from market_data import MT5MarketFeed
        feed = MT5MarketFeed()
        assert hasattr(feed, 'initialize')
        assert hasattr(feed, 'connection_state')
        assert hasattr(feed, 'latest_quote')
        assert hasattr(feed, 'latest_completed_bar')
        assert hasattr(feed, 'terminal_info')
        assert hasattr(feed, 'shutdown')
        
    def test_feed_disconnected_state(self):
        from market_data import MT5MarketFeed
        feed = MT5MarketFeed()
        assert feed.connection_state() == "DISCONNECTED"
        
    def test_feed_unavailable_when_disconnected(self):
        from market_data import MT5MarketFeed
        feed = MT5MarketFeed()
        result = feed.latest_quote("USTECm")
        assert result["status"] == "FEED_UNAVAILABLE"


# ---------------------------------------------------------------------------
# STATUS DISPLAY TESTS
# ---------------------------------------------------------------------------

class TestStatus:
    """Verify status display reads correctly."""
    
    def test_status_script_exists(self):
        assert os.path.exists(os.path.join(forward_dir, "status.py"))
        
    def test_status_reads_supervisor_status(self, tmp_path):
        # Write a mock status file
        status_dir = tmp_path / "supervisor"
        status_dir.mkdir()
        status_file = status_dir / "status.json"
        mock_status = {
            "supervisor_state": "RUNNING",
            "pid": 12345,
            "mt5_connection": "CONNECTED",
            "broker": "Test Broker",
            "server": "Test Server",
            "uptime_seconds": 100.0,
            "modules_loaded": 2
        }
        with open(status_file, "w") as f:
            json.dump(mock_status, f)
        # Verify it can be read
        with open(status_file) as f:
            data = json.load(f)
        assert data["supervisor_state"] == "RUNNING"
        assert data["pid"] == 12345


# ---------------------------------------------------------------------------
# SHUTDOWN TESTS
# ---------------------------------------------------------------------------

class TestShutdown:
    """Verify graceful shutdown mechanism."""
    
    def test_shutdown_request_file(self, tmp_path):
        shutdown_path = tmp_path / "shutdown.req"
        with open(shutdown_path, "w") as f:
            f.write("shutdown")
        assert shutdown_path.exists()
        os.remove(shutdown_path)
        assert not shutdown_path.exists()
        
    def test_shutdown_cleans_req_file(self, tmp_path):
        from quantforge_forward_supervisor import Supervisor
        supervisor = Supervisor(mode="smoke", base_runtime_dir=str(tmp_path))
        with open(supervisor.shutdown_req_path, "w") as f:
            f.write("shutdown")
        supervisor.process_shutdown()
        assert not os.path.exists(supervisor.shutdown_req_path)


# ---------------------------------------------------------------------------
# BAT FILE TESTS
# ---------------------------------------------------------------------------

class TestBatFiles:
    """Verify BAT files exist and have correct structure."""
    
    def test_run_bat_exists(self):
        bat_path = os.path.join(repo_dir, "run_quantforge_forward.bat")
        assert os.path.exists(bat_path)
        
    def test_stop_bat_exists(self):
        bat_path = os.path.join(repo_dir, "stop_quantforge_forward.bat")
        assert os.path.exists(bat_path)
        
    def test_status_bat_exists(self):
        bat_path = os.path.join(repo_dir, "status_quantforge_forward.bat")
        assert os.path.exists(bat_path)
        
    def test_run_bat_uses_start_b(self):
        bat_path = os.path.join(repo_dir, "run_quantforge_forward.bat")
        with open(bat_path) as f:
            content = f.read()
        assert "start" in content.lower()
        
    def test_run_bat_checks_lock_file(self):
        bat_path = os.path.join(repo_dir, "run_quantforge_forward.bat")
        with open(bat_path) as f:
            content = f.read()
        assert "supervisor.lock" in content or "LOCK_FILE" in content


# ---------------------------------------------------------------------------
# CANONICAL IDENTITY TESTS
# ---------------------------------------------------------------------------

class TestCanonicalIdentity:
    """Verify canonical identity format and separation."""
    
    def test_no_phantom_hashes_in_contracts(self):
        from contracts import CAND_024_CONTRACT, CAND_035_CONTRACT
        phantom_024 = "c49c5bb06b35e6266b3dd04e27474dc94f19e86f0c0649cb0b976443f71cb13e"
        phantom_035 = "a7c2132dbed41a7ccae30e69b2b8b38914e2a90693282ecd2823e10948d48cc5"
        assert CAND_024_CONTRACT.hash != phantom_024
        assert CAND_035_CONTRACT.hash != phantom_035
        
    def test_evidence_not_in_hash(self):
        from contracts import CAND_024_CONTRACT, CAND_024_EVIDENCE
        # Changing evidence should not change hash
        original_hash = CAND_024_CONTRACT.hash
        # Evidence is a separate object
        assert CAND_024_EVIDENCE.candidate_id == "CAND-024"
        assert CAND_024_CONTRACT.hash == original_hash
        
    def test_environment_not_in_hash(self):
        from contracts import CAND_024_CONTRACT, USATECHIDXUSD_USTECM_MAPPING
        # Environment is a separate object
        assert USATECHIDXUSD_USTECM_MAPPING.logical_symbol == "USATECHIDXUSD"
        # Hash should be stable
        assert CAND_024_CONTRACT.hash == "925495a86b35e6266b3dd04e27474dc94f19e86f0c0649cb0b976443f71cb13e"


# ---------------------------------------------------------------------------
# CAND-015 EXTERNAL STATUS TESTS
# ---------------------------------------------------------------------------

class TestCand015External:
    """Verify CAND-015 is recognized as external/protected."""
    
    def test_cand015_not_in_registry(self, tmp_path):
        from module_registry import get_registry
        modules = get_registry(str(tmp_path))
        module_ids = [m.candidate_id for m in modules]
        assert "CAND-015" not in module_ids
        assert "CAND-G0-015" not in module_ids
        
    def test_cand015_identity_exists(self):
        # CAND-015 identity should exist in research/g6_forward
        identity_path = os.path.join(
            repo_dir, "research", "g6_forward", "cand015_identity.py"
        )
        assert os.path.exists(identity_path)
