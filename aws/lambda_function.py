import json
from questions import get_questions

def lambda_handler(event, context):
    inputs = event['queryStringParameters']
    return {
        'statusCode': 200,
        'body': json.dumps(get_questions(inputs['url']))
    }
    