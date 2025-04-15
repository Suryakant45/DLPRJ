import sys
import os
import shutil

from Xray.cloud_storage.s3_operation import S3Operation
from Xray.constant.training_pipeline import *
from Xray.entity.artifact_entity import DataIngestionArtifact
from Xray.entity.config_entity import DataIngestionConfig
from Xray.exception import XRayException
from Xray.logger import logging


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config

        self.s3 = S3Operation()

    def get_data_from_s3(self) -> None:
        try:
            logging.info("Entered the get_data_from_s3 method of Data ingestion class")

            # Create a mock directory structure instead of downloading from S3
            logging.info("Creating mock directory structure for training data")

            # Create the main data directory
            os.makedirs(self.data_ingestion_config.data_path, exist_ok=True)

            # Create train directory
            os.makedirs(self.data_ingestion_config.train_data_path, exist_ok=True)

            # Create test directory
            os.makedirs(self.data_ingestion_config.test_data_path, exist_ok=True)

            # Create class directories inside train
            os.makedirs(os.path.join(self.data_ingestion_config.train_data_path, "NORMAL"), exist_ok=True)
            os.makedirs(os.path.join(self.data_ingestion_config.train_data_path, "PNEUMONIA"), exist_ok=True)

            # Create class directories inside test
            os.makedirs(os.path.join(self.data_ingestion_config.test_data_path, "NORMAL"), exist_ok=True)
            os.makedirs(os.path.join(self.data_ingestion_config.test_data_path, "PNEUMONIA"), exist_ok=True)

            # Create a dummy image file in each directory
            with open(os.path.join(self.data_ingestion_config.train_data_path, "NORMAL", "dummy.jpg"), "w") as f:
                f.write("dummy image")

            with open(os.path.join(self.data_ingestion_config.train_data_path, "PNEUMONIA", "dummy.jpg"), "w") as f:
                f.write("dummy image")

            with open(os.path.join(self.data_ingestion_config.test_data_path, "NORMAL", "dummy.jpg"), "w") as f:
                f.write("dummy image")

            with open(os.path.join(self.data_ingestion_config.test_data_path, "PNEUMONIA", "dummy.jpg"), "w") as f:
                f.write("dummy image")

            logging.info("Exited the get_data_from_s3 method of Data ingestion class")

        except Exception as e:
            raise XRayException(e, sys)



    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        logging.info(
            "Entered the initiate_data_ingestion method of Data ingestion class"
        )

        try:
            self.get_data_from_s3()

            data_ingestion_artifact: DataIngestionArtifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.train_data_path,
                test_file_path=self.data_ingestion_config.test_data_path,
            )

            logging.info(
                "Exited the initiate_data_ingestion method of Data ingestion class"
            )

            return data_ingestion_artifact

        except Exception as e:
            raise XRayException(e, sys)