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
        success = self._is_success(success, status_code)
        super().__init__(
            content=self._pre_render(content, success),
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )

    @staticmethod
    def _is_success(success, status_code):
        if not 200 <= status_code <= 299:
            return False
        return success

    @staticmethod
    def _pre_render(content: Any, success: bool) -> dict:
        data_key = "data" if success else "error"
        return {
            data_key: content or {},
            "success": success,
            "version": settings.VERSION,
        }