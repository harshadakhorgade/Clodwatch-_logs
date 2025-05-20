import boto3
import json

secret_name = "django_app_secrets"
region_name = "us-west-2"

session = boto3.session.Session()
client = session.client(service_name="secretsmanager", region_name=region_name)

try:
    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response['SecretString'])
    print("✅ Secret fetched successfully!")
    print(secret)
except Exception as e:
    print("❌ Error fetching secret:", e)
