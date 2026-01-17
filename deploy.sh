#!/bin/bash

# Configuration
PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"
API_SERVICE_NAME="books-api"
DASHBOARD_SERVICE_NAME="books-dashboard"
REPO_NAME="books-repo"

echo "Deploying to Project: $PROJECT_ID in Region: $REGION"

# 1. Enable necessary services (optional, uncomment if needed)
# gcloud services enable artifactregistry.googleapis.com run.googleapis.com cloudbuild.googleapis.com

# 2. Create Artifact Registry repository if it doesn't exist
if ! gcloud artifacts repositories describe $REPO_NAME --location=$REGION &>/dev/null; then
    echo "Creating Artifact Registry repository..."
    gcloud artifacts repositories create $REPO_NAME \
        --repository-format=docker \
        --location=$REGION \
        --description="Docker repository for Books API project"
fi

# 3. Build and Push API Image
echo "Building and Pushing API Image..."
gcloud builds submit --config cloudbuild.api.yaml --substitutions=_IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/api:latest" .

# 4. Deploy API to Cloud Run
echo "Deploying API to Cloud Run..."
gcloud run deploy $API_SERVICE_NAME \
    --image "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/api:latest" \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --port 8000

# Get the API URL
API_URL=$(gcloud run services describe $API_SERVICE_NAME --region $REGION --format 'value(status.url)')
echo "API Deployed at: $API_URL"

# 5. Build and Push Dashboard Image
echo "Building and Pushing Dashboard Image..."
gcloud builds submit --config cloudbuild.dashboard.yaml --substitutions=_IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/dashboard:latest" .

# 6. Deploy Dashboard to Cloud Run
echo "Deploying Dashboard to Cloud Run..."
gcloud run deploy $DASHBOARD_SERVICE_NAME \
    --image "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/dashboard:latest" \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --port 8501 \
    --set-env-vars API_URL="$API_URL/api/v1"

# Get the Dashboard URL
DASHBOARD_URL=$(gcloud run services describe $DASHBOARD_SERVICE_NAME --region $REGION --format 'value(status.url)')
echo "Dashboard Deployed at: $DASHBOARD_URL"

echo "Deployment Complete!"
echo "API: $API_URL"
echo "Dashboard: $DASHBOARD_URL"
