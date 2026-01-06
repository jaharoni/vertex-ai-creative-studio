import sys

# Read the file
with open('main.py', 'r') as f:
    lines = f.readlines()

# Find and replace the credentials line in get_signed_url function
for i in range(len(lines)):
    # Look for the credentials line around line 141
    if 'credentials=signing_credentials,' in lines[i] and i > 130 and i < 150:
        # Replace with impersonated credentials approach
        indent = '    ' * 3
        # Insert impersonation code before the signed_url generation
        insert_pos = i - 4  # Before the signed_url = blob.generate_signed_url line
        
        # Find the start of blob.generate_signed_url
        while insert_pos < len(lines) and 'signed_url = blob.generate_signed_url' not in lines[insert_pos]:
            insert_pos += 1
        
        if insert_pos < len(lines):
            # Get service account email
            new_code = f"""{indent}# Get service account for signing
{indent}_, project = google.auth.default()
{indent}service_account_email = f"{{os.environ.get('SERVICE_ACCOUNT_EMAIL', f'{{project}}@appspot.gserviceaccount.com')}}"
{indent}
{indent}# Create impersonated credentials for signing
{indent}target_scopes = ['https://www.googleapis.com/auth/devstorage.read_write']
{indent}impersonated_creds = impersonated_credentials.Credentials(
{indent}    source_credentials=signing_credentials,
{indent}    target_principal=service_account_email,
{indent}    target_scopes=target_scopes,
{indent})
{indent}
"""
            lines.insert(insert_pos, new_code)
            # Update the credentials parameter
            for j in range(insert_pos, min(insert_pos + 20, len(lines))):
                if 'credentials=signing_credentials,' in lines[j]:
                    lines[j] = lines[j].replace('credentials=signing_credentials,', 'credentials=impersonated_creds,')
                    break
        break

# Write the file
with open('main.py', 'w') as f:
    f.writelines(lines)

print("Fixed signed URL credentials")
