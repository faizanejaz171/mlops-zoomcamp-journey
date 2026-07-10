import base64
import json

def lambda_handler(event, context):
    """
    This function is triggered automatically by AWS Lambda 
    whenever a new record arrives in the Kinesis stream.
    """
    print("Lambda triggered! Processing new records from Kinesis...")
    
    # Kinesis sends data in batches, so we loop through the records
    for record in event['Records']:
        
        # The data is inside the 'kinesis' dictionary and is base64 encoded
        encoded_data = record['kinesis']['data']
        
        # Decode the base64 data back to a regular string
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        
        # Log the actual message
        print(f"Successfully decoded payload: {decoded_data}")
        
        # Note: Later, we will pass this decoded_data (image) to our YOLO model here!
        
    return {
        'statusCode': 200,
        'body': json.dumps('Records processed successfully!')
    }
