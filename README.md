# Google Meet Attendance Tracker

A Python application that automatically tracks attendance for Google Meet conferences by retrieving participant information from active meetings.

## Features

- 🎥 Create and manage Google Meet spaces
- 👥 Track participants in active meetings
- 📊 Export attendance data to JSON files
- 🔐 Secure OAuth2 authentication with Google APIs
- ⚡ Asynchronous operations for better performance

## Prerequisites

- Python 3.10 or higher
- Google Cloud Console account
- Google Workspace account (for testing)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/any-business-solutions/google-meet-attendance.git
   cd google-meet-attendance
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Google Cloud Setup

### Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter a project name (e.g., "meet-attendance-tracker")
4. Click "Create"

### Step 2: Enable the Google Meet API

1. In the Google Cloud Console, navigate to "APIs & Services" → "Library"
2. Search for "Google Meet API"
3. Click on "Google Meet API" and click "Enable"

### Step 3: Create OAuth2 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in the required fields:
     - App name: Your app name
     - User support email: Your email
     - Developer contact information: Your email
   - Add scopes: `https://www.googleapis.com/auth/meetings.space.created`
   - Add test users (see important note below)
4. For OAuth client ID:
   - Application type: "Desktop application"
   - Name: "Google Meet Attendance Client"
5. Click "Create"
6. Download the JSON file and rename it to `credentials.json`
7. Place `credentials.json` in the project root directory

## ⚠️ Important: Adding Test Users

**CRITICAL**: You must add test users to your OAuth consent screen for the application to work properly.

1. In Google Cloud Console, go to "APIs & Services" → "OAuth consent screen"
2. Scroll down to "Test users" section
3. Click "Add users"
4. Add the email addresses of users who will:
   - Run this application
   - Join Google Meet sessions that will be tracked
5. Click "Save"

**Note**: Without adding test users, the application will not be able to access Google Meet data, even for meetings you organize.

### Step 4: Configure Scopes (Optional)

The application uses the following scope by default:
- `https://www.googleapis.com/auth/meetings.space.created`

You can modify the scopes in `main.py` if needed.

## Usage

### Basic Usage

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **First-time authentication:**
   - A browser window will open for OAuth2 authentication
   - Sign in with your Google account
   - Grant the requested permissions
   - The authentication token will be saved as `token.json`

3. **Track attendance:**
   - The application will automatically detect active Google Meet conferences
   - Participant data will be saved to the `attendance/` directory
   - Files are named with timestamp: `attendance-YYYYMMDD_HHMMSS.json`

### API Usage Examples

```python
import asyncio
from google_meet_client import GoogleMeetAPI

# Initialize the API client
SCOPES = ["https://www.googleapis.com/auth/meetings.space.created"]
meet_api = GoogleMeetAPI(scopes=SCOPES)

# Create a new Google Meet space
space_info = asyncio.run(meet_api.create_space())
print(f"Meeting URL: {space_info['meeting_uri']}")
print(f"Meeting Code: {space_info['meeting_code']}")

# Get participants from active meeting and save to file
asyncio.run(meet_api.get_participants_save())

# List all conference records
conferences = asyncio.run(meet_api.list_conference_records())
print(conferences)
```

## Output Format

The attendance data is saved in JSON format with the following structure:

```json
{
  "parent_name": "conferenceRecords/ABC123...",
  "signed_users": [
    "John Doe",
    "Jane Smith"
  ],
  "anonymus_users": [
    "Anonymous User 1"
  ]
}
```

## File Structure

```
google-meet-attendance/
├── main.py                     # Main application entry point
├── google_meet_client.py       # Google Meet API client
├── requirements.txt            # Python dependencies
├── credentials.json            # OAuth2 credentials (you need to create this)
├── token.json                  # Authentication token (auto-generated)
├── attendance/                 # Directory for attendance files
│   └── attendance-*.json       # Timestamped attendance records
└── conferenceRecords/          # Directory for conference record backups
    └── *.json                  # Conference record files
```

## Troubleshooting

### Common Issues

1. **"credentials.json not found"**
   - Ensure you've downloaded the OAuth2 credentials from Google Cloud Console
   - Verify the file is named exactly `credentials.json`
   - Check that the file is in the project root directory

2. **"No active Meeting right now!"**
   - Make sure you have an active Google Meet session running
   - Verify that the Google account used for authentication has access to the meeting
   - Ensure test users are properly configured in OAuth consent screen

3. **Authentication errors**
   - Delete `token.json` and re-authenticate
   - Check that the correct scopes are configured
   - Verify that the Google Meet API is enabled in your project

4. **Permission denied errors**
   - Ensure all required test users are added to the OAuth consent screen
   - Verify that the authenticated user has appropriate permissions
   - Check that the Google Meet API is properly enabled

### API Limitations

- The application can only track meetings where the authenticated user has appropriate access
- Anonymous users are listed but may have limited information
- Meeting data is only available for recent conferences (Google's retention policy applies)

## Security Notes

- Keep `credentials.json` and `token.json` secure and never commit them to version control
- The `credentials.json` file contains sensitive OAuth2 client information
- The `token.json` file contains user authentication tokens

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section above
- Review Google Meet API documentation: https://developers.google.com/meet/api

## Changelog

### v1.0.0
- Initial release with basic attendance tracking functionality
- Support for creating and managing Google Meet spaces
- Asynchronous API operations
- JSON export functionality