#!/bin/bash

echo "🛠️ Generating .env configuration file..."

read -p "Enter QuickBooks Client ID: " QB_CLIENT_ID
read -p "Enter QuickBooks Client Secret: " QB_CLIENT_SECRET
read -p "Enter QuickBooks Redirect URI (e.g. http://localhost:8000/callback): " QB_REDIRECT_URI
read -p "Enter QuickBooks Refresh Token: " QB_REFRESH_TOKEN
read -p "Enter QuickBooks Company ID: " QB_COMPANY_ID
read -p "Enter Google API Key: " GOOGLE_API_KEY
read -p "Enter Gmail user email: " GMAIL_USER
read -p "Enter Gmail client secret: " GMAIL_CLIENT_SECRET
read -p "Enter Jibble API key: " JIBBLE_API_KEY
read -p "Enter Jotform API key: " JOTFORM_API_KEY
read -p "Use PostgreSQL? (yes/no): " USE_PG

if [[ "$USE_PG" == "yes" ]]; then
    read -p "Enter PostgreSQL DB URL (e.g. postgresql://user:pass@localhost/db): " PG_URL
    echo "DATABASE_URL=$PG_URL" > .env
else
    echo "DATABASE_URL=sqlite:///./test.db" > .env
fi

cat <<EOF >> .env
QB_CLIENT_ID=$QB_CLIENT_ID
QB_CLIENT_SECRET=$QB_CLIENT_SECRET
QB_REDIRECT_URI=$QB_REDIRECT_URI
QB_REFRESH_TOKEN=$QB_REFRESH_TOKEN
QB_COMPANY_ID=$QB_COMPANY_ID
GOOGLE_API_KEY=$GOOGLE_API_KEY
GMAIL_USER=$GMAIL_USER
GMAIL_CLIENT_SECRET=$GMAIL_CLIENT_SECRET
JIBBLE_API_KEY=$JIBBLE_API_KEY
JOTFORM_API_KEY=$JOTFORM_API_KEY
EOF

echo ".env file created!"
