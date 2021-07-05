
Background  
==========  
911 emergency incident data are sent in nation wide in realtime so that we can provide better analytics to improve fire department operations and public safety.  
  
Task  
----  
Design a cloud based system for ingesting, enriching, and storing 911 incident data so that they can be used for analytics.  
  
Design  
------  
* In an effort to keep this simple, while providing the greatest flexibility for data schema, a NoSQL approach was used.  
* The service was deployed using AWS Lambda and API Gateway, while persisting ingested data in DynamoDB.  
* The individual deploying this application would need CentOS 7.3, git, sudo access, and basic unix knowledge for permissions.  They also need to have an AWS Key/Secret pair.
  
Installation:  
-------------  
* Ensure git is installed and pull the project:
>`$ git clone https://github.com/mbrinkg8tr/PEProject.git`
>`$ cd PEProject`
* Update executable permissions on the deployment script:
>`$ chmod 755 ./deploy.sh`
* Launch the deployment script:
> `$ ./deploy.sh`

