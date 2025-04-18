import os
import sys
import boto3

from Xray.exception import XRayException


class S3Operation:
    def __init__(self):
        self.s3 = boto3.client('s3')

    def sync_folder_to_s3(
        self, folder: str, bucket_name: str, bucket_folder_name: str
    ) -> None:
        try:
            command: str = (
                f"aws s3 sync {folder} s3://{bucket_name}/{bucket_folder_name}/ "
            )

            os.system(command)

        except Exception as e:
            raise XRayException(e, sys)

    def sync_folder_from_s3(
        self, folder: str, bucket_name: str, bucket_folder_name: str
    ) -> None:
        try:
            # Create the folder if it doesn't exist
            if not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)

            # Try to use AWS CLI first
            command: str = (
                f"aws s3 sync s3://{bucket_name}/{bucket_folder_name}/ {folder} "
            )

            result = os.system(command)

            # If AWS CLI fails, use boto3 as fallback
            if result != 0:
                self._download_with_boto3(bucket_name, bucket_folder_name, folder)

        except Exception as e:
            raise XRayException(e, sys)

    def _download_with_boto3(self, bucket_name, bucket_folder_name, local_dir):
        """Fallback method to download using boto3 instead of AWS CLI"""
        try:
            print(f"Downloading from S3 bucket: {bucket_name}/{bucket_folder_name} to {local_dir}")

            # List objects in the bucket
            response = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=bucket_folder_name)

            # Download each object
            for item in response.get('Contents', []):
                s3_key = item['Key']
                if s3_key.endswith("/"):
                    continue  # skip folders

                local_file_path = os.path.join(local_dir, os.path.relpath(s3_key, bucket_folder_name))
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

                self.s3.download_file(bucket_name, s3_key, local_file_path)
                print(f"Downloaded: {s3_key} -> {local_file_path}")

        except Exception as e:
            raise XRayException(e, sys)


# For backward compatibility
class S3Sync:
    def __init__(self, bucket_name="lungxray49", s3_prefix="data/", local_dir="artifacts/data"):
        self.bucket_name = bucket_name
        self.s3_prefix = s3_prefix
        self.local_dir = local_dir
        self.s3 = boto3.client('s3')

    def download_folder(self):
        if not os.path.exists(self.local_dir):
            os.makedirs(self.local_dir)

        print(f"Downloading from S3 bucket: {self.bucket_name}/{self.s3_prefix} to {self.local_dir}")
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=self.s3_prefix)

        for item in response.get('Contents', []):
            s3_key = item['Key']
            if s3_key.endswith("/"):
                continue  # skip folders

            local_file_path = os.path.join(self.local_dir, os.path.relpath(s3_key, self.s3_prefix))
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

            self.s3.download_file(self.bucket_name, s3_key, local_file_path)
            print(f"Downloaded: {s3_key} -> {local_file_path}")
