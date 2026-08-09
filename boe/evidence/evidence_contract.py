from abc import ABC

class EvidenceContract(ABC):
    """
    Abstract contract for scientific evidence.
    
    All Evidence instances must fulfill this contract, ensuring they expose
    only abstract information without leaking implementation details.
    """
    
    evidence_id: str
    candidate_id: str
    timeline_id: str
