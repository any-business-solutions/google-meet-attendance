import asyncio
from google_meet_client import GoogleMeetAPI


if __name__ == "__main__":
    SCOPES = ["https://www.googleapis.com/auth/meetings.space.created"]
    meet_api = GoogleMeetAPI(scopes=SCOPES)
    # Create a new Google Meet space
    space_info = asyncio.run(meet_api.create_space())
    print(f"Meeting URL: {space_info['meeting_uri']}")
    print(f"Meeting Code: {space_info['meeting_code']}")

    # Save participants of the active meeting to a file
    # parent_name = asyncio.run(meet_api.get_participants_save())
