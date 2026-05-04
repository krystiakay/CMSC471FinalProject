# Tia Kay and Amaya Owens  --  Final Project CMSC 471
## System Write-up


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

