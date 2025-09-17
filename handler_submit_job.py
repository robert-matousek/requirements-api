import boto3
import uuid
import os
from datetime import datetime, timezone

# Environment variables set in serverless.yml
UPLOADS_BUCKET = os.environ['UPLOADS_BUCKET']
JOBS_TABLE = os.environ['JOBS_TABLE']

# AWS resources
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
jobs_table = dynamodb.Table(JOBS_TABLE)

def submit_job(event, context):
    """
    Handles POST /jobs
    Expects a multipart/form-data with 'file' field containing XML.
    Note: Send your XML as Content-Type: application/xml or text/plain, API Gateway passes it as raw text.
    """
    try:
        # Extract the file from the event
        xml_content = event.get('body', '')
        if not xml_content:
            return {
                "statusCode": 400,
                "body": "Missing XML content"
            }

        # Generate a unique job ID
        job_id = str(uuid.uuid4())

        # Upload XML to S3
        s3_key = f"{job_id}.xml"
        s3_client.put_object(
            Bucket=UPLOADS_BUCKET,
            Key=s3_key,
            Body=xml_content,
            ContentType='application/xml'
        )

        # Store job metadata in DynamoDB
        jobs_table.put_item(
            Item={
                'jobId': job_id,
                'status': 'pending',
                's3Key': s3_key,
                'createdAt': datetime.now(timezone.utc).isoformat(),
                'results': []
            }
        )

        # Return job ID to client
        return {
            "statusCode": 201,
            "body": f'{{"jobId": "{job_id}", "status": "pending"}}'
        }

    except Exception as e:
        print(f"Error submitting job: {e}")
        return {
            "statusCode": 500,
            "body": f"Internal server error: {str(e)}"
        }
