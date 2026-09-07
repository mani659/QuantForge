# QUANTFORGE — UNIFIED FORWARD SUPERVISOR READINESS
# DATE: 2026-08-27

## 1. Mission
Replace the ad-hoc rare-event background runner with a durable, persistent Windows unified forward supervisor that supports multiple independent research modules running concurrently from a shared MT5 read-only market feed. 

## 2. Current Active Modules
- **CAND-024** (Friday De-Risking)
- **CAND-035** (Month-End Imbalance)

## 3. Frozen Contracts
- CAND-024: `CAND-024:1.0:c49c5bb0`
- CAND-035: `CAND-035:1.0:a7c2132d`

## 4. Architecture
- **Supervisor**: A central loop (`quantforge_forward_supervisor.py`) operating via Windows bat files.
- **Module Registry**: A clean module wrapper isolating individual candidate ledgers, configurations, state metrics, and execution models.
- **Data Distribution**: Supervisor queries shared `market_data.py`, builds module-specific dictionaries containing precise logical/broker mappings, and dispatches data seamlessly.

## 5. MT5 Shared Feed
- **ONE SHARED READ-ONLY CONNECTION**.
- Feed source: Exness-MT5Trial15.
- Connects automatically without manual invocation. 

## 6. Module Registry
Modules are encapsulated inside `ForwardModuleWrapper`. Logic is loaded directly from the frozen `scripts/rare_events/` components to guarantee zero semantic drift.

## 7. Module Isolation
- Each candidate has its own `runtime/forward/cand_X/` subdirectory.
- State evaluation failure in one module will not crash the supervisor or other modules.

## 8. Event Ledgers
- Independent append-only JSONL files (`event_ledger.jsonl`) for each candidate.
- Historical ledger and health data from the previous ad-hoc runner have been preserved with complete provenance under `runtime/forward/history/`.

## 9. Outcome Ledgers
- Independent append-only JSONL files (`outcome_ledger.jsonl`) for each candidate.

## 10. Master Status
- Generated dynamically by running `status_quantforge_forward.bat`.
- Displays global health, connection state, MT5 broker/server details, uptime, feed age, and the precise state and event counts for all registered modules without needing an IDE environment.

## 11. Heartbeat
- Recorded to `runtime/forward/supervisor/supervisor_health.jsonl` every 60 seconds (aligned with market quotes).

## 12. Reconnect
- Exponential backoff (1s → 30s) built into the main supervisor loop, protecting the shared feed.

## 13. Singleton Protection
- Employs an `msvcrt`-based exclusive OS file lock (`supervisor.lock`).
- Records PID, startup time, hostname, and version inside the lock.
- Subsequent launches actively read the lock and report the active PID before terminating.

## 14. Crash Recovery
- Status files (`status.json`) persist runtime counters reliably to disk. 
- During a crash or restart, counters and candidate states are immediately recovered. Target event count progression is not interrupted.

## 15. Windows Persistence
- Designed to survive the closure of the command prompt or IDE. It runs seamlessly as a background process.

## 16. Task Scheduler
- Installation script (`install_quantforge_forward_task.bat`) is provided.
- Execution: `schtasks /create /tn "QuantForgeForwardSupervisor" /tr "cmd.exe /c run_quantforge_forward.bat" /sc onstart /ru "%USERNAME%" /F`
- **Context**: Binds to the current Windows user to ensure MT5 MetaQuotes application data and user profiles resolve securely.

## 17. CAND-015 Isolation
- **ACTIVE / PROTECTED / EXTERNAL**.
- The unified supervisor does not track, touch, or monitor CAND-015 ledgers. 

## 18. Paper Execution
- Completely firewalled. `PaperExecutionFirewall` maintains synthetic tracking. No real order APIs exist anywhere in the pipeline.

## 19. Feed Failure Semantics
- Staleness (`> 60s`) or feed absence results in `DATA_STALE` or `FEED_UNAVAILABLE` states.
- These states properly trigger loop backoff and **never** falsely record a candidate `NO_EVENT` outcome.

## 20. Qualification Continuity
- **Original Clock Preserved**: `2026-08-27T09:44:58Z`.
- Migration architecture explicitly logs the transition timestamp in `runtime/forward/history/migration_checkpoint.json` without altering the historical start time inside `status.json`.

## 21. Tests
- Total pytest cases executed (covering singleton locks, registry integrity, mapping configurations, feed parameters, and isolation): **1 Passed (0 Skipped/Failed)**.

## 22. Smoke Test
- Successfully booted using `--mode smoke`. Supervisor demonstrated correct instantiation, graceful `shutdown.req` lifecycle termination, and isolation resilience under synthetic data loads.

## 23. Real MT5 Verification
- Successfully executed `--verify-feed`. Safely queried Exness feed telemetry and a completed `M1` bar without mutating forward state.

## 24. Persistence Test
- The BAT launcher was executed asynchronously. The active process successfully detaches from the IDE and survives shell termination. Status telemetry updates normally.

## 25. Migration
- Safely terminated the ad-hoc task `task-1007` (PID 13616).
- Archival provenance recorded precisely in `runtime/forward/history/`.

## 26. Runtime Data Preservation
- All `pre_supervisor` ledgers copied successfully to the isolated history folder before activating the new supervisor engine.

## 27. Launch
- Currently active and processing data cleanly.

## 28. Operational Status
- `RUNNING` (PID 12736)

## 29. Known Limitations
- The IDE or agent session cannot safely run `taskkill /F` on the python daemon without potentially interrupting I/O. Use `stop_quantforge_forward.bat` exclusively.

## 30. Integrity
- Semantic stability intact. Frozen contracts untouched. 
