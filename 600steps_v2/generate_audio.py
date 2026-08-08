import json
import os
import subprocess
from pathlib import Path

def generate_listening_audio():
    base_dir = Path(__file__).resolve().parent
    json_path = base_dir / "assets" / "questions" / "listening.json"
    audio_dir = base_dir / "assets" / "audio" / "listening"
    
    if not json_path.exists():
        print(f"Error: {json_path} not found.")
        return
        
    os.makedirs(audio_dir, exist_ok=True)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for item in data:
        audio_file = item.get("audio")
        script_text = item.get("script")
        
        if not audio_file or not script_text:
            continue
            
        output_path = audio_dir / audio_file
        if output_path.exists():
            print(f"Skipping {audio_file}, already exists.")
            continue
            
        print(f"Generating {audio_file}...")
        
        # Clean script text
        text_to_speak = script_text.replace("M:", "").replace("W:", "").replace("\n", " ")
        
        voice = "en-US-AriaNeural"
        temp_mp3 = audio_dir / (audio_file.replace(".ogg", ".mp3"))
        
        try:
            subprocess.run([
                "edge-tts",
                "--voice", voice,
                "--text", text_to_speak,
                "--write-media", str(temp_mp3)
            ], check=True)
            
            # Convert to OGG using ffmpeg
            subprocess.run([
                "ffmpeg", "-y", "-i", str(temp_mp3), "-c:a", "libvorbis", "-q:a", "4", str(output_path)
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Clean up temp mp3
            if temp_mp3.exists():
                temp_mp3.unlink()
                
            print(f"Successfully created {audio_file}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to generate {audio_file}: {e}")
            if temp_mp3.exists():
                temp_mp3.unlink()
            
if __name__ == "__main__":
    generate_listening_audio()
