from httpx import AsyncClient, Response, HTTPStatusError, RequestError
from app.shared import ExceptionRaiser


class Translator:
    def __init__(
        self,
        auth_key: str,
        base_url: str,
    ):
        self.auth_key = auth_key
        self.base_url = base_url

    async def translate_text(
        self,
        text: str,
        target_lang: str = "ENG",
    ):
        async with AsyncClient(
            timeout=10,
            headers=self._get_headers(),
        ) as client:
            try:
                data = {
                    "text": [text],
                    "target_lang": target_lang,
                }
                response: Response = await client.post(
                    url=self.base_url,
                    json=data,
                )

                translated_text: dict = response.json()
                data = translated_text.get("translations")
                return data[0].get("text")

            except HTTPStatusError as exc:
                ExceptionRaiser.raise_exception(
                    status_code=exc.response.status_code,
                    detail="Сервер DeepL вернул ошибку. Попробуйте позже.",
                )

            except RequestError:
                ExceptionRaiser.raise_exception(
                    status_code=503,
                    detail="Сетевая ошибка. DeepL временно недоступен.",
                )

            except Exception:
                ExceptionRaiser.raise_exception(
                    status_code=500,
                    detail="Не удалось выполнить перевод. Попробуйте позже.",
                )

    def _get_headers(self):
        headers = {
            "Authorization": f"DeepL-Auth-Key {self.auth_key}",
            "Content-Type": "application/json",
        }
        return headers
