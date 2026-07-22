import numpy as np
from pathlib import Path
from datetime import datetime, date
from uuid import UUID
from enum import Enum
import dataclasses

def serialize_result(obj):
    """
    Recursively serialize numpy arrays, Path, datetime, UUID, dataclasses, and Enums
    into standard JSON-safe Python primitives.
    """
    if isinstance(obj, dict):
        # Filter out heavy raw image arrays ('image', 'roi') to prevent database bloat
        return {str(k): serialize_result(v) for k, v in obj.items() if k not in ("image", "roi")}
    elif isinstance(obj, (list, tuple, set)):
        return [serialize_result(item) for item in obj]
    elif isinstance(obj, np.ndarray):
        return serialize_result(obj.tolist())
    elif isinstance(obj, np.generic):
        return obj.item()
    elif isinstance(obj, Path):
        return str(obj)
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, UUID):
        return str(obj)
    elif isinstance(obj, Enum):
        return obj.value
    elif dataclasses.is_dataclass(obj):
        return serialize_result(dataclasses.asdict(obj))
    elif hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
        return serialize_result(obj.to_dict())
    else:
        return obj
