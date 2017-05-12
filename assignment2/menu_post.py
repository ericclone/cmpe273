import boto3

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Menus')
    
    response = table.put_item(
        Item={
            "menu_id":event['menu_id'],
            "selection":event['selection'],
            "size":event['size'],
            "price":event['price'],
            "store_hours":event['store_hours']
        }
    )
    return 'OK'