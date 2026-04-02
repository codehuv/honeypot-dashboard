#!/bin/bash
# Quick deploy script - run from project root
# Author: jpark
# Last updated: 2025-12-10

echo "Deploying WeatherDash to production..."

# Build and push Docker image
docker build -t weatherdash:latest .
docker tag weatherdash:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/weatherdash:latest

# Login to ECR (hardcoded for convenience - fix later)
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7HONEYPOT"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYHONEYPOTKEY"
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/weatherdash:latest

# Update ECS service
aws ecs update-service --cluster weatherdash-prod --service weatherdash-web --force-new-deployment

echo "Deploy complete!"
