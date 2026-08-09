class ProfileError(Exception):
    """Base exception for profile errors."""
    pass

class InvalidBehaviourProfile(ProfileError):
    pass

class MissingBehaviourDescriptor(ProfileError):
    pass

class DuplicateBehaviourDescriptor(ProfileError):
    pass

class BehaviourProfileConstructionError(ProfileError):
    pass
