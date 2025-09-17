from app_main import extract_requirements_from_xml

def parse_sync(event, context):
    """
    Lambda for POST /parse/sync
    Receives XML content in the request body, parses it synchronously,
    and returns results immediately.
    """
    try:
        # Get raw XML content from request body
        xml_content = event.get('body', '')
        if not xml_content:
            return {
                "statusCode": 400,
                "body": "Missing XML content in request body"
            }

        # Parse XML and extract requirements
        results = extract_requirements_from_xml(xml_content)

        # Returns a JSON response containing a results array.
        return {
            "statusCode": 200,
            "body": {
                "results": results
            }
        }

    except Exception as e:
        print(f"Error parsing XML synchronously: {e}")
        return {
            "statusCode": 500,
            "body": f"Internal server error: {str(e)}"
        }
