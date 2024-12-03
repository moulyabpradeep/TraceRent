from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import json
from decimal import Decimal


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
class PropertyObject:
    rent: Optional[int] = None
    property_coordinates: Optional[tuple] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
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
    points: Optional[int] = None
    property_media: Optional[List[Dict[str, Any]]] = None  # JSON array of JSON objects

    @staticmethod
    def from_json(json_str: str) -> 'PropertyObject':
        data = json.loads(json_str)
        return PropertyObject(**data)
