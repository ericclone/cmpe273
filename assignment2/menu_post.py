import boto3

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Menus')
    
    response = table.put_item(Item=event)
    return 'OK'
