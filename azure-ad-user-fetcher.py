import msal
import requests
import csv
from collections import Counter
import os
from dotenv import load_dotenv

load_dotenv()

# App Registration credentials
client_id = os.getenv("CLIENT_ID") 
client_secret = os.getenv("CLIENT_SECRET")  
tenant_id = os.getenv("TENANT_ID")  

graph_url = 'https://graph.microsoft.com/beta/users'

authority_url = f'https://login.microsoftonline.com/{tenant_id}'
app = msal.ConfidentialClientApplication(client_id, authority=authority_url, client_credential=client_secret)

scopes = ["https://graph.microsoft.com/.default"]
token_response = app.acquire_token_for_client(scopes=scopes)

if "access_token" in token_response:
    access_token = token_response['access_token']

    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    next_link = graph_url
    all_users_data = []
    identity_counter = Counter()

    while next_link:
        response = requests.get(next_link, headers=headers)

        if response.status_code == 200:
            users_data = response.json()
            all_users_data.extend(users_data['value']) 

            next_link = users_data.get('@odata.nextLink')
        else:
            print(f"Error retrieving users: {response.status_code} - {response.text}")
            break

    with open('b2c_users_displayname_identities_summary.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Display Name", "Identities", "Distinct Identities"])

        for user in all_users_data:
            display_name = user.get('displayName', 'N/A')

            identities = user.get('identities', [])
            identities_str = ", ".join([f"{identity['issuer']}: {identity['signInType']}" for identity in identities]) if identities else "No identities"
            
            for identity in identities:
                identity_counter[identity['issuer']] += 1

            writer.writerow([display_name, identities_str])

    with open('identity_summary.csv', 'w', newline='', encoding='utf-8') as summary_file:
        summary_writer = csv.writer(summary_file)
        summary_writer.writerow(["Issuer", "Count"])
        for issuer, count in identity_counter.items():
            summary_writer.writerow([issuer, count])

    print("User data and identity summary have been written to CSV files.")
else:
    print(f"Error retrieving access token: {token_response}")