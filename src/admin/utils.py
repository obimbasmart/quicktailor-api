from enum import Enum

class TailorState(str, Enum):
    VERIFY = 'verify'
    SUSPEND = 'suspend'


