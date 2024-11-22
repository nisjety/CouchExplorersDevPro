Imagen Generator Pro

Introduction:
Imagen Generator Pro is an AWS Lambda-powered application that generates images based on user-provided prompts using Amazon Bedrock. The application serves a web interface allowing users to input a prompt and view the generated image in real time.
The project integrates several AWS services, including Lambda, S3, API Gateway, and CloudFormation. The workflow and deployment are automated using GitHub Actions, ensuring a streamlined development and deployment process.

Features
Web Interface:            A user-friendly HTML page for entering prompts and viewing generated images in real-time.
Image Generation:         Utilizes Amazon Bedrock's generative AI model to create unique and visually appealing images based on user prompts.
AWS Integration:          Securely integrates with AWS services, including Amazon S3 for storing generated images and Amazon SQS for asynchronous message handling.
CI/CD:                    Fully automated deployment, testing, and infrastructure management workflows using GitHub Actions.
Monitoring and Alerts:    CloudWatch alarms monitor SQS queue delays, sending email notifications for potential performance issues.


Architecture
AWS Lambda:             Handles backend logic, processes image generation requests, and interacts with S3 for storing generated images.
Amazon S3:              Reliable and scalable storage solution for storing generated images and other static assets.
API Gateway:            Serves as the entry point for the application, providing endpoints for the HTML page and image generation requests.
Amazon SQS:             Manages asynchronous messaging for handling high volumes of image generation requests efficiently.
GitHub Actions:         Automates deployment pipelines for SAM and Terraform applications, ensuring seamless and error-free updates.
CloudWatch Alarms:      Tracks SQS queue performance metrics, like message age, to maintain user experience and system reliability.


Prerequisites
AWS Account:            Access to Amazon Bedrock, S3, SQS, and required IAM permissions.
AWS CLI and SAM CLI:    Installed and configured for deploying and managing the serverless application.
Node.js and Python:     Node.js (for development) and Python 3.9 for Lambda function development.
Docker:                 Required for running local builds, testing Lambda functions, and creating container images for the Java SQS client.
Terraform:              Installed for provisioning and managing infrastructure such as SQS queues and CloudWatch alarms.nt.


GitHub repository: CouchExplorersDevPro.
Local Setup
Clone the Repository, and go to:
cd ImagenGeneratorPro

Install Dependencies, with:
sam build

Run Locally, in a terminal write:
sam local start-api --port 4000
Access the Application: Open your browser and navigate to http://127.0.0.1:4000.

Deployment
Ensure your changes are pushed to the test first:

In a terminal write:
git add .
eksemple: git commit -m "Update application"
git push origin test

GitHub Actions: The deployment process is automated via GitHub Actions. Every push to main triggers the deployment workflow.

API Gateway URL: Once deployed, access the application using the API Gateway URL:

Static Page: https://nsironwlv8.execute-api.eu-west-1.amazonaws.com/Prod
Image Generation: https://nsironwlv8.execute-api.eu-west-1.amazonaws.com/Prod/generate

Files and Structure
CouchExplorersDevPro/
├── ImagenLambda/
│   ├── app.py                 # Lambda function logic
│   ├── index.html             # Web page
├── infra_sqs_terraform/       # Terraform configuration for infrastructure
│   ├── main.tf                # Main Terraform configuration
│   ├── provider.tf            # AWS provider configuration
│   ├── variables.tf           # Terraform variables
│   ├── outputs.tf             # Terraform outputs
│   ├── terraform.tfvars       # Terraform variable values
├── Dockerfile                 # Docker configuration for Java SQS Client
├── template.yaml              # AWS SAM template
├── .github/
│   ├── workflows/
│       ├── deploy.yml         # SAM application deployment workflow
│       ├── terraform_deploy.yml # Terraform infrastructure deployment workflow
│       ├── docker_publish.yml # Docker build and push workflow
├── README.md                  # Project documentation

Deliverables with Docker

| Requirement           | Description                                       | Location                              |
|-----------------------|---------------------------------------------------|---------------------------------------|
| Lambda Function       | Generates images based on user input              | `ImagenLambda/app.py`                 |
| Static Web Page       | Frontend interface for the app                    | `ImagenLambda/index.html`             |
| AWS SAM Template      | Infrastructure as code                            | `template.yaml`                       |
| CI/CD Workflow        | Automated deployment processes                    | `.github/workflows/`                  |
| S3 Bucket             | Stores generated images                           | `s3://pgr301-couch-explorers/`        |
| API Gateway Endpoint  | Serves the app and image generation               | **API URL:** `https://nsironwlv8.execute-api.eu-west-1.amazonaws.com/Prod/generate/` |
| Terraform Config      | Infrastructure for SQS monitoring                 | `infra_sqs_terraform/`                |
| Container Image       | Docker container for Java SQS Client              | **Image:** `nisjety/java-sqs-client:latest` |
| SQS Queue             | Handles message processing for image generation   | **URL:** `https://sqs.eu-west-1.amazonaws.com/244530008913/image_generation_pro` |


Testing
Generate Image:
      Navigate to the application.
      Enter a prompt and click "Generate Image."
      Verify the image is displayed.

Error Handling:
      Submit an invalid prompt or leave it blank.
      Verify the error message.
