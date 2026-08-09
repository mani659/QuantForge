import os

with open('boe/science/science_errors.py', 'a', encoding='utf-8') as f:
    f.write('''
class ValidationServiceError(ScienceError):
    """Base exception for ValidationService related errors."""
    pass

class InvalidServiceOperation(ValidationServiceError):
    """Raised when a validation service operation violates lifecycle rules or linkage constraints."""
    pass
''')
