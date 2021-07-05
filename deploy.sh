#!/usr/bin/bash

# Install requirements
sudo yum -y install python3
sudo pip3 install awscli

echo "Please configure AWS"
aws configure

read -p "Please enter your Amazon Account ID: " arn

# Create roles and configure security
aws iam create-role --role-name lambda-ex --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'



# Build deployment package
zip emergency_events.zip emergency_events/lambda_function.py

aws lambda create-function --function-name my-math-function --zip-file fileb://emergency_events.zip --handler lambda_function.lambda_handler --runtime python3.8 --role arn:aws:iam::${arn}:role/lambda-ex
