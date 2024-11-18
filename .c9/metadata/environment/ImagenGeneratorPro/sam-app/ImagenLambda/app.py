{"filter":false,"title":"app.py","tooltip":"/ImagenGeneratorPro/sam-app/ImagenLambda/app.py","undoManager":{"mark":0,"position":0,"stack":[[{"start":{"row":0,"column":0},"end":{"row":42,"column":0},"action":"remove","lines":["import json","","# import requests","","","def lambda_handler(event, context):","    \"\"\"Sample pure Lambda function","","    Parameters","    ----------","    event: dict, required","        API Gateway Lambda Proxy Input Format","","        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format","","    context: object, required","        Lambda Context runtime methods and attributes","","        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html","","    Returns","    ------","    API Gateway Lambda Proxy Output Format: dict","","        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html","    \"\"\"","","    # try:","    #     ip = requests.get(\"http://checkip.amazonaws.com/\")","    # except requests.RequestException as e:","    #     # Send some context about this error to Lambda Logs","    #     print(e)","","    #     raise e","","    return {","        \"statusCode\": 200,","        \"body\": json.dumps({","            \"message\": \"hello world\",","            # \"location\": ip.text.replace(\"\\n\", \"\")","        }),","    }",""],"id":2},{"start":{"row":0,"column":0},"end":{"row":63,"column":0},"action":"insert","lines":["import base64","import boto3","import json","import random","import os","","def lambda_handler(event, context):","    try:","        # Get the prompt from the event","        body = json.loads(event.get('body', '{}'))","        prompt = body.get('prompt', 'Default prompt')","","        # Retrieve environment variables","        bucket_name = os.getenv('BUCKET_NAME')","        candidate_number = os.getenv('CANDIDATE_NUMBER')","","        if not bucket_name or not candidate_number:","            raise ValueError(\"Missing environment variables BUCKET_NAME or CANDIDATE_NUMBER\")","","        # Set up AWS clients","        bedrock_client = boto3.client(\"bedrock-runtime\", region_name=\"us-east-1\")","        s3_client = boto3.client(\"s3\")","","        # Generate file path","        seed = random.randint(0, 2147483647)","        s3_image_path = f\"{candidate_number}/titan_{seed}.png\"","","        # Bedrock model invocation","        native_request = {","            \"taskType\": \"TEXT_IMAGE\",","            \"textToImageParams\": {\"text\": prompt},","            \"imageGenerationConfig\": {","                \"numberOfImages\": 1,","                \"quality\": \"standard\",","                \"cfgScale\": 8.0,","                \"height\": 1024,","                \"width\": 1024,","                \"seed\": seed,","            }","        }","","        response = bedrock_client.invoke_model(","            modelId=\"amazon.titan-image-generator-v1\",","            body=json.dumps(native_request)","        )","        model_response = json.loads(response[\"body\"].read())","","        # Extract and decode the Base64 image data","        base64_image_data = model_response[\"images\"][0]","        image_data = base64.b64decode(base64_image_data)","","        # Upload the image to S3","        s3_client.put_object(Bucket=bucket_name, Key=s3_image_path, Body=image_data)","","        return {","            'statusCode': 200,","            'body': json.dumps({'message': 'Image generated successfully'})","        }","    except Exception as e:","        return {","            'statusCode': 500,","            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})","        }",""]}]]},"ace":{"folds":[],"scrolltop":0,"scrollleft":0,"selection":{"start":{"row":63,"column":0},"end":{"row":63,"column":0},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"timestamp":1731895918024,"hash":"53717a6cf6c29f89aaecf8eeba537d0045b410fa"}