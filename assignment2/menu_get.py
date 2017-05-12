import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Menus')
    
    try:
        response = table.get_item(
            Key={'menu_id': event['menu_id']}
        )
    except ClientError as e:
        return {"Error":e.response['Error']['Message']}
    else:
        item = response['Item']
        return item