#!/usr/bin/bash

# Install requirements
sudo yum -y install epel-release
sudo yum -y install python3 jq
sudo pip3 install awscli

echo "Please configure AWS"
aws configure

read -p "Please enter your Amazon Account ID: " arn
read -p "Please specify deployment region: " region

# Create roles and configure security
aws iam create-role --role-name emergency-events-executable --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'

# Build deployment package
zip emergency_events.zip emergency_events/lambda_function.py

#deploy artifacts
aws lambda create-function \
    --function-name emergency_events \
    --zip-file fileb://emergency_events.zip \
    --handler lambda_function.lambda_handler \
    --runtime python3.8 \
    --role arn:aws:iam::${arn}:role/emergency-events-executable

aws apigateway put-integration \
    --region ${region} \
    --http-method GET  \
    --type AWS \
    --integration-http-method POST  \
    --uri arn:aws:apigateway:${region}:lambda:path/2015-03-31/functions/arn:aws:lambda:${region}:${arn}:function:emergency_events/invocations --credentials arn:aws:iam::${arn}:role/apigAwsProxyRole
