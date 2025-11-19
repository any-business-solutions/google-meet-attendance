import asyncio
from google_meet_client import GoogleMeetAPI
import time


async def main():
    SCOPES = ["https://www.googleapis.com/auth/meetings.space.created"]
    meet_api = GoogleMeetAPI(scopes=SCOPES)
    # Create a new Google Meet space
    # space_info = asyncio.run(meet_api.create_space())
    # print(f"Meeting URL: {space_info['meeting_uri']}")
    # print(f"Meeting Code: {space_info['meeting_code']}")

    # Save participants of the active meeting to a file
    for _ in range(3):
        print("Checking attendance...")
        await meet_api.get_participants_save_csv()
        print("Attendance saved. Waiting for the next check...")
        time.sleep(60*30)

if __name__ == "__main__":
    asyncio.run(main())
