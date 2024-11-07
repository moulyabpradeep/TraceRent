from dataclasses import dataclass
from typing import Optional
import json


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

    @staticmethod
    def from_json(json_str: str) -> 'UserData':
        data = json.loads(json_str)
        return UserData(**data)


@dataclass
class PropertyObject:
    property_price: Optional[int] = None
    property_coordinates: Optional[tuple] = None
    school_proximity: Optional[int] = None
    hospital_proximity: Optional[int] = None
    transit_proximity: Optional[int] = None
    in_house_laundry: Optional[bool] = None
    gym: Optional[bool] = None
    pet_friendly: Optional[bool] = None
    pool: Optional[bool] = None
    points: Optional[int] = None
    percent_close: Optional[int] = None
    distance: Optional[int] = None
    school_proximity_points: Optional[int] = None
    hospital_proximity_points: Optional[int] = None
    transit_proximity_points: Optional[int] = None
    max_points: Optional[int] = None

    @staticmethod
    def from_json(json_str: str) -> 'PropertyObject':
        data = json.loads(json_str)
        return PropertyObject(**data)
