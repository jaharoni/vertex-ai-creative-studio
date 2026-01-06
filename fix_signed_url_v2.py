import re

# Read the file
with open('main.py', 'r') as f:
    content = f.read()

# Find the get_signed_url function and replace the credential creation part
# The issue is that compute_engine.Credentials() doesn't have signing capability
# We need to use impersonated_credentials.Credentials instead

# Find the section where signing_credentials is created
pattern = r'(signing_credentials = credentials.Credentials\(\))'
replacement = r'''# Use impersonated credentials for signing (required on Cloud Run)
    source_credentials, _ = google.auth.default()
    signing_credentials = impersonated_credentials.Credentials(
        source_credentials=source_credentials,
        target_principal=source_credentials.service_account_email,
        target_scopes=['https://www.googleapis.com/auth/cloud-platform'],
    )'''

content = re.sub(pattern, replacement, content)

# Write the file
with open('main.py', 'w') as f:
    f.write(content)

print("Fixed signed URL credentials using impersonation")
