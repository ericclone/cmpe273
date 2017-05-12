import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Menus')
    
    expression = []
    values = {}
    body = event['body']
    if 'selection' in body:
        expression.append('selection=:sel')
        values[':sel'] = body['selection']
    
    if 'size' in body:
        expression.append('selection=:sz')
        values[':sz'] = body['size']
    
    if 'price' in event:
        expression.append('price=:p')
        values[':p'] = body['price']
    
    updateExpression = "set " + ",".join(expression)
    
    response = table.update_item(
        Key={'menu_id':event['menu_id']},
        UpdateExpression=updateExpression,
        ExpressionAttributeValues=values,
        ReturnValues="UPDATED_NEW"
    )

    return "OK"