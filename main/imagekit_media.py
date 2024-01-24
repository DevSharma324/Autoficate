from imagekitio import ImageKit

from django.core.files import File
from imagekitio.models.ListAndSearchFileRequestOptions import (
    ListAndSearchFileRequestOptions,
)
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from imagekitio.models.results.UploadFileResult import UploadFileResult

import os


class ImageMediaLibrary:
    """
    ImageKit SDK initialization with custom endpoints.
        Args:
            endpoint_name (str):
                "main" - Used to store the main User Background Image
                "preview" - Used to store the Preview Image (Reduced Quality/Size)
                "buffer" - Used as a buffer for exporting Zip File

    Requires the following Environment Variables to be set:
        Keys:
            IMAGEKIT_PUBLIC_KEY, IMAGEKIT_PRIVATE_KEY

        Endpoints:
            IMAGEKIT_MAIN_ENDPOINT, IMAGEKIT_PREVIEW_ENDPOINT, IMAGEKIT_BUFFER_ENDPOINT

    """

    ImageMedia = None
    
    def __init__(self, endpoint_name):
        """
        ImageKit SDK initialization with custom endpoints.

        Args:
            endpoint_name (str): "main" - Used to store the main User Background Image
                                 "preview" - Used to store the Preview Image (Reduced Quality/Size)
                                 "buffer" - Used as a buffer for exporting Zip File
        """
        if endpoint_name == "main":
            endpoint = os.getenv("IMAGEKIT_MAIN_ENDPOINT")
            self.folder_name = "main"

        elif endpoint_name == "preview":
            endpoint = os.getenv("IMAGEKIT_PREVIEW_ENDPOINT")
            self.folder_name = "preview"

        elif endpoint_name == "buffer":
            endpoint = os.getenv("IMAGEKIT_BUFFER_ENDPOINT")
            self.folder_name = "buffer"

        else:
            raise TypeError("Invalid Endpoint Type Provided")

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
            # type="file",
            # sort="ASC_CREATED",
            path=image_type,
            # search_query=f'tags IN ["{user_code}"]',
            # file_type="all",
            # limit=5,
            # skip=0,
            tags=user_code,
        )

        try:
            image_id = imagekit.list_files(options=options).list[0].file_id

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
            self.result = self.ImageMedia.upload_file(
                file=image_file.read(),  # required
                file_name=image_file.name,  # required
                options=options,
            )

            # Print that uploaded file's ID
            print(self.result.url)
            
            print(self.result.response_metadata.raw)

            return self.result
        except Exception as e:
            print(f"Error during image upload: {e}")
            print(f"Exception Type: {type(e).__name__}")  # Print the type of the exception
            print(f"Exception Details: {str(e)}")         # Print the details of the exception

            print(e.response_metadata.headers)
            print(e.response_metadata.raw)
            
            # Optionally, print the traceback for more detailed information
            import traceback
            traceback.print_exc()
            
            raise
