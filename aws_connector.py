"""AWS Connector Module for S3 operations"""
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)

class AWSConnector:
    def __init__(self, region='ap-south-1'):
        """Initialize AWS S3 connector"""
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region)
        self.s3_resource = boto3.resource('s3', region_name=region)
    
    def list_buckets(self):
        """List all S3 buckets"""
        try:
            response = self.s3_client.list_buckets()
            buckets = [bucket['Name'] for bucket in response['Buckets']]
            logger.info(f"Found {len(buckets)} buckets")
            return buckets
        except ClientError as e:
            logger.error(f"Error listing buckets: {e}")
            return []
    
    def bucket_exists(self, bucket_name):
        """Check if S3 bucket exists"""
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            logger.info(f"Bucket '{bucket_name}' exists")
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                logger.warning(f"Bucket '{bucket_name}' does not exist")
            else:
                logger.error(f"Error checking bucket: {e}")
            return False
    
    def upload_file(self, bucket_name, file_path, object_key):
        """Upload file to S3 bucket"""
        try:
            self.s3_client.upload_file(file_path, bucket_name, object_key)
            logger.info(f"File '{file_path}' uploaded to '{bucket_name}/{object_key}'")
            return True
        except ClientError as e:
            logger.error(f"Error uploading file: {e}")
            return False
    
    def download_file(self, bucket_name, object_key, file_path):
        """Download file from S3 bucket"""
        try:
            self.s3_client.download_file(bucket_name, object_key, file_path)
            logger.info(f"File downloaded from '{bucket_name}/{object_key}' to '{file_path}'")
            return True
        except ClientError as e:
            logger.error(f"Error downloading file: {e}")
            return False
    
    def list_objects(self, bucket_name):
        """List all objects in S3 bucket"""
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            if 'Contents' in response:
                objects = [obj['Key'] for obj in response['Contents']]
                logger.info(f"Found {len(objects)} objects in '{bucket_name}'")
                return objects
            return []
        except ClientError as e:
            logger.error(f"Error listing objects: {e}")
            return []
    
    def delete_object(self, bucket_name, object_key):
        """Delete object from S3 bucket"""
        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=object_key)
            logger.info(f"Object '{object_key}' deleted from '{bucket_name}'")
            return True
        except ClientError as e:
            logger.error(f"Error deleting object: {e}")
            return False


if __name__ == '__main__':
    # Test the connector
    connector = AWSConnector()
    buckets = connector.list_buckets()
    print(f"Available buckets: {buckets}")
