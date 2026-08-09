import unittest
from datetime import datetime
from types import MappingProxyType
from dataclasses import FrozenInstanceError

from boe.risk.policy import RiskPolicyEvaluation, RiskPolicyAction
from boe.risk.assessment import RiskAssessment, AssessmentStatus
from boe.risk.risk_errors import (
    InvalidRiskAssessment,
    MissingRiskDecision,
    InvalidAssessmentState
)

class TestRiskAssessment(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        self.metadata = MappingProxyType({"policy": "DefaultRiskPolicy_v1.0"})

        self.evaluation_approve = RiskPolicyEvaluation(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="obs_1",
            schema_version="1.0",
            action=RiskPolicyAction.APPROVE,
            rationale="Approved",
            metadata=self.metadata,
            timestamp=self.dt
        )

        self.evaluation_reduce = RiskPolicyEvaluation(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="obs_1",
            schema_version="1.0",
            action=RiskPolicyAction.REDUCE_EXPOSURE,
            rationale="Reduced",
            metadata=self.metadata,
            timestamp=self.dt
        )

    def test_deterministic_construction_from_evaluation(self):
        assessment = RiskAssessment.from_policy_evaluation(self.evaluation_approve, self.dt)
        self.assertEqual(assessment.status, AssessmentStatus.APPROVED)
        self.assertEqual(assessment.candidate_id, "c_1")
        self.assertEqual(assessment.rationale, "Approved")
        self.assertEqual(assessment.metadata["source_policy"], "DefaultRiskPolicy_v1.0")

        assessment_reduce = RiskAssessment.from_policy_evaluation(self.evaluation_reduce, self.dt)
        self.assertEqual(assessment_reduce.status, AssessmentStatus.REDUCED_EXPOSURE)

    def test_immutable_risk_assessment(self):
        assessment = RiskAssessment.from_policy_evaluation(self.evaluation_approve, self.dt)
        
        with self.assertRaises(FrozenInstanceError):
            assessment.status = AssessmentStatus.REJECTED # type: ignore

    def test_repeatability_and_hashing(self):
        assessment1 = RiskAssessment.from_policy_evaluation(self.evaluation_approve, self.dt)
        assessment2 = RiskAssessment.from_policy_evaluation(self.evaluation_approve, self.dt)
        
        self.assertEqual(assessment1, assessment2)
        self.assertEqual(hash(assessment1), hash(assessment2))

    def test_schema_validation_and_errors(self):
        with self.assertRaises(InvalidRiskAssessment):
            RiskAssessment(
                candidate_id="",
                timeline_id="t",
                observation_id="o",
                schema_version="1",
                status=AssessmentStatus.APPROVED,
                rationale="r",
                metadata=self.metadata,
                timestamp=self.dt
            )
            
        with self.assertRaises(InvalidAssessmentState):
            RiskAssessment(
                candidate_id="c",
                timeline_id="t",
                observation_id="o",
                schema_version="1",
                status="NOT_AN_ENUM", # type: ignore
                rationale="r",
                metadata=self.metadata,
                timestamp=self.dt
            )

    def test_missing_evaluation_error(self):
        with self.assertRaises(MissingRiskDecision):
            RiskAssessment.from_policy_evaluation(None, self.dt) # type: ignore

if __name__ == '__main__':
    unittest.main()
