from dataclasses import dataclass
import json
from pydantic import BaseModel
from typing import Optional
from enum import Enum


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


class TenantActionsData(BaseModel):
    unit_id: int
    is_logged_in: bool
    user_id: int
    is_viewed: Optional[bool] = False
    is_liked: Optional[bool] = False
    is_contacted: Optional[bool] = False
    
    @staticmethod
    def from_json(action_data_json: dict):
        # Optional preprocessing or validation logic
        return TenantActionsData(**action_data_json)


class TenantActionFilterType(Enum):
    LIKED = "LIKED"
    DISLIKED = "DISLIKED"
    CONTACTED = "CONTACTED"

