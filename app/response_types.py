from typing import Any

from fastapi.responses import ORJSONResponse
from starlette.background import BackgroundTask

from app.settings import settings


class APIResponse(ORJSONResponse):
    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        success: bool = True,
        headers: dict = None,
        media_type: str = None,
        background: BackgroundTask = None,
    ) -> None:
        """
        Initialize an APIResponse instance.

        Args:
            content (Any, optional): The response content. Defaults to None.
            status_code (int, optional): HTTP status code. Defaults to 200.
            success (bool, optional): Flag indicating if the response is successful. Defaults to True.
            headers (dict, optional): HTTP headers to include in the response. Defaults to None.
            media_type (str, optional): The media type of the response. Defaults to None.
            background (BackgroundTask, optional): Background tasks to run after the response is sent. Defaults to None.
        """
        success = self._is_success(success, status_code)
        super().__init__(
            content=self._pre_render(content, success),
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )

    @staticmethod
    def _is_success(success, status_code) -> bool:
        """
        Determine if the response is successful.

        If the status code is not between 200 and 299 (inclusive), the response is not successful.
        Otherwise, the response is successful if and only if the `success` flag is set to `True`.

        Args:
            success (bool): Flag indicating if the response is successful.
            status_code (int): HTTP status code.

        Returns:
            bool: `True` if the response is successful, `False` otherwise.
        """
        if not 200 <= status_code <= 299:
            return False
        return success

    @staticmethod
    def _pre_render(content: Any, success: bool) -> dict:
        """
        Pre-render the response content.

        The response content is wrapped in a dictionary with an appropriate key,
        based on success or failure.
        The "success" key is also set to `True` or `False` accordingly.
        The "version" key is set to the application version.

        Args:
            content (Any): The response content.
            success (bool): Flag indicating if the response is successful.

        Returns:
            dict: The pre-rendered response content.
        """
        data_key = "data" if success else "error"
        return {
            data_key: content or {},
            "success": success,
            "version": settings.VERSION,
        }
