```{mermaid}
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
