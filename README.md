# Speed Test Serverless App 

### Stack
- Serverless Framework
- Python + Flask
- AWS: Lambda + API Gateway + DynamoDB

### Motivation

I decided on this stack due to the possibility of its quick implementation and smooth AWS deployment. I am serverless enthusiast,  so I wanted to use this approach and leverages this kind of AWS components. I don't work often with Python on a daily basis, but I used it here as an experiment


### Speed test method

The internet speed connection is counted on the client side in browser. JS script downloads an image of a certain known size from the Internet. Knowing the size of the file and calculating the time needed to download the file, we are able to calculate the approximate speed of the link


```
duration = (endTime - startTime) / 1000;
bitsLoaded = imageSize * 8;
speedBps = bitsLoaded / duration
```


### App overview

```
├── conftest.py
├── requirements.txt
├── serverless.yml
├── src
│   ├── __init__.py
│   ├── data
│   │   ├── __init__.py
│   │   ├── measurement_repostiort.py
│   │   └── tests
│   │       └── test_repository.py
│   ├── entities
│   │   ├── __init__.py
│   │   ├── measurement_record.py
│   │   └── tests
│   │       └── test_entities.py
│   └── handlers
│       ├── __init__.py
│       ├── main_handler.py
│       └── templates
│           ├── index.hyml
│           └── result.html
└── resources
    └── dynamoDB.yml
```


`conftest.py` - This file is used by `pytest` to setup testing configuration. `Fixtures` in this file help setup the mocked infrastructure inside our tests.


`requirements.txt` - contains all required dependency. Only production dependencies should be present in the final solution. For simplicity, there are also test dependencies and boto3 which is not needed in deployment because it is embedded in Lambda runtime

```serverless.yml``` - main definition of serverless project. 

```resources``` - additional definition of resources which we want to provision used Serverless Framework

```src``` - source code packages and tests


### Setup and deployment

First of all we need install Serverless Framework. Instruction of installation you can find on my blog post 

https://cloud-box.pl/serverless-framework-konfiguracja-aws/

This entry cover part with installation of this tool and also creating dedicated AWS Role. 

Next you can download sources, move to main directory and install serverless framework packages 

```
git clone https://github.com/luafanti/speed-test-serverless
cd speed-test-serverless
npm install
```

Then you need to create python venv and install required packages

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

To deploy application to AWS, execute below command 

```
sls deploy
```

Serverless Framework will built our package with the code and based on the deployment definition (serverless.yml) created the appropriate CloudFormation template, which will know what resources to create in AWS for our behalf

Once the deploy is complete, run sls info to get the endpoint:

```
sls info

Service Information
<snip>
endpoints:
  ANY - https://7qez7sd8k6.execute-api.eu-west-2.amazonaws.com/measurement
  ANY - https://7qez7sd8k6.execute-api.eu-west-2.amazonaws.com/

```

### Local development
Local development required prior deployed stack on AWS to use DynamoDB from the cloud. To develop locally, you can use this same venv becouse for the sake of simplicity it has all the necessary dependencies. It is not a good solution for production applications !


Then, run app:

```
sls wsgi serve
```

Navigate to localhost:5000 to see your app running locally.


To run test 

```
pytest
```



