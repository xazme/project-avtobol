from typing import cast
from contextlib import asynccontextmanager
from deepl import DeepLClient

auth_key = "0383824e-9239-468a-b96e-73aa2a6fe273:fx"
# translator = deepl.DeepLClient(auth_key=auth_key)

# result = translator.translate_text(
#     text="Это сообщение было написано с помощью Deepl API. ", target_lang="PL"
# )

# print(result)


class Translator:
    def __init__(
        self,
        auth_key: str,
    ):
        self.auth_key = auth_key

    @asynccontextmanager
    async def get_client(self):
        async with DeepLClient(auth_key=self.auth_key) as client:
            yield cast(DeepLClient, client)

    # TODO
    async def translate_text(
        self,
        text: dict,
        target_language: str,
    ):
        async with self.get_client() as client:
            result = client.translate_text(
                text=text,
                target_language=target_language,
            )
            return result
