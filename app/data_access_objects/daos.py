from dataclasses import dataclass
import json
from typing import Optional


@dataclass
class UserPreferences:
    city: Optional[str] = None
    user_id: Optional[str] = None
    tenant_category_id: Optional[int] = None
    location_category_id: Optional[int] = None
    budget_category_id: Optional[int] = None
    school_proximity: Optional[int] = None
    hospital_proximity: Optional[int] = None
    transit_proximity: Optional[int] = None
    in_house_laundry: Optional[bool] = None
    gym: Optional[bool] = None
    pet_friendly: Optional[bool] = None
    pool: Optional[bool] = None
    is_logged_in: Optional[bool] = None
    session_id: Optional[str] = None

    @staticmethod
    def from_json(json_data: dict) -> 'UserPreferences':
        return UserPreferences(**json_data)

    
@dataclass
class UserData:
    name_of_user: str
    user_email: str
    user_phone: str
    user_password: str
    session_id: str
    user_id: int

    @staticmethod
    def from_json(json_str: str) -> 'UserData':
        data = json.loads(json_str)
        return UserData(**data)
    
