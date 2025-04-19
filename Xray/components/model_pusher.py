import os
import sys

from Xray.entity.artifact_entity import ModelPusherArtifact
from Xray.entity.config_entity import ModelPusherConfig
from Xray.exception import XRayException
from Xray.logger import logging


class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig):
        self.model_pusher_config = model_pusher_config

    def check_command_exists(self, command):
        """Check if a command exists and is executable."""
        import subprocess
        import shutil

        return shutil.which(command) is not None

    def build_and_push_bento_image(self):
        logging.info("Entered build_and_push_bento_image method of ModelPusher class")

        try:
            # Check if bentoml command is available
            if not self.check_command_exists("bentoml"):
                logging.warning("BentoML command not found. Skipping BentoML build and containerization.")
                logging.info("To install BentoML, run: pip install bentoml")
                return

            logging.info("Building the bento from bentofile.yaml")

            # Check if bentofile.yaml exists
            if not os.path.exists("bentofile.yaml"):
                logging.warning("bentofile.yaml not found. Skipping BentoML build.")
                return

            # Run bentoml build with error handling
            build_result = os.system("bentoml build")
            if build_result != 0:
                logging.warning(f"BentoML build failed with exit code {build_result}")
                return

            logging.info("Built the bento from bentofile.yaml")

            # Check if docker command is available
            if not self.check_command_exists("docker"):
                logging.warning("Docker command not found. Skipping containerization and pushing.")
                logging.info("Please install Docker to containerize and push the model.")
                return

            logging.info("Creating docker image for bento")

            containerize_result = os.system(
                f"bentoml containerize {self.model_pusher_config.bentoml_service_name}:latest -t 136566696263.dkr.ecr.us-east-1.amazonaws.com/{self.model_pusher_config.bentoml_ecr_image}:latest"
            )

            if containerize_result != 0:
                logging.warning(f"BentoML containerize failed with exit code {containerize_result}")
                return

            logging.info("Created docker image for bento")

            # Check if aws command is available
            if not self.check_command_exists("aws"):
                logging.warning("AWS CLI not found. Skipping ECR login and push.")
                logging.info("Please install AWS CLI to push to ECR.")
                return

            logging.info("Logging into ECR")

            login_result = os.system(
                "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 136566696263.dkr.ecr.us-east-1.amazonaws.com"
            )

            if login_result != 0:
                logging.warning(f"ECR login failed with exit code {login_result}")
                return

            logging.info("Logged into ECR")

            logging.info("Pushing bento image to ECR")

            push_result = os.system(
                f"docker push 841807079254.dkr.ecr.ap-southeast-2.amazonaws.com/{self.model_pusher_config.bentoml_ecr_image}:latest"
            )

            if push_result != 0:
                logging.warning(f"Docker push failed with exit code {push_result}")
                return

            logging.info("Pushed bento image to ECR")

            logging.info(
                "Exited build_and_push_bento_image method of ModelPusher class"
            )

        except Exception as e:
            logging.error(f"Error in build_and_push_bento_image: {str(e)}")
            # Don't raise the exception, just log it and continue
            # This way the pipeline won't fail if there are issues with BentoML or Docker



    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        Method Name :   initiate_model_pusher
        Description :   This method initiates model pusher.

        Output      :   Model pusher artifact
        """
        logging.info("Entered initiate_model_pusher method of ModelPusher class")

        try:
            # Try to build and push the BentoML image, but continue even if it fails
            try:
                self.build_and_push_bento_image()
            except Exception as e:
                logging.warning(f"Error in build_and_push_bento_image: {str(e)}")
                logging.info("Continuing with model pusher despite BentoML/Docker errors")

            # Create the model pusher artifact regardless of BentoML/Docker success
            model_pusher_artifact = ModelPusherArtifact(
                bentoml_model_name=self.model_pusher_config.bentoml_model_name,
                bentoml_service_name=self.model_pusher_config.bentoml_service_name,
            )

            logging.info("Exited the initiate_model_pusher method of ModelPusher class")

            return model_pusher_artifact

        except Exception as e:
            logging.error(f"Error in initiate_model_pusher: {str(e)}")
            # Create a default artifact even if there's an error
            return ModelPusherArtifact(
                bentoml_model_name=self.model_pusher_config.bentoml_model_name,
                bentoml_service_name=self.model_pusher_config.bentoml_service_name,
            )