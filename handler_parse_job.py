import boto3
import os
from datetime import datetime, timezone
from app_main import extract_requirements_from_xml

# Environment variables from serverless.yml
UPLOADS_BUCKET = os.environ['UPLOADS_BUCKET']
JOBS_TABLE = os.environ['JOBS_TABLE']

# AWS resources
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
jobs_table = dynamodb.Table(JOBS_TABLE)


def parse_job(event, context):
    """
    Lambda triggered by S3 'ObjectCreated:*' event.
    Fetches XML file from S3, parses it, and updates DynamoDB with results.
    """
    try:
        # S3 event payload contains bucket and object key
        records = event.get('Records', [])
        for record in records:
            s3_bucket = record['s3']['bucket']['name']
            s3_key = record['s3']['object']['key']

            # Extract jobId from filename (assuming format: jobId.xml)
            job_id = os.path.splitext(s3_key)[0]

            # Download XML from S3
            response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
            xml_content = response['Body'].read()

            # Parse XML and extract requirements
            results = extract_requirements_from_xml(xml_content)

            # Update DynamoDB with results and status
            jobs_table.update_item(
                Key={'jobId': job_id},
                UpdateExpression="SET #s = :status, results = :results, processedAt = :processedAt",
                ExpressionAttributeNames={
                    "#s": "status"
                },
                ExpressionAttributeValues={
                    ':status': 'complete',
                    ':results': results,
                    ':processedAt': datetime.now(timezone.utc).isoformat()
                }
            )

    except Exception as e:
        print(f"Error processing S3 event: {e}")
        # Optionally update DynamoDB status to 'failed'
        # jobs_table.update_item(...)

        raise e
