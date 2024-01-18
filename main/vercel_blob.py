from os import getenv
from typing import Any, Optional, Union
from mimetypes import guess_type
import urllib.parse

import requests
from tabulate import tabulate


class VercelBlobClient:
    """
    Class Method Material Taken from https://github.com/misaelnieto/vercel-storage and modified my ChatGPT as of 17/01/2024.
    Original Author: Noe Nieto

    License in: self.LICENSE()
    """

    def __init__(self, token: Optional[str] = None, debug: Optional[bool] = False):
        self.vercel_api_url = "https://blob.vercel-storage.com"
        self.api_version = "4"
        self.default_cache_age = 365 * 24 * 60 * 60  # 1 Year
        self.default_page_size = 100
        self.token = token
        self.debug = debug

    def guess_mime_type(self, url):
        return guess_type(url, strict=False)[0]

    def get_token(self, options: Optional[dict] = None):
        _tkn = (
            options.get("token", getenv("BLOB_READ_WRITE_TOKEN", None))
            if options
            else None
        )
        if not _tkn:
            raise ConfigurationError("Vercel's BLOB_READ_WRITE_TOKEN is not set")
        return _tkn

    def dump_headers(self, options: Optional[dict], headers: dict):
        if options and options.get("debug", False):
            print(tabulate([(k, v) for k, v in headers.items()]))

    def _coerce_bool(self, value):
        return str(int(bool(value)))

    def _handle_response(self, response: requests.Response):
        if str(response.status_code) == "200":
            return response.json()
        raise APIResponseError(f"Oops, something went wrong: {response.json()}")

    def put(self, pathname: str, body: bytes, options: Optional[dict] = None) -> dict:
        _opts = dict(options) if options else dict()
        headers = {
            "access": "public",
            "authorization": f"Bearer {self.get_token(_opts)}",
            "x-api-version": self.api_version,
            "x-content-type": self.guess_mime_type(pathname),
            "x-cache-control-max-age": _opts.get(
                "cacheControlMaxAge", str(self.default_cache_age)
            ),
        }
        if "no_suffix" in options:
            headers["x-add-random-suffix"] = "false"

        self.dump_headers(options, headers)
        _resp = requests.put(
            f"{self.vercel_api_url}/{pathname}", data=body, headers=headers
        )
        return self._handle_response(_resp)

    def delete(
        self, url: Union[str, list[str], tuple[str]], options: Optional[dict] = None
    ) -> dict:
        """
        Deletes a blob object from the Blob store.
        Args:
            url (str|list[str]|tuple[str]): A string or a list of strings specifying the
                unique URL(s) of the blob object(s) to delete.
            options (dict): A dict with the following optional parameter:
                token (Not required) A string specifying the read-write token to
                      use when making requests. It defaults to the BLOB_READ_WRITE_TOKEN
                      environment variable when deployed on Vercel as explained
                      in Read-write token

        Returns:
            None: A delete action is always successful if the blob url exists.
                  A delete action won't throw if the blob url doesn't exists.
        """
        _opts = dict(options) if options else dict()
        headers = {
            "authorization": f"Bearer {self.get_token(_opts)}",
            "x-api-version": self.api_version,
            "content-type": "application/json",
        }
        self.dump_headers(options, headers)
        _resp = requests.post(
            f"{self.vercel_api_url}/delete",
            json={"urls": [url]} if isinstance(url, str) else {"urls": url},
            headers=headers,
        )
        return self._handle_response(_resp)

    def list(self, options: Optional[dict] = None) -> Any:
        """
        The list method returns a list of blob objects in a Blob store.
        Args:
            options (dict): A dict with the following optional parameter:
                token (Not required) A string specifying the read-write token to
                      use when making requests. It defaults to the BLOB_READ_WRITE_TOKEN
                      environment variable when deployed on Vercel as explained
                      in Read-write token
                limit (Not required): A number specifying the maximum number of
                    blob objects to return. It defaults to 1000
                prefix (Not required): A string used to filter for blob objects
                    contained in a specific folder assuming that the folder name was
                    used in the pathname when the blob object was uploaded
                cursor (Not required): A string obtained from a previous response for pagination
                    of retults
                mode (Not required): A string specifying the response format. Can
                    either be "expanded" (default) or "folded". In folded mode
                    all blobs that are located inside a folder will be folded into
                    a single folder string entry

        Returns:
            Json response
        """
        _opts = dict(options) if options else dict()
        headers = {
            "authorization": f"Bearer {self.get_token(_opts)}",
            "limit": _opts.get("limit", str(self.default_page_size)),
        }
        if "prefix" in _opts:
            headers["prefix"] = _opts["prefix"]
        if "cursor" in _opts:
            headers["cursor"] = _opts["cursor"]
        if "mode" in _opts:
            headers["mode"] = _opts["mode"]

        self.dump_headers(options, headers)
        _resp = requests.get(
            self.vercel_api_url,
            headers=headers,
        )
        return self._handle_response(_resp)

    def head(self, url: str, options: Optional[dict] = None) -> dict:
        """
        Returns a blob object's metadata.

        Args:
            url: (Required) A string specifying the unique URL of the blob object to read
            options (dict): A dict with the following optional parameter:
                token (Not required) A string specifying the read-write token to
                      use when making requests. It defaults to the BLOB_READ_WRITE_TOKEN
                      environment variable when deployed on Vercel as explained
                      in Read-write token

        Returns:
            dict: with the blob's metadata. Throws an error if the blob is not found
        """
        _opts = dict(options) if options else dict()
        headers = {
            "authorization": f"Bearer {self.get_token(_opts)}",
            "x-api-version": self.api_version,
        }
        self.dump_headers(options, headers)
        _resp = requests.get(
            f"{self.vercel_api_url}", headers=headers, params={"url": url}
        )
        return self._handle_response(_resp)

    def copy(
        self, from_url: str, to_pathname: str, options: Optional[dict] = None
    ) -> dict:
        """
        Copies an existing blob object to a new path inside the blob store.

        The contentType and cacheControlMaxAge will not be copied from the source
        blob. If the values should be carried over to the copy, they need to be
        defined again in the options object.

        Contrary to put(), addRandomSuffix is false by default. This means no
        automatic random id suffix is added to your blob url, unless you pass
        addRandomSuffix: True. This also means copy() overwrites files per default,
        if the operation targets a pathname that already exists.

        Args:
            from_url: (Required) A blob URL identifying an already existing blob
            to_pathname: (Required) A string specifying the new path inside the blob
                store. This will be the base value of the return URL
            options: A dict with the following optional parameter:
                token (Not required): A string specifying the read-write token to
                      use when making requests. It defaults to the BLOB_READ_WRITE_TOKEN
                      environment variable when deployed on Vercel as explained
                      in Read-write token
                contentType (Not required): A string indicating the media type.
                    By default, it's extracted from the to_pathname's extension.
                addRandomSuffix (Not required): A boolean specifying whether to add
                    a random suffix to the pathname. It defaults to False.
                cacheControlMaxAge (Not required): A number in seconds to configure
                    the edge and browser cache. Defaults to one year. See Vercel's
                    caching documentation for more details.
        """
        _opts = dict(options) if options else dict()
        headers = {
            "access": "public",
            "authorization": f"Bearer {self.get_token(_opts)}",
            "x-api-version": self.api_version,
            "x-content-type": _opts.get("contentType", self.guess_mime_type(from_url)),
            "x-add-random-suffix": self._coerce_bool(
                _opts.get("addRandomSuffix", False)
            ),
            "x-cache-control-max-age": _opts.get(
                "cacheControlMaxAge", str(self.default_cache_age)
            ),
        }
        self.dump_headers(options, headers)
        _to = urllib.parse.quote(to_pathname)
        resp = requests.put(
            f"{self.vercel_api_url}/{_to}",
            headers=headers,
            params={"fromUrl": from_url},
        )
        return self._handle_response(resp)

    def LICENSE(self):
        license_text = """
            MIT License\n

            Copyright (c) 2023 Noe Nieto\n

            Permission is hereby granted, free of charge, to any person obtaining a copy
            of this software and associated documentation files (the "Software"), to deal
            in the Software without restriction, including without limitation the rights
            to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
            copies of the Software, and to permit persons to whom the Software is
            furnished to do so, subject to the following conditions:\n

            The above copyright notice and this permission notice shall be included in all
            copies or substantial portions of the Software.\n

            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
            IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
            FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
            AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
            LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
            OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
            SOFTWARE.\n
            """

        print(license_text)

        return license_text


"""
MIT License

Copyright (c) 2023 Noe Nieto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
# Instantiate the VercelBlobClient
vercel_blob_client = VercelBlobClient(token="your_vercel_token", debug=True)

# Example: Upload a file
file_path = "/path/to/your/file.jpg"
with open(file_path, "rb") as file:
    body = file.read()

pathname = "uploads/file.jpg"
upload_response = vercel_blob_client.put(pathname, body)
print("Upload Response:", upload_response)

# Example: Delete a file
file_url_to_delete = "https://blob.vercel-storage.com/uploads/file.jpg"
delete_response = vercel_blob_client.delete(file_url_to_delete)
print("Delete Response:", delete_response)

# Example: List files
list_response = vercel_blob_client.list()
print("List Response:", list_response)

# Example: Get metadata of a file
file_url_to_get_metadata = "https://blob.vercel-storage.com/uploads/file.jpg"
head_response = vercel_blob_client.head(file_url_to_get_metadata)
print("Head Response:", head_response)

# Example: Copy a file to a new path
from_url = "https://blob.vercel-storage.com/uploads/file.jpg"
to_pathname = "uploads/copied_file.jpg"
copy_response = vercel_blob_client.copy(from_url, to_pathname)
print("Copy Response:", copy_response)

"""
