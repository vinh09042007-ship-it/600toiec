import json
import os
import shutil
from pathlib import Path
from player.profile import PlayerProfile

class SaveManager:
    """
    Handles all JSON file I/O for persisting the player's profile.
    """
    
    @staticmethod
    def _get_save_path() -> Path:
        """Returns the absolute path to the save file, ensuring the directory exists."""
        base_dir = Path(__file__).resolve().parent.parent
        save_dir = base_dir / "save"
        save_dir.mkdir(parents=True, exist_ok=True)
        return save_dir / "player_profile.json"

    @staticmethod
    def save_profile(profile: PlayerProfile) -> None:
        """
        Serializes the profile and saves it to disk.
        
        Args:
            profile (PlayerProfile): The profile instance to save.
        """
        print("Saving Player Profile...")
        file_path = SaveManager._get_save_path()
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(profile.to_dict(), f, indent=4)
            print("Saved successfully.")
        except Exception as e:
            print(f"Warning: Failed to save profile to {file_path}. Error: {e}")

    @staticmethod
    def load_profile() -> PlayerProfile:
        """
        Loads the profile from disk. Creates a new one if missing or corrupted.
        
        Returns:
            PlayerProfile: The restored or newly created profile.
        """
        print("Loading Player Profile...")
        file_path = SaveManager._get_save_path()
        
        if not file_path.exists():
            print("No save found. Creating default profile.")
            return SaveManager.create_default_profile()
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Simple validation: ensure it's a dict
            if not isinstance(data, dict):
                raise ValueError("Save file root must be a JSON object.")
                
            print("Save found.")
            profile = PlayerProfile.from_dict(data)
            
            print(f"Level: {profile.current_level}")
            print(f"Coins: {profile.total_coins}")
            print(f"EXP: {profile.total_exp}")
            
            return profile
            
        except Exception as e:
            print(f"Warning: Save file corrupted or unreadable. Error: {e}")
            backup_path = file_path.with_name("player_profile_backup.json")
            try:
                # Use shutil.move in case a backup already exists (it will overwrite)
                shutil.copy2(file_path, backup_path)
                print(f"Corrupted save renamed to {backup_path.name}")
            except Exception as backup_err:
                print(f"Failed to create backup: {backup_err}")
                
            print("Generating a fresh save.")
            return SaveManager.create_default_profile()

    @staticmethod
    def create_default_profile() -> PlayerProfile:
        """
        Creates and returns a fresh default profile.
        
        Returns:
            PlayerProfile: A new profile instance.
        """
        return PlayerProfile(player_name="Student")
