import base64
import json
import os


def lambda_handler(event, context):
    print("Lambda Triggered!")

    # Environment variables (S3 bucket aur Output Stream ka naam)
    output_stream = os.getenv("PREDICTIONS_STREAM_NAME", "ride-predictions-output")
    model_bucket = os.getenv("MODEL_BUCKET_NAME", "faizan-mlflow-models-bucket")

    print(f"Using Model Bucket: {model_bucket}")
    print(f"Sending to Stream: {output_stream}")

    # Kinesis se data parhna (Data base64 mein hota hai)
    for record in event["Records"]:
        payload = base64.b64decode(record["kinesis"]["data"]).decode("utf-8")
        print(f"Received raw data: {payload}")

        # Yahan asal mein ML Model prediction karta hai
        # Abhi hum sirf mock (fake) prediction return kar rahe hain

    return {
        "statusCode": 200,
        "body": json.dumps("Prediction successful and sent to output stream!"),
    }
