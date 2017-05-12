import boto3
from datetime import datetime
from time import strftime

dynamodb = boto3.resource('dynamodb')

def list2string(l):
    res = []
    for i in range(len(l)):
        res.append("{}. {}".format(i + 1, l[i]))
    return ", ".join(res)

def post(event):
    table = dynamodb.Table('orders')
    
    response = table.put_item(
        Item={
            "order_id":event['order_id'],
            "menu_id":event['menu_id'],
            "customer_name":event['customer_name'],
            "customer_email":event['customer_email'],
            "order_status": "processing",
            "order": {
                "selection": "-1",
                "size": "-1",
                "costs": "-1",
                "order_time": "-1"
            }
    
        }
    )
    
    table = dynamodb.Table('Menus')
    
    try:
        response = table.get_item(
            Key={'menu_id': event['menu_id']}
        )
        item = response['Item']
    except ClientError as e:
        return {"Error":e.response['Error']['Message']}
    
    selection = list2string(item['selection'])
        
    message = "Hi {}, please choose one of these selection:  {}".format(event['customer_name'], selection)
    
    return {"Message": message}
    
def put(event):
    table_order = dynamodb.Table('orders')
    
    try:
        response = table_order.get_item(
            Key={'order_id': event['order_id']}
        )
        order = response['Item']
    except ClientError as e:
        return {"Error":e.response['Error']['Message']}
        
    table_menu = dynamodb.Table('Menus')
    
    try:
        response = table_menu.get_item(
            Key={'menu_id': order['menu_id']}
        )
        menu = response['Item']
    except ClientError as e:
        return {"Error":e.response['Error']['Message']}
    
    choice = int(event['input']) - 1
    if order['order']['selection'] == "-1":
        order['order']['selection'] = menu['selection'][choice]
        table_order.put_item(Item=order)
        size = list2string(menu['size'])
        message = "Which size do you want? {}".format(size)
    else:
        order['order']['size'] = menu['size'][choice]
        cost = menu['price'][choice]
        order['order']['costs'] = cost
        order['order']['order_time'] = datetime.now().strftime("%m-%d-%Y@%H:%M:%S")
        table_order.put_item(Item=order)
        message = "Your order costs ${:.2f}. We will email you when the order is ready. Thank you!".format(float(cost))
    return {"Message": message}
    
def get(event):
    table_order = dynamodb.Table('orders')
    
    try:
        response = table_order.get_item(
            Key={'order_id': event['order_id']}
        )
        order = response['Item']
    except ClientError as e:
        return {"Error":e.response['Error']['Message']}
        
    return order

def lambda_handler(event, context):
    if event['action'] == "POST":
        return post(event['body'])
    elif event['action'] == "PUT":
        event['body']['order_id'] = event['order_id']
        return put(event['body'])
    elif event['action'] == "GET":
        event['body']['order_id'] = event['order_id']
        return get(event['body'])
        
    return 'Not supported'