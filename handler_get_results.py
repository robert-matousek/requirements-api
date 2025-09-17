import boto3
import os

# Environment variables from serverless.yml
JOBS_TABLE = os.environ['JOBS_TABLE']

# AWS resources
dynamodb = boto3.resource('dynamodb')
jobs_table = dynamodb.Table(JOBS_TABLE)

def get_results(event, context):
    """
    Lambda for GET /jobs/{jobId}/results
    Retrieves job status and results from DynamoDB using the jobId path parameter.
    """
    try:
        # Extract jobId from path parameters
        path_params = event.get('pathParameters', {})
        job_id = path_params.get('jobId')

        if not job_id:
            return {
                "statusCode": 400,
                "body": "Missing jobId in path parameters"
            }

        # Fetch job record from DynamoDB
        response = jobs_table.get_item(Key={'jobId': job_id})
        item = response.get('Item')

        # Return 404 if the job does not exist.
        if not item:
            return {
                "statusCode": 404,
                "body": f"Job {job_id} not found"
            }

        # Return job status and results
        return {
            "statusCode": 200,
            "body": {
                "jobId": job_id,
                "status": item.get('status', 'unknown'),
                "results": item.get('results', [])
            }
        }

    except Exception as e:
        print(f"Error retrieving job results: {e}")
        return {
            "statusCode": 500,
            "body": f"Internal server error: {str(e)}"
        }
