#file name: DB_fetcher.py
# This file contains a class for fetching images from a Supabase database based on a time range 
# and returning the relevant entries.
# It handles both 'HH:MM' and 'HH:MM:SS' time formats
from supabase import create_client, Client
from datetime import datetime
from typing import List, Dict

class SupabaseImageFetcher:
    def __init__(self, url: str, service_role_key: str,
                 table_name: str, start_time: str, end_time: str):
        self.supabase: Client = create_client(url, service_role_key)
        self.table_name = table_name
        self.start_time = start_time
        self.end_time = end_time


    def get_images_in_time_range(
        self,
    ) -> List[Dict]:
        """
        Retrieve image entries from the specified table where 'time' is between start_time and end_time.
        Handles both 'HH:MM' and 'HH:MM:SS' time string formats.
        """
        # Convert start and end times to time objects
        start_dt = datetime.strptime(self.start_time, "%H:%M").time()
        end_dt = datetime.strptime(self.end_time, "%H:%M").time()

        # Fetch all records from the table
        response = self.supabase.table(self.table_name).select("*").execute()
        print("SANITY CHECK:", len(response.data), "records found in the table.")

        if not response.data:
            print("No records found in the table.")
            return []

        filtered = []
        for record in response.data:
            time_str = record.get("time")
            filename = record.get("filename")
            if not time_str:
                print("Skipping record with missing time field:", record)
                continue

            # Try parsing as HH:MM, then as HH:MM:SS
            try:
                try:
                    record_time = datetime.strptime(time_str.strip(), "%H:%M").time()
                except ValueError:
                    record_time = datetime.strptime(time_str.strip(), "%H:%M:%S").time()

                if start_dt <= record_time <= end_dt:
                    print(filename,"-Included picture:", record_time)
                    filtered.append(record)
                else:
                    print(filename,"-Excluded picture(out of range):", record_time)

            except ValueError:
                print("Skipping invalid time format:", time_str)
                continue

        return filtered

#EXAMPLE MODULE USAGE
"""
if __name__ == "__main__":
    SUPABASE_URL = "https://tpgyjmwkfofcibihtdhl.supabase.co"
    SUPABASE_SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwZ3lqbXdrZm9mY2liaWh0ZGhsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTAxNzA1MSwiZXhwIjoyMDY2NTkzMDUxfQ.EwHX7EPpQy9EXP4NgToP8PCKoJPneiLf_SJ6dNtr-a8"

    fetcher = SupabaseImageFetcher(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    results = fetcher.get_images_in_time_range(table_name="Images",start_time="00:00",end_time= "23:59")

    print(f"Found {len(results)} images between 00:00 and 23:59:")
    for image in results:
        print(f"Image: {image['filename']}, Time: {image['time']}, Public URL: {image['public_url']}")
"""