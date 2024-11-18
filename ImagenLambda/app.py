import base64
import boto3
import json
import random
import os
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambda handler function for serving the HTML page and generating images.
    """
    try:
        # Handle GET request to serve the HTML page
        if event.get('httpMethod') == 'GET' and event.get('path') == '/':
            logger.info("Serving the index.html file.")
            try:
                with open('index.html', 'r') as file:
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'text/html'},
                        'body': file.read()
                    }
            except FileNotFoundError:
                logger.error("index.html file not found.")
                return {
                    'statusCode': 404,
                    'body': json.dumps({'message': 'index.html not found'})
                }

        # Validate HTTP method
        if event.get('httpMethod') != 'POST':
            logger.warning("Invalid HTTP method received.")
            return {
                'statusCode': 405,
                'body': json.dumps({'message': 'Method Not Allowed'})
            }

        # Load environment variables
        bucket_name = os.environ.get('BUCKET_NAME')
        candidate_number = os.environ.get('CANDIDATE_NUMBER')
        if not bucket_name or not candidate_number:
            logger.error("Missing required environment variables.")
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Missing required environment variables'})
            }

        # Parse and validate input body
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
            logger.error("Failed to parse JSON body.")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid JSON in request body'})
            }

        # Generate a unique file name for the image
        seed = random.randint(0, 2147483647)
        s3_image_path = f"{candidate_number}/titan_{seed}.png"

        # Set up Bedrock client and prepare the request
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
            logger.info("Invoking the Bedrock model.")
            response = bedrock_client.invoke_model(
                modelId="amazon.titan-image-generator-v1",
                body=json.dumps(native_request)
            )
            model_response = json.loads(response["body"].read())
        except Exception as bedrock_error:
            logger.error(f"Bedrock invocation failed: {str(bedrock_error)}")
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Failed to generate image', 'error': str(bedrock_error)})
            }

        # Decode and upload the image to S3
        try:
            logger.info("Decoding and uploading image to S3.")
            base64_image_data = model_response["images"][0]
            image_data = base64.b64decode(base64_image_data)
            s3_client = boto3.client('s3')
            s3_client.put_object(Bucket=bucket_name, Key=s3_image_path, Body=image_data)
        except Exception as s3_error:
            logger.error(f"Failed to upload image to S3: {str(s3_error)}")
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Failed to upload image to S3', 'error': str(s3_error)})
            }

        # Construct the S3 image URL
        image_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_image_path}"
        logger.info(f"Image successfully generated and uploaded: {image_url}")

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Image generated successfully', 'image_url': image_url})
        }

    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
