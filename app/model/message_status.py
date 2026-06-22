from enum import Enum

class MessageStatus(Enum):
    PROCESSING = "processing"
    PROCESSED = "processed"
    UNPROCESSED = "unprocessed"