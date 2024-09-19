# Azure AD User Identity Fetcher

This Python script fetches user identities from Azure AD or Azure B2C and summarizes the identity issuers (e.g., federated identities or UPNs). The script uses Microsoft Graph API to retrieve user data and outputs the results in CSV files.

## Prerequisites

1. **Python** installed on your machine.
2. **Azure App Registration** with the following permissions:
   - `User.Read.All`
   - `Directory.Read.All`

3. **Environment Variables** for sensitive credentials. You will need to create a `.env` file to store your app registration credentials.

## Setup

### Step 1: App Registration

1. Go to the [Azure Portal](https://portal.azure.com/) and navigate to **Azure Active Directory** or the **B2C Tenant** you wish to use.
2. Under **App registrations**, create a new registration and configure the following:
   - **API permissions**: 
     - Add `User.Read.All` and `Directory.Read.All` application permissions.
   - **Certificates & secrets**: Generate a new client secret and note it down.
3. Obtain the following information from the App Registration:
   - `CLIENT_ID`: Application (client) ID
   - `CLIENT_SECRET`: The generated client secret
   - `TENANT_ID`: Directory (tenant) ID

### Step 2: Clone the Repository

```bash
git clone https://github.com/Jordan-Murray/azure-ad-user-fetcher.git
cd azure-ad-user-fetcher
