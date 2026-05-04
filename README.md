# Tia Kay and Amaya Owens  --  Final Project CMSC 471
## System Write-up
The system that we have developed will take images of handwritten lists and convert them to text. The user will interact with the system through their browser. The browser will be connected to the API Gateway to communicate with the backend. From the API Gateway, there are several lambda functions that can be invoked. There is a lambda function to fetch and return the index.html from the S3 Bucket so that the webpage displays properly. There is a lambda function that will manage the S3 inbox files to control which files are displayed. Another lambda function will fetch and delete results and update the Aurora RDS. One lambda function will check the job status in the DynamoDB every 200 seconds so that updates can be given to the user. There is a lambda function to start execution, which is connected to a step function state machine within a serverless domain. The step functions state machine can invoke lambda functions to fetch images from the S3 bucket, invoke Amazon's textract to digitize the handwritten text, and to save the results in the DynamoDB and Aurora RDS. The DynamoDB stores the job status. The Aurora RDS is used to maintain the shopping list. The CloudWatch service was also used with the step function state machine to monitor the website to help troubleshoot bugs and detect abnormal usage.

## Mermaid Diagram
```mermaid
graph TD
    User[User browser] --> APIG[API Gateway\nPublic Entry Point]

    APIG -->|GET /| L0[Lambda\nFetch and Return Index.html]
    
    APIG -->|GET POST DELETE /api/inbox| LInbox[Lambda\nManage S3 inbox files]

    APIG -->|POST /api/jobs| LSubmit[Lambda\nstartExecution]
    APIG -->|GET /api/jobs/jobId| LPoll[Lambda\nPoll Job Status]

    APIG -->|GET DELETE /api/records| LRecords[Lambda\nFetch and delete results]

    L0 -.-> S3Web[S3 Bucket\nindex.html, JS, CSS]

    LInbox -.-> S3Store[S3 Bucket\nInbox Images]
    LSubmit -->|startExecution| SF
    LPoll -.-> DDB[DynamoDB\nJob State and Metadata]
    LRecords -.-> Aurora[Aurora RDS]

    subgraph Serverless[Serverless Domain]
        SF[Step Functions State Machine]

        SF --> L1[Lambda\nFetch image from S3]
        SF --> L2[Lambda\nCall Textract]
        SF --> L3[Lambda\nSave Results]

        L2 -.-> Textract[Amazon textract\nReplaces Bedrock]
    end
    L1 -.-> S3Store
    L3 -.-> Aurora
    L3 -.-> DDB
    
    CW[CloudWatch] -.-> SF
```
## DevOps Board
<img width="1201" height="445" alt="Screenshot 2026-05-04 182346" src="https://github.com/user-attachments/assets/7beae023-4230-4d02-90b7-eba876957d0b" />
<img width="1197" height="737" alt="Screenshot 2026-05-04 182406" src="https://github.com/user-attachments/assets/9cda4700-c883-41ff-8883-449c76313dc0" />

## Gherkin Files
```gherkin
    Feature: Upload Files
        Scenario: Upload files by browsing the device
            Given the user has selected a file
            When the user selects the upload button
            Then the file will display in the inbox files
```

## User Stories
### Amaya's User Stories
1. As a user, I want to be able to upload a file
2. As a user, I want to be able to view a list of my uploaded files
3. As a user, I want to be able to delete a file
4. As a user, I want my files to persist
5. As a user, I want the user interface to be clear and easy to navigate


## Well-Architected Questions

## Cost Calculator
The estimate given by https://calculator.aws was $180 upfront and $27.99 per month, coming to $515.88 (including upfront cost) for 12 months. The services entered were Amazon API Gateway: 

## Template.yaml

## Finished Website
<img width="1920" height="1008" alt="Owens and Kay Final Project - Deletion Working CMSC471" src="https://github.com/user-attachments/assets/7ab4b581-b557-4fcc-8ff9-6d099db30237" />

