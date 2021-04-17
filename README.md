# Speed Test Serverless App 

### Stack
- Serverless Framework
- Python + Flask
- AWS: Lambda + API Gateway + DynamoDB

### Motivation

I decided on this stack due to the possibility of its quick implementation and smooth AWS deployment. I am serverless enthusiast,  so I wanted to use this approach and leverages this kind of AWS components. I don't work often with Python on a daily basis, but I used it here as an experiment and because I was able to find an open-source library for speed test functionality https://github.com/sivel/speedtest-cli. 

The library obviously performs a speed test on the server side. Thus, local launch will test the local internet connection, while when deployed to another server, the test will be performed on a foreign server. I'm aware that it was not the essence of the task, but unfortunately I'm not a specialist in the implementation things on the client side (frontend technoligies), so I decided to simplify it

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

Serverless Framework will built our package with the code (app.py) and based on the deployment definition (serverless.yml) created the appropriate CloudFormation template, which will know what resources to create in AWS for our behalf

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
Local development required prior deployed stack on AWS to use DynamoDB from the cloud. To develop locally, you can use this same venv but you need to install boto3. I didn't put a boto3 into requirements.txt because it is embedded in Lambda runtime

```
pip install boto3
```

Then, run app:

```
sls wsgi serve
```

Navigate to localhost:5000 to see your app running locally.



