import unittest
from datetime import datetime
from types import MappingProxyType
from dataclasses import FrozenInstanceError

from boe.risk.position_sizer import PositionSizingResult
from boe.risk.specification import PositionSpecification
from boe.risk.risk_errors import (
    InvalidPositionSpecification,
    InvalidSizingOutput,
    PositionSpecificationConstructionError
)

class TestPositionSpecification(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        self.metadata = MappingProxyType({"sizer": "DefaultPositionSizer_v1.0"})
        
        self.sizing_result = PositionSizingResult(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="o_1",
            schema_version="1.0",
            risk_units=1.0,
            exposure_fraction=0.01,
            position_size_multiplier=1.0,
            metadata=self.metadata,
            timestamp=self.dt
        )

    def test_immutable_construction_from_sizing_result(self):
        spec = PositionSpecification.from_sizing_result(self.sizing_result, self.dt)
        self.assertEqual(spec.candidate_id, "c_1")
        self.assertEqual(spec.exposure_fraction, 0.01)
        self.assertEqual(spec.metadata["source_sizer"], "DefaultPositionSizer_v1.0")

        with self.assertRaises(FrozenInstanceError):
            spec.exposure_fraction = 0.5 # type: ignore

    def test_missing_sizing_result_error(self):
        with self.assertRaises(InvalidSizingOutput):
            PositionSpecification.from_sizing_result(None, self.dt) # type: ignore

    def test_repeatability_and_hashing(self):
        spec1 = PositionSpecification.from_sizing_result(self.sizing_result, self.dt)
        spec2 = PositionSpecification.from_sizing_result(self.sizing_result, self.dt)
        
        self.assertEqual(spec1, spec2)
        self.assertEqual(hash(spec1), hash(spec2))

    def test_schema_validation_and_errors(self):
        with self.assertRaises(InvalidPositionSpecification):
            PositionSpecification(
                candidate_id="",
                timeline_id="t",
                observation_id="o",
                schema_version="1",
                position_size_multiplier=1.0,
                exposure_fraction=1.0,
                risk_units=1.0,
                metadata=self.metadata,
                timestamp=self.dt
            )
            
        with self.assertRaises(InvalidPositionSpecification):
            PositionSpecification(
                candidate_id="c",
                timeline_id="t",
                observation_id="o",
                schema_version="1",
                position_size_multiplier="NOT_NUMERIC", # type: ignore
                exposure_fraction=1.0,
                risk_units=1.0,
                metadata=self.metadata,
                timestamp=self.dt
            )

if __name__ == '__main__':
    unittest.main()
