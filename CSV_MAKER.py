from supabase import create_client, Client
import csv
import random
from datetime import datetime, timedelta

# Replace these with your actual Supabase details
SUPABASE_URL = "https://tpgyjmwkfofcibihtdhl.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwZ3lqbXdrZm9mY2liaWh0ZGhsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTAxNzA1MSwiZXhwIjoyMDY2NTkzMDUxfQ.EwHX7EPpQy9EXP4NgToP8PCKoJPneiLf_SJ6dNtr-a8"
BUCKET_NAME = "cars"

# Initialize Supabase client with service role key
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
def list_files_and_save_to_csv():
    # List all files in the bucket
    response = supabase.storage.from_(BUCKET_NAME).list()
    print(response)  # Debugging: Print the response to see its structure
    if not response:
        print("No files found in the bucket.")
        return

    # Open a CSV file for writing
    with open('cars_images.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['filename', 'type', 'time', 'public_url'])

        for file_obj in response:
            filename = file_obj["name"]
            # Generate a random time within the last 30 days
           # Generate a random time (hour and minute)
            random_hour = random.randint(0, 23)
            random_minute = random.randint(0, 59)
            formatted_time = f"{random_hour:02d}:{random_minute:02d}"
            
            result = supabase.storage.from_(BUCKET_NAME).get_public_url(filename)
            public_url = result["publicUrl"] if isinstance(result, dict) and "publicUrl" in result else result

            # Write the data to the CSV file
            writer.writerow([filename, 'car', formatted_time, public_url])

    print("Data has been written to car_images.csv")


if __name__ == "__main__":
    list_files_and_save_to_csv()