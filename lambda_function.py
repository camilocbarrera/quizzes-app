import boto3
import json
import logging
from custom_encoder import CustomEncoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbTableName = 'user-quiz'

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(dynamodbTableName)

getMethod = 'GET'
postMethod = 'POST'

quizzesPath = '/quizzes'
responsePath = '/response'


def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']

    if httpMethod == getMethod and path == quizzesPath:
        response = getQuizzes()
    elif httpMethod == postMethod and path == responsePath:
        response = saveResponse(json.loads(event['body']))
    else:
        response = buidlResponse(404, 'Not Found')

    return response


def getQuizzes():
    try:
        response = table.scan()
        result = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStarKey=response['LastEvaluatedKey'])
            result.extended(response['Items'])

        body = {
            'responses': response
        }
        return buidlResponse(200, body)
    except:
        logger.exception("Error!")


def saveResponse(requestBody):
    try:
        table.put_item(Item=requestBody)
        body = {
            'Operation': 'SAVE',
            'MESSAGE': 'SUCCESS',
            'Item': requestBody
        }
        return buidlResponse(200, body)

    except:
        logger.exception("Error!")


def buidlResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)
    return response
