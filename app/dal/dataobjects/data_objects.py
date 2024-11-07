from dataclasses import dataclass
import json

@dataclass
class UserData:
    name: str
    email: str
    phone: str
    password: str
    username: str
    user_id: int = None  # Optional, as it will be auto-generated

    @staticmethod
    def from_json(json_str: str) -> 'UserData':
        data = json.loads(json_str)
        return UserData(**data)
