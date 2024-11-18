import os
import json
import boto3
import base64
import random
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        path = event.get('path', '')

        # Serve the HTML page
        if event.get('httpMethod') == 'GET' and path == '/':
            logger.info("Serving the index.html file.")
            try:
                with open('index.html', 'r') as file:
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'text/html'},
                        'body': file.read()
                    }
            except FileNotFoundError:
                logger.error("index.html not found.")
                return {'statusCode': 404, 'body': 'index.html not found'}

        # Serve the CSS file
        if event.get('httpMethod') == 'GET' and path == '/styles.css':
            logger.info("Serving the styles.css file.")
            try:
                with open('styles.css', 'r') as file:
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'text/css'},
                        'body': file.read()
                    }
            except FileNotFoundError:
                logger.error("styles.css not found.")
                return {'statusCode': 404, 'body': 'styles.css not found'}

        # Serve the JavaScript file
        if event.get('httpMethod') == 'GET' and path == '/script.js':
            logger.info("Serving the script.js file.")
            try:
                with open('script.js', 'r') as file:
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/javascript'},
                        'body': file.read()
                    }
            except FileNotFoundError:
                logger.error("script.js not found.")
                return {'statusCode': 404, 'body': 'script.js not found'}

        # Handle POST requests to generate the image
        if event.get('httpMethod') == 'POST' and path == '/generate':
            logger.info("Generating image based on the prompt.")
            
            # Load environment variables
            bucket_name = os.environ.get('BUCKET_NAME')
            candidate_number = os.environ.get('CANDIDATE_NUMBER')

            if not bucket_name or not candidate_number:
                logger.error("Missing required environment variables.")
                return {
                    'statusCode': 500,
                    'body': json.dumps({'message': 'Missing required environment variables'})
                }

            # Parse and validate the input
            try:
                body = json.loads(event.get('body', '{}'))
                prompt = body.get('prompt', '').strip()
                if not prompt:
                    logger.warning("Prompt is missing or empty.")
                    return {
                        'statusCode': 400,
                        'body': json.dumps({'message': 'Prompt is required'})
                    }
            except json.JSONDecodeError:
                logger.error("Invalid JSON body.")
                return {
                    'statusCode': 400,
                    'body': json.dumps({'message': 'Invalid JSON in request body'})
                }

            # Generate a unique file name for the image
            seed = random.randint(0, 2147483647)
            s3_image_path = f"{candidate_number}/titan_{seed}.png"

            # Set up Bedrock client and request
            bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
            native_request = {
                "taskType": "TEXT_IMAGE",
                "textToImageParams": {"text": prompt},
                "imageGenerationConfig": {
                    "numberOfImages": 1,
                    "quality": "standard",
                    "cfgScale": 8.0,
                    "height": 1024,
                    "width": 1024,
                    "seed": seed,
                }
            }

            # Invoke the Bedrock model
            try:
                response = bedrock_client.invoke_model(
                    modelId="amazon.titan-image-generator-v1",
                    body=json.dumps(native_request)
                )
                model_response = json.loads(response["body"].read())
            except Exception as e:
                logger.error(f"Bedrock invocation failed: {str(e)}")
                return {
                    'statusCode': 500,
                    'body': json.dumps({'message': 'Failed to generate image', 'error': str(e)})
                }

            # Decode and upload the image to S3
            try:
                base64_image_data = model_response["images"][0]
                image_data = base64.b64decode(base64_image_data)
                s3_client = boto3.client('s3')
                s3_client.put_object(Bucket=bucket_name, Key=s3_image_path, Body=image_data)
            except Exception as e:
                logger.error(f"Failed to upload image to S3: {str(e)}")
                return {
                    'statusCode': 500,
                    'body': json.dumps({'message': 'Failed to upload image to S3', 'error': str(e)})
                }

            # Construct the S3 image URL
            image_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_image_path}"
            logger.info(f"Image successfully generated and uploaded: {image_url}")

            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Image generated successfully', 'image_url': image_url})
            }

        # Return 404 for other paths
        logger.warning(f"Path not found: {path}")
        return {'statusCode': 404, 'body': 'Path not found'}

    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
