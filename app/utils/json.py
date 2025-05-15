import json
from bson import ObjectId
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from fastapi.responses import JSONResponse as FastAPIJSONResponse


class MongoJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that can handle MongoDB ObjectId and datetime."""
    
    def default(self, obj: Any) -> Any:
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def mongo_json_dumps(obj: Any) -> str:
    """JSON dumps with MongoDB object support."""
    return json.dumps(obj, cls=MongoJSONEncoder)


class JSONResponse(FastAPIJSONResponse):
    """Custom JSONResponse that uses MongoJSONEncoder by default."""
    
    def render(self, content: Any) -> bytes:
        return mongo_json_dumps(content).encode("utf-8")