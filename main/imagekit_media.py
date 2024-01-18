from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

import os


class ImageMediaLibrary:
    """
    Requires the Environment Variables to be set as:
        Keys:
            IMAGEKIT_PUBLIC_KEY, IMAGEKIT_PRIVATE_KEY

        Endpoints:
            IMAGEKIT_MAIN_ENDPOINT, IMAGEKIT_PREVIEW_ENDPOINT, IMAGEKIT_BUFFER_ENDPOINT
    """

    def __init__(self, endpoint_name):
        """imagekit SDK initialization with custom endpoints

        Args:
            endpoint_name (str): main - used to store the main User Background Image
                                 preview - used to store the Preview Image (Reduced Quality/Size)
                                 buffer - used as buffer for exporting Zip File
        """
        if endpoint_name == "main":
            endpoint = os.getenv("IMAGEKIT_MAIN_ENDPOINT")

        elif endpoint_name == "preview":
            endpoint = os.getenv("IMAGEKIT_PREVIEW_ENDPOINT")

        elif endpoint_name == "buffer":
            endpoint = os.getenv("IMAGEKIT_BUFFER_ENDPOINT")

        else:
            raise TypeError("Invaid Endpoint Type Provided")

        # imagekit SDK initialization
        self.ImageMedia = ImageKit(
            private_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),
            public_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
            url_endpoint=endpoint,
        )

    def upload_file(
        self, filename: str, tags: list = None, overwrite_status: bool = False
    ) -> UploadFileResult:
        """Upload a file to the Object specified Endpoint

        Args:
            filename (str): Required File name including extension
            tags (list, optional): Tags to be associated with the file. Defaults to None.
            overwrite_status (bool, optional): If a similar image exists, Overwrite it. Defaults to False.

        Returns:
            UploadFileResult: custom object by imagekit
        """

        # extensions = [
        #     {"name": "remove-bg", "options": {"add_shadow": True, "bg_color": "pink"}},
        #     {"name": "google-auto-tagging", "minConfidence": 80, "maxTags": 10},
        # ]

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
            # folder="/testing-python-folder/",
            # custom_coordinates="10,10,20,20",
            # extensions=None,
            # webhook_url="https://webhook.site/c78d617f-33bc-40d9-9e61-608999721e2e",
            # overwrite_ai_tags=False,
            # overwrite_tags=False,
            # overwrite_custom_metadata=True,
            # custom_metadata={"testss": 12},
        )

        result = self.ImageMedia.upload_file(
            file="<url|base_64|binary>",  # required
            file_name=filename,  # required
            options=options,
        )

        # Final Result
        print(result)

        # Raw Response
        print(result.response_metadata.raw)

        # print that uploaded file's ID
        print(result.url)

        return result
