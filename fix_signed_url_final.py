import re

# Read the file  
with open('main.py', 'r') as f:
    content = f.read()

# Fix: Replace the impersonated credentials section to use explicit service account email
# The issue is source_credentials.service_account_email doesn't exist on Compute Engine creds

pattern = r'(# Use impersonated credentials for signing \(required on Cloud Run\)\s+source_credentials, _ = google\.auth\.default\(\)\s+signing_credentials = impersonated_credentials\.Credentials\(\s+source_credentials=source_credentials,\s+target_principal=source_credentials\.service_account_email,\s+target_scopes=\[\'https://www\.googleapis\.com/auth/cloud-platform\'\],\s+\))'

replacement = r'''# Use impersonated credentials for signing (required on Cloud Run)
    source_credentials, project_id = google.auth.default()
    
    # Get the service account email - on Cloud Run this is the Compute Engine SA
    # Format: PROJECT_NUMBER-compute@developer.gserviceaccount.com
    import requests
    metadata_server = "http://metadata.google.internal/computeMetadata/v1/"
    metadata_flavor = {"Metadata-Flavor": "Google"}
    sa_email = requests.get(
        metadata_server + "instance/service-accounts/default/email",
        headers=metadata_flavor
    ).text
    
    signing_credentials = impersonated_credentials.Credentials(
        source_credentials=source_credentials,
        target_principal=sa_email,
        target_scopes=['https://www.googleapis.com/auth/cloud-platform'],
    )'''

content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)

# Write the file
with open('main.py', 'w') as f:
    f.write(content)

print("Fixed signed URL credentials with metadata server SA email lookup")
