import base64
import boto3
import json
import random
import os

def lambda_handler(event, context):
    try:
        # Get the prompt from the event
        body = json.loads(event.get('body', '{}'))
        prompt = body.get('prompt', 'Default prompt')

        # Retrieve environment variables
        bucket_name = os.getenv('BUCKET_NAME')
        candidate_number = os.getenv('CANDIDATE_NUMBER')

        if not bucket_name or not candidate_number:
            raise ValueError("Missing environment variables BUCKET_NAME or CANDIDATE_NUMBER")

        # Set up AWS clients
        bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
        s3_client = boto3.client("s3")

        # Generate file path
        seed = random.randint(0, 2147483647)
        s3_image_path = f"{candidate_number}/titan_{seed}.png"

        # Bedrock model invocation
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

        response = bedrock_client.invoke_model(
            modelId="amazon.titan-image-generator-v1",
            body=json.dumps(native_request)
        )
        model_response = json.loads(response["body"].read())

        # Extract and decode the Base64 image data
        base64_image_data = model_response["images"][0]
        image_data = base64.b64decode(base64_image_data)

        # Upload the image to S3
        s3_client.put_object(Bucket=bucket_name, Key=s3_image_path, Body=image_data)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Image generated successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
