<<<<<<< HEAD
Imagen Generator Pro
Introduction:
Imagen Generator Pro is an AWS Lambda-powered application that generates images based on user-provided prompts using Amazon Bedrock. The application serves a web interface allowing users to input a prompt and view the generated image in real time.

The project integrates several AWS services, including Lambda, S3, API Gateway, and CloudFormation. The workflow and deployment are automated using GitHub Actions, ensuring a streamlined development and deployment process.

Features:
Web Interface:          A user-friendly HTML page for entering prompts and viewing generated images.
Image Generation:       Utilizes Amazon Bedrock's generative AI model to create images.
AWS Integration:        Securely stores generated images in an S3 bucket.
CI/CD:                  Automated deployment and testing using GitHub Actions.


Architecture
AWS Lambda:      Backend logic for processing requests, generating images, and interacting with S3.
Amazon S3:       Storage for the generated images.
API Gateway:     Provides endpoints for serving the HTML page and handling image generation requests.
GitHub Actions:  Automates the deployment process and ensures code quality.

Prerequisites
AWS account with access to Amazon Bedrock and S3.
Installed and configured AWS SAM CLI.
Node.js and Python 3.9 installed locally for development.


GitHub repository: ImagenGeneratorPro.
Local Setup
Clone the Repository, in a terminal write:
git clone https://github.com/nisjety/ImagenGeneratorPro.git
cd ImagenGeneratorPro

Install Dependencies, in a terminal write:
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

ImagenGeneratorPro/
├── ImagenLambda/
│   ├── app.py              # Lambda function logic
│   ├── index.html          # Web page
├── template.yaml           # AWS SAM template
├── .github/
│   ├── workflows/
│       ├── deploy.yml      # GitHub Actions workflow


Deliverables

Requirement	            Description	                                                Location
Lambda Function	      Generates images based on user input	                  app.py
Static Web Page	      Frontend interface for the application	                  index.html
AWS SAM Template	      Infrastructure as code	                                    template.yaml
CI/CD Workflow	      Automated deployment process	                              deploy.yml
S3 Bucket	            Stores generated images	                                    s3://pgr301-couch-explorers/8/
API Gateway Endpoint	Serves the application and image generation endpoint	      API URL


Testing
Generate Image:
      Navigate to the application.
      Enter a prompt and click "Generate Image."
      Verify the image is displayed.

Error Handling:
      Submit an invalid prompt or leave it blank.
      Verify the error message.
=======
# CouchExplorersDevPro
AWS Lambda-funksjon som genererer bilder basert på brukergenererte prompts ved hjelp av AWS SAM (Serverless Application Model)
>>>>>>> efdd4b780088507c92b1b87a95ab97801dd3dc81
