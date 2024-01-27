import os
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from django.core.files import File
from imagekitio.models.ListAndSearchFileRequestOptions import (
    ListAndSearchFileRequestOptions,
)
from imagekitio.models.results.UploadFileResult import UploadFileResult


class ImageMediaLibrary:
    """
    ImageKit SDK initialization with custom endpoints.
    """

    ImageMedia = None

    ENDPOINT_MAPPING = {
        "main": ("IMAGEKIT_MAIN_ENDPOINT", "main"),
        "preview": ("IMAGEKIT_PREVIEW_ENDPOINT", "preview"),
        "buffer": ("IMAGEKIT_BUFFER_ENDPOINT", "buffer"),
    }

    def __init__(self, endpoint_name):
        """
        ImageKit SDK initialization with custom endpoints.

        Args:
            endpoint_name (str): "main" - Used to store the main User Background Image
                                 "preview" - Used to store the Preview Image (Reduced Quality/Size)
                                 "buffer" - Used as a buffer for exporting Zip File
        """
        if endpoint_name not in self.ENDPOINT_MAPPING:
            raise TypeError("Invalid Endpoint Type Provided")

        endpoint_env_var, folder_name = self.ENDPOINT_MAPPING[endpoint_name]
        endpoint = os.getenv(endpoint_env_var)

        self.folder_name = folder_name

        # ImageKit SDK initialization
        self.ImageMedia = ImageKit(
            private_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),
            public_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
            url_endpoint=endpoint,
        )

    def delete_image(self, image_url: str, user_code: str, image_type: str) -> bool:
        """
        Delete the Image at the Specified Imagekit URL

        Args:
            image_url (str): Actual Image URL to Delete
            user_code (str): the User releated to whom the image should be deleted
            image_type (str): "main" - Used to store the main User Background Image
                              "preview" - Used to store the Preview Image (Reduced Quality/Size)
                              "buffer" - Used as a buffer for exporting Zip File

        Returns:
            bool: True if the Delete Operation was Successful, False Otherwise
        """

        options = ListAndSearchFileRequestOptions(
            tags=user_code,
            path=image_type,
        )

        try:
            image_id = self.ImageMedia.list_files(options=options).list[0].file_id

            result = self.ImageMedia.delete_file(file_id=image_id)

            if result.response_metadata.http_status_code == 200:
                return True

        except Exception as e:
            print(f"Error during image upload: {e}")
            raise

    def upload_image(
        self, image_file: File, tags: list = None, overwrite_status: bool = False
    ) -> UploadFileResult:
        """Upload a Image to the Object specified Endpoint

        Args:
            image_file (File): File object to upload
            tags (list, optional): Tags to be associated with the file. Defaults to None.
            overwrite_status (bool, optional): If a similar image exists, Overwrite it. Defaults to False.

        Returns:
            UploadFileResult: Custom object by ImageKit
        """

        options = UploadFileRequestOptions(
            tags=tags,
            is_private_file=False,
            response_fields=[
                "tags",
                "custom_coordinates",
                "is_private_file",
                "embedded_metadata",
                "custom_metadata",
            ],
            overwrite_file=overwrite_status,
            folder=f"/{self.folder_name}/",
        )

        try:
            result = self.ImageMedia.upload_file(
                file=image_file.read(),  # required
                file_name=image_file.name,  # required
                options=options,
            )

            # Print that uploaded file's ID
            print(result.url)

            print(result.response_metadata.raw)

            return result
        except Exception as e:
            raise
