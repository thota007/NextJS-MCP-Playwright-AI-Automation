import json
import os
from typing import Optional
from models import UserData, MHMDPreference

class JSONDataService:
    def __init__(self, data_file: str = "user_data.json"):
        self.data_file = data_file
        self.ensure_data_file_exists()
    
    def ensure_data_file_exists(self):
        """Create the data file if it doesn't exist"""
        if not os.path.exists(self.data_file):
            default_data = {
                "user": {
                    "name": "",
                    "email": "",
                    "mhmd_preference": "OPT_OUT"
                }
            }
            with open(self.data_file, 'w') as f:
                json.dump(default_data, f, indent=2)
    
    def load_data(self) -> dict:
        """Load data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return default data if file doesn't exist or is corrupted
            return {
                "user": {
                    "name": "",
                    "email": "",
                    "mhmd_preference": "OPT_OUT"
                }
            }
    
    def save_data(self, data: dict):
        """Save data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_user_data(self) -> Optional[UserData]:
        """Get user data"""
        data = self.load_data()
        user_data = data.get("user", {})
        
        if not user_data.get("name") or not user_data.get("email"):
            return None
        
        try:
            return UserData(
                name=user_data["name"],
                email=user_data["email"],
                mhmd_preference=MHMDPreference(user_data["mhmd_preference"])
            )
        except Exception:
            return None
    
    def save_user_data(self, user_data: UserData) -> bool:
        """Save user data"""
        try:
            data = self.load_data()
            data["user"] = {
                "name": user_data.name,
                "email": user_data.email,
                "mhmd_preference": user_data.mhmd_preference.value
            }
            self.save_data(data)
            return True
        except Exception as e:
            print(f"Error saving user data: {e}")
            return False
    
    def update_user_data(self, **kwargs) -> Optional[UserData]:
        """Update specific fields of user data"""
        try:
            data = self.load_data()
            user_data = data.get("user", {})
            
            # Update only provided fields
            if "name" in kwargs and kwargs["name"] is not None:
                user_data["name"] = kwargs["name"]
            if "email" in kwargs and kwargs["email"] is not None:
                user_data["email"] = str(kwargs["email"])
            if "mhmd_preference" in kwargs and kwargs["mhmd_preference"] is not None:
                user_data["mhmd_preference"] = kwargs["mhmd_preference"].value
            
            data["user"] = user_data
            self.save_data(data)
            
            # Return updated user data if complete
            if user_data.get("name") and user_data.get("email"):
                return UserData(
                    name=user_data["name"],
                    email=user_data["email"],
                    mhmd_preference=MHMDPreference(user_data["mhmd_preference"])
                )
            return None
        except Exception as e:
            print(f"Error updating user data: {e}")
            return None
    
    def delete_user_data(self) -> bool:
        """Delete user data (reset to defaults)"""
        try:
            default_data = {
                "user": {
                    "name": "",
                    "email": "",
                    "mhmd_preference": "OPT_OUT"
                }
            }
            self.save_data(default_data)
            return True
        except Exception as e:
            print(f"Error deleting user data: {e}")
            return False
