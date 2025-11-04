import asyncio
from datetime import datetime
import json
import os
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import meet_v2


class GoogleMeetAPI:

    def __init__(
        self,
        credentials_file="token.json",
        scopes=["https://www.googleapis.com/auth/meetings.space.created"],
    ):
        self.scopes = scopes
        self.credentials_file = credentials_file
        self.credentials = self._get_credentials()
        self.conference_client = None
        self.space_client = None

    def _get_credentials(self):
        """Handle Google API authentication and return valid credentials."""
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.credentials_file):
            creds = Credentials.from_authorized_user_file(
                self.credentials_file, self.scopes
            )
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.scopes
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.credentials_file, "w") as token:
                token.write(creds.to_json())
        return creds

    async def _get_conference_client(
        self,
    ) -> meet_v2.ConferenceRecordsServiceAsyncClient:
        """Get or create the async client."""
        if self.conference_client is None:
            self.conference_client = meet_v2.ConferenceRecordsServiceAsyncClient(
                credentials=self.credentials
            )
        return self.conference_client

    async def _get_space_client(self) -> meet_v2.SpacesServiceAsyncClient:
        if self.space_client is None:
            self.space_client = meet_v2.SpacesServiceAsyncClient(
                credentials=self.credentials
            )
        return self.space_client

    async def create_space(self):
        """Creates a new Google Meet space."""
        client = await self._get_space_client()
        request = meet_v2.CreateSpaceRequest()
        response = await client.create_space(request=request)

        return {
            "meeting_code": response.meeting_code,
            "meeting_uri": response.meeting_uri,
        }

    async def delete_space(self, space_name):
        """Deletes a Google Meet space."""
        client = await self._get_space_client()
        request = meet_v2.DeleteSpaceRequest(name=space_name)
        await client.delete_space(request=request)
        print(f"Space deleted: {space_name}")

    async def list_conference_records(self):
        """
        Retrieves and lists all conference records from Google Meet.

        Returns:
            list: A list of conference record names.
        """
        client = await self._get_conference_client()
        request = meet_v2.ListConferenceRecordsRequest()
        page_result = await client.list_conference_records(request=request)

        spaces = []
        async for response in page_result:
            spaces.append(
                {
                    "name": response.name,
                    "space": response.space,
                    "start_time": response.start_time,
                    "end_time": response.end_time,
                }
            )

        return spaces

    async def get_one_active_conference_record(self):
        """
        Get the first active conference record from Google Meet.

        Returns:
            dict: Conference record with name, space, and start_time if found, None otherwise.
        """
        client = await self._get_conference_client()
        request = meet_v2.ListConferenceRecordsRequest()
        page_result = await client.list_conference_records(request=request)

        async for response in page_result:
            if not response.end_time:
                return {
                    "name": response.name,
                    "space": response.space,
                    "start_time": response.start_time,
                }

    async def get_partipicants(self, parent_name: str):
        """
        Retrieves participants from a Google Meet conference.

        Args:
            parent_name (str): The parent resource name of the conference.

        Returns:
            dict: Dictionary containing participant information with keys:
                - parent_name: The conference parent name
                - signed_users: List of signed-in user display names
                - anonymus_users: List of anonymous user display names
        """
        # Create a client
        client = await self._get_conference_client()

        # Initialize request argument(s)
        request = meet_v2.ListParticipantsRequest(
            parent=parent_name,
        )

        # Make the request
        page_result = await client.list_participants(request=request)

        participants = {
            "parent_name": parent_name,
            "signed_users": [],
            "anonymus_users": [],
        }

        # Handle the response
        async for response in page_result:
            if response.anonymous_user:
                participants["anonymus_users"].append(
                    response.anonymous_user.display_name
                )
            elif response.signedin_user:
                participants["signed_users"].append(response.signedin_user.display_name)

        return participants

    async def get_participants_save(self, file_path='attendance'):
        active_conference = await self.get_one_active_conference_record()
        if not active_conference:
            print("No active Meeting right now!")
            return
        participants = await self.get_partipicants(active_conference.get("name"))
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        directory = Path(file_path)
        directory.mkdir(parents=True, exist_ok=True)
        file_path = directory / f"attendance-{now}.json"
        with open(str(file_path), "w") as f:
            json.dump(participants, f)