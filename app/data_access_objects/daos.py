from dataclasses import dataclass
import json


@dataclass
class UserPreferences:
    user_id: int
    tenant_category_id: int
    location_category_id: int
    budget_category_id: int
    school_proximity: int
    hospital_proximity: int
    transit_proximity: int
    in_house_laundry: bool
    gym: bool
    pet_friendly: bool
    pool: bool
    is_logged_in: bool
    session_id: str

    @staticmethod
    def from_json(json_str: str) -> 'UserPreferences':
        data = json.loads(json_str)
        return UserPreferences(**data)
    
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
    
