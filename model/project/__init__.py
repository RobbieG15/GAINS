import json
from datetime import datetime
from typing import Any, Type, TypeVar
from uuid import uuid4
from zoneinfo import ZoneInfo

T = TypeVar("T", bound="Serializable")


class Serializable:
    def to_dict(self) -> dict[str, Any]:
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Serializable):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [
                    item.to_dict() if isinstance(item, Serializable) else item
                    for item in value
                ]
            else:
                result[key] = value
        return result

    def to_json(self, **kwargs) -> str:
        return json.dumps(self.to_dict(), **kwargs)

    @classmethod
    def from_dict(cls: Type[T], data: dict[str, Any]) -> T:
        obj = cls.__new__(cls)  # create instance without calling __init__
        for key, value in data.items():
            attr = getattr(cls, key, None)
            if isinstance(value, dict) and hasattr(attr, "from_dict"):
                # If attr is a Serializable subclass, use its from_dict
                setattr(obj, key, attr.from_dict(value))
            elif isinstance(value, list):
                # Check if list items are dicts that should be deserialized
                new_list = []
                for item in value:
                    if isinstance(item, dict):
                        # Try to find the right class to deserialize, fallback to dict
                        # This requires some hint, here we just keep dict
                        new_list.append(item)
                    else:
                        new_list.append(item)
                setattr(obj, key, new_list)
            else:
                setattr(obj, key, value)
        return obj

    @classmethod
    def from_json(cls: Type[T], json_str: str) -> T:
        data = json.loads(json_str)
        return cls.from_dict(data)


class ProjectObject(Serializable):
    def __init__(self, name: str, object_id: str = None):
        self.name = name
        self.id = object_id or str(uuid4())
        self.created_at = datetime.now(ZoneInfo("America/New_York")).isoformat(
            timespec="seconds"
        )
