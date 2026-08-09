import unittest
from datetime import datetime

from boe.science import (
    Hypothesis,
    HypothesisStatus,
    InvalidHypothesisData
)

class TestHypothesisContract(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        
    def test_immutable_construction_and_equality(self):
        h1 = Hypothesis(
            identifier="HYP-001",
            title="Mean Reversion on SPX",
            description="Testing MR on S&P 500",
            author="Researcher A",
            created_timestamp=self.dt,
            status=HypothesisStatus.DRAFT
        )
        
        h2 = Hypothesis(
            identifier="HYP-001",
            title="Mean Reversion on SPX",
            description="Testing MR on S&P 500",
            author="Researcher A",
            created_timestamp=self.dt,
            status=HypothesisStatus.DRAFT
        )
        
        self.assertEqual(h1.identifier, "HYP-001")
        self.assertEqual(h1.status, HypothesisStatus.DRAFT)
        
        # Test equality and hashing
        self.assertEqual(h1, h2)
        self.assertEqual(hash(h1), hash(h2))
        
        # Test immutability
        with self.assertRaises(Exception): # FrozenInstanceError
            h1.identifier = "HYP-002" # type: ignore

    def test_invalid_values(self):
        with self.assertRaises(InvalidHypothesisData):
            Hypothesis(
                identifier="",
                title="Title",
                description="Desc",
                author="Author",
                created_timestamp=self.dt,
                status=HypothesisStatus.DRAFT
            )
            
        with self.assertRaises(InvalidHypothesisData):
            Hypothesis(
                identifier="HYP-001",
                title="",
                description="Desc",
                author="Author",
                created_timestamp=self.dt,
                status=HypothesisStatus.DRAFT
            )
            
        with self.assertRaises(InvalidHypothesisData):
            Hypothesis(
                identifier="HYP-001",
                title="Title",
                description=" ",
                author="Author",
                created_timestamp=self.dt,
                status=HypothesisStatus.DRAFT
            )
            
        with self.assertRaises(InvalidHypothesisData):
            Hypothesis(
                identifier="HYP-001",
                title="Title",
                description="Desc",
                author=" ",
                created_timestamp=self.dt,
                status=HypothesisStatus.DRAFT
            )
            
        with self.assertRaises(InvalidHypothesisData):
            Hypothesis(
                identifier="HYP-001",
                title="Title",
                description="Desc",
                author="Author",
                created_timestamp="Not a datetime", # type: ignore
                status=HypothesisStatus.DRAFT
            )

    def test_status_validation(self):
        with self.assertRaises(InvalidHypothesisData):
            Hypothesis(
                identifier="HYP-001",
                title="Title",
                description="Desc",
                author="Author",
                created_timestamp=self.dt,
                status="INVALID_STATUS" # type: ignore
            )
            
        # Valid statuses should work
        for status in HypothesisStatus:
            h = Hypothesis(
                identifier="HYP-001",
                title="Title",
                description="Desc",
                author="Author",
                created_timestamp=self.dt,
                status=status
            )
            self.assertEqual(h.status, status)

if __name__ == '__main__':
    unittest.main()
