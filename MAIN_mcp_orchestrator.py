# file: orchestrator.py

from Yolo_image_detector import YoloDetector
from DB_fetcher import SupabaseImageFetcher
from LLM_mission_parser import MissionParserLLM

def run_mission(mission_text):
    LLM_Parser = MissionParserLLM()
    # === 1. Parse the mission ===
    print(f"Mission received: {mission_text}")
    parsed = LLM_Parser.parse_mission(mission_text)
    target_class = parsed["target_object"]
    start_time = parsed["start_time"]
    end_time = parsed["end_time"]

    print(f"Target class: {target_class}, Time range: {start_time} to {end_time}")

    # === 2. Connect to Supabase and fetch image metadata ===
    SUPABASE_URL = "https://tpgyjmwkfofcibihtdhl.supabase.co"
    SUPABASE_SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwZ3lqbXdrZm9mY2liaWh0ZGhsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTAxNzA1MSwiZXhwIjoyMDY2NTkzMDUxfQ.EwHX7EPpQy9EXP4NgToP8PCKoJPneiLf_SJ6dNtr-a8"
    TABLE_NAME = "Images"
    db = SupabaseImageFetcher(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, TABLE_NAME, start_time, end_time)
    image_metadata = db.get_images_in_time_range()

    if not image_metadata:
        print("No images found in the specified time range.")
        return []

    images = [(record["filename"], record["public_url"]) for record in image_metadata]


    # === 3. Detect objects in images ===
    detector = YoloDetector(target_class=target_class)
    matched_images = detector.detect_all(images)
    

    # === 4. Filter out image filenames that contain the target class ===
    
    print(f"\nImages containing '{target_class}' between {start_time} and {end_time}:")
    if len(matched_images) == 0:
        print("No images matched the target class.")
        return []
    for filename,results in matched_images:
        print("-", filename)
    
    return matched_images


# MAIN PROGRAM
if __name__ == "__main__":
    mission = input("Enter mission: ")  # e.g., "detect all cars in images between 11:00 and 11:05"
    run_mission(mission)
