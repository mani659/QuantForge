import unittest
from datetime import datetime
from types import MappingProxyType
from dataclasses import FrozenInstanceError

from boe.risk.assessment import RiskAssessment, AssessmentStatus
from boe.risk.position_sizer import (
    PositionSizingResult,
    PositionSizerConfig,
    DefaultPositionSizer
)
from boe.risk.risk_errors import (
    PositionSizingError,
    InvalidRiskAssessment
)

class TestPositionSizer(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        self.metadata = MappingProxyType({"source": "test"})
        
        self.assessment_approved = RiskAssessment(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="o_1",
            schema_version="1.0",
            status=AssessmentStatus.APPROVED,
            rationale="Test",
            metadata=self.metadata,
            timestamp=self.dt
        )
        
        self.assessment_reduced = RiskAssessment(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="o_1",
            schema_version="1.0",
            status=AssessmentStatus.REDUCED_EXPOSURE,
            rationale="Test",
            metadata=self.metadata,
            timestamp=self.dt
        )
        
        self.assessment_rejected = RiskAssessment(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="o_1",
            schema_version="1.0",
            status=AssessmentStatus.REJECTED,
            rationale="Test",
            metadata=self.metadata,
            timestamp=self.dt
        )

        self.sizer = DefaultPositionSizer()

    def test_valid_sizing_approved(self):
        result = self.sizer.size_position(self.assessment_approved, self.dt)
        
        self.assertEqual(result.exposure_fraction, 0.01)
        self.assertEqual(result.position_size_multiplier, 1.0)
        self.assertEqual(result.risk_units, 1.0)
        self.assertEqual(result.candidate_id, "c_1")

    def test_valid_sizing_reduced(self):
        result = self.sizer.size_position(self.assessment_reduced, self.dt)
        
        self.assertEqual(result.exposure_fraction, 0.005)
        self.assertEqual(result.position_size_multiplier, 0.5)
        self.assertEqual(result.risk_units, 0.5)

    def test_valid_sizing_rejected(self):
        result = self.sizer.size_position(self.assessment_rejected, self.dt)
        
        self.assertEqual(result.exposure_fraction, 0.0)
        self.assertEqual(result.position_size_multiplier, 0.0)
        self.assertEqual(result.risk_units, 0.0)

    def test_invalid_risk_assessment(self):
        with self.assertRaises(InvalidRiskAssessment):
            self.sizer.size_position(None, self.dt) # type: ignore

    def test_repeatability_and_hashing(self):
        result1 = self.sizer.size_position(self.assessment_approved, self.dt)
        result2 = self.sizer.size_position(self.assessment_approved, self.dt)
        
        self.assertEqual(result1, result2)
        self.assertEqual(hash(result1), hash(result2))

    def test_immutable_outputs_and_config(self):
        result = self.sizer.size_position(self.assessment_approved, self.dt)
        
        with self.assertRaises(FrozenInstanceError):
            result.exposure_fraction = 0.5 # type: ignore
            
        config = PositionSizerConfig()
        with self.assertRaises(FrozenInstanceError):
            config.base_risk_fraction = 0.05 # type: ignore

    def test_schema_validation(self):
        with self.assertRaises(PositionSizingError):
            PositionSizingResult(
                candidate_id="",
                timeline_id="t",
                observation_id="o",
                schema_version="1",
                risk_units=1.0,
                exposure_fraction=0.01,
                position_size_multiplier=1.0,
                metadata=self.metadata,
                timestamp=self.dt
            )
            
        with self.assertRaises(PositionSizingError):
            PositionSizingResult(
                candidate_id="c",
                timeline_id="t",
                observation_id="o",
                schema_version="1",
                risk_units="NOT_NUMERIC", # type: ignore
                exposure_fraction=0.01,
                position_size_multiplier=1.0,
                metadata=self.metadata,
                timestamp=self.dt
            )

if __name__ == '__main__':
    unittest.main()
