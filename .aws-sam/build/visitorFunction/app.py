import json
import boto3
import os

# Initialize dynamodb boto3 object
dynamodb = boto3.resource('dynamodb')
# Set dynamodb table name variable from env
ddbTableName = os.environ['databaseName']
table = dynamodb.Table(ddbTableName)

def lambda_handler(event, context):
    # Update item in table or add if doesn't exist
    ddbResponse = table.update_item(
        Key={
            'id': 'count'
        },
        UpdateExpression='SET visitor_count = visitor_count + :value',
        ExpressionAttributeValues={
            ':value':1
        },
        ReturnValues="UPDATED_NEW"
    )

    # Format dynamodb response into variable
    responseBody = json.dumps({"Count": ddbResponse["Attributes"]["visitor_count"]})

    # Create api response object
    apiResponse = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": responseBody
    }

    # Return api response object
    return apiResponse
