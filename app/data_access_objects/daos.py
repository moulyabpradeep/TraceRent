from dataclasses import dataclass
import json
from pydantic import BaseModel
from typing import Optional, Union
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
    name_of_user: Optional[str] = None
    user_email: Optional[str] = None
    user_phone: Optional[str] = None
    user_password: Optional[str] = None
    session_id: Optional[str] = None
    user_id: Optional[int] = None

    @staticmethod
    def from_json(data: Union[str, dict]) -> 'UserData':
        # If data is a JSON string, parse it to a dictionary
        if isinstance(data, str):
            data = json.loads(data)

        # Return an instance of UserData, using ** to unpack dictionary values
        return UserData(
            name_of_user=data.get('name_of_user'),
            user_email=data.get('user_email'),
            user_phone=data.get('user_phone'),
            user_password=data.get('user_password'),
            session_id=data.get('session_id'),
            user_id=data.get('user_id')
        )



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

    @classmethod
    def get_by_value(cls, value: str):
        """Return the enum member for a given value."""
        try:
            return cls[value.upper()]  # Ensure the value is case-insensitive
        except KeyError:
            raise ValueError(f"{value} is not a valid TenantActionFilterType.")