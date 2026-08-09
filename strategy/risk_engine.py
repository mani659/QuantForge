"""
QuantForge Risk Engine (v1.0.0)

Evaluates strategy, signal, and account inputs to produce a deterministic
Milestone 1 trade plan. This module does not calculate lot sizes, stop losses,
take profits, or place orders.
"""

import json
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional


class RiskEngine:
    """Applies configured account-protection rules to a proposed trade."""

    def __init__(self, config_path: Optional[Path] = None) -> None:
        self.config_path = Path(config_path) if config_path else self._default_config_path()
        self.rules = self._load_rules()

    @staticmethod
    def _default_config_path() -> Path:
        """Returns the risk configuration path relative to the project root."""
        return Path(__file__).resolve().parents[1] / "config" / "risk_rules.json"

    def _load_rules(self) -> Dict[str, Any]:
        """Loads and validates the external risk-rule configuration."""
        if not self.config_path.is_file():
            raise FileNotFoundError(
                f"Risk rules configuration was not found: {self.config_path}"
            )

        try:
            with self.config_path.open("r", encoding="utf-8") as config_file:
                rules = json.load(config_file)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"Risk rules configuration contains invalid JSON: {self.config_path}"
            ) from error

        required_rules = {
            "base_risk_percent",
            "low_risk_multiplier",
            "medium_risk_multiplier",
            "high_risk_multiplier",
            "minimum_signal_confidence",
            "minimum_strategy_confidence",
            "maximum_daily_loss_percent",
            "maximum_drawdown_percent",
            "maximum_open_positions",
            "maximum_consecutive_losses",
        }
        missing_rules = required_rules.difference(rules)
        if missing_rules:
            raise ValueError(
                "Risk rules configuration is missing required entries: "
                f"{', '.join(sorted(missing_rules))}"
            )

        return rules

    def create_trade_plan(
        self,
        adaptive_strategy: Dict[str, Any],
        signal: Dict[str, Any],
        account: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Returns the approval decision and risk allocation for a proposed trade."""
        self._validate_inputs(adaptive_strategy, signal, account)

        reasons: List[str] = []
        rejection_reasons = self._get_rejection_reasons(
            adaptive_strategy, signal, account
        )
        trade_allowed = not rejection_reasons
        risk_percent = 0.0
        risk_dollars = 0.0
        if trade_allowed:
            risk_profile = str(adaptive_strategy["risk_profile"]).lower()
            risk_percent = self.rules["base_risk_percent"] * self.rules[
                f"{risk_profile}_risk_multiplier"
            ]
            risk_dollars = account["balance"] * (risk_percent / 100)
            reasons.extend(
                [
                    "Trade Approved",
                    "Signal confidence acceptable",
                    "Strategy confidence acceptable",
                    "Daily loss within limit",
                    "Drawdown within limit",
                    "Open position count acceptable",
                    "Consecutive losses within limit",
                    f"Risk profile {adaptive_strategy['risk_profile']}",
                ]
            )
        else:
            reasons.extend(["Trade Rejected", *rejection_reasons])

        return self._build_trade_plan(
            adaptive_strategy=adaptive_strategy,
            signal=signal,
            account=account,
            trade_allowed=trade_allowed,
            risk_percent=round(risk_percent, 2),
            risk_dollars=round(risk_dollars, 2),
            reasons=reasons,
        )

    def _build_trade_plan(
        self,
        adaptive_strategy: Dict[str, Any],
        signal: Dict[str, Any],
        account: Dict[str, Any],
        trade_allowed: bool,
        risk_percent: float,
        risk_dollars: float,
        reasons: List[str],
    ) -> Dict[str, Any]:
        """Wraps the existing Milestone 1 decision in the frozen TradePlan schema."""
        timestamp = signal.get("timestamp")
        trade_plan_timestamp = timestamp.replace(" ", "T") if isinstance(timestamp, str) else None
        identity_data = {
            "strategy": adaptive_strategy,
            "signal": signal,
            "account": account,
        }
        plan_id = "trade_" + hashlib.sha256(
            json.dumps(identity_data, sort_keys=True, default=str).encode("utf-8")
        ).hexdigest()[:12]
        decision_status = "Approved" if trade_allowed else "Rejected"

        return {
            "schema_version": "1.0",
            "plan_id": plan_id,
            "timestamp": trade_plan_timestamp,
            "instrument": adaptive_strategy.get("instrument"),
            "timeframe": signal.get("timeframe"),
            "direction": signal["signal"],
            "trade_allowed": trade_allowed,
            "strategy": {
                "class": adaptive_strategy.get("strategy_class"),
                "holding_style": adaptive_strategy.get("holding_style"),
                "confidence": adaptive_strategy["confidence"],
            },
            "signal": {
                "strength": signal["signal_strength"],
                "confidence": signal["confidence"],
                "reason": signal.get("reason", []),
            },
            "risk": {
                "risk_profile": adaptive_strategy["risk_profile"],
                "risk_percent": risk_percent,
                "risk_dollars": risk_dollars,
            },
            "execution": {
                "lot_size": None,
                "stop_distance": None,
                "take_profit_distance": None,
                "risk_reward": 2.0,
            },
            "validation": {
                "daily_loss_ok": account["daily_loss_percent"] < self.rules["maximum_daily_loss_percent"],
                "drawdown_ok": account["drawdown_percent"] < self.rules["maximum_drawdown_percent"],
                "spread_ok": None,
                "session_ok": None,
                "exposure_ok": account["open_positions"] < self.rules["maximum_open_positions"],
            },
            "decision_trace": {
                "strategy": decision_status,
                "signal": decision_status,
                "risk": decision_status,
                "execution": "Pending",
            },
            "metadata": {
                "adaptive_version": "1.0.1",
                "signal_version": "1.0.0",
                "risk_version": "1.0.0",
            },
            # Legacy Milestone 1 fields are retained for existing callers.
            "risk_percent": risk_percent,
            "risk_dollars": risk_dollars,
            "reason": reasons,
        }

    def _get_rejection_reasons(
        self,
        adaptive_strategy: Dict[str, Any],
        signal: Dict[str, Any],
        account: Dict[str, Any],
    ) -> List[str]:
        """Evaluates every configured rejection rule in a stable order."""
        reasons: List[str] = []

        if str(signal["signal"]).upper() == "NO_TRADE":
            reasons.append("Signal is NO_TRADE")
        if signal["confidence"] < self.rules["minimum_signal_confidence"]:
            reasons.append("Signal confidence below threshold")
        if adaptive_strategy["confidence"] < self.rules["minimum_strategy_confidence"]:
            reasons.append("Strategy confidence below threshold")
        if account["daily_loss_percent"] >= self.rules["maximum_daily_loss_percent"]:
            reasons.append("Maximum daily loss exceeded")
        if account["drawdown_percent"] >= self.rules["maximum_drawdown_percent"]:
            reasons.append("Maximum drawdown exceeded")
        if account["open_positions"] >= self.rules["maximum_open_positions"]:
            reasons.append("Maximum open positions reached")
        if account["consecutive_losses"] >= self.rules["maximum_consecutive_losses"]:
            reasons.append("Maximum consecutive losses reached")

        return reasons

    @staticmethod
    def _validate_inputs(
        adaptive_strategy: Dict[str, Any],
        signal: Dict[str, Any],
        account: Dict[str, Any],
    ) -> None:
        """Ensures all required Milestone 1 input values are available."""
        required_fields = {
            "adaptive strategy": (adaptive_strategy, {"risk_profile", "confidence"}),
            "signal": (signal, {"signal", "signal_strength", "confidence"}),
            "account": (
                account,
                {
                    "balance",
                    "equity",
                    "daily_loss_percent",
                    "drawdown_percent",
                    "open_positions",
                    "consecutive_losses",
                },
            ),
        }
        for input_name, (input_data, fields) in required_fields.items():
            missing_fields = fields.difference(input_data)
            if missing_fields:
                raise ValueError(
                    f"Missing required {input_name} fields: "
                    f"{', '.join(sorted(missing_fields))}"
                )

        risk_profile = str(adaptive_strategy["risk_profile"]).lower()
        if risk_profile not in {"low", "medium", "high"}:
            raise ValueError("Risk profile must be one of: Low, Medium, High")
