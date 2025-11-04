import asyncio
from google_meet_client import GoogleMeetAPI


if __name__ == "__main__":
    SCOPES = ["https://www.googleapis.com/auth/meetings.space.created"]
    meet_api = GoogleMeetAPI(scopes=SCOPES)
    # print(asyncio.run(meet_api.create_space()))
    parent_name = asyncio.run(meet_api.get_participants_save())
