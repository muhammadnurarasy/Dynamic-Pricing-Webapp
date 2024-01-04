import google.auth
from google.oauth2 import service_account
import google.auth.transport.requests

# Path to your service account key file
key_path = "solid-coder-408011-3216f9d3e6d1.json"

# Load the service account credentials
credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"])

# Request a new token
credentials.refresh(google.auth.transport.requests.Request())

# Print the access token
print(credentials.token)
