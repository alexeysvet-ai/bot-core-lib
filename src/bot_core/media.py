from aiohttp import ClientError
import asyncio
import re
from aiogram import types
from bot_core.utils import log
from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError

MAX_SEND_RETRIES = 3
REQUEST_TIMEOUT = 120
RETRY_DELAY = 2  # секунды


def sanitize_error_text(error) -> str:
    text = str(error)
    return re.sub(r"/bot[^/]+/", "/bot***/", text)


async def send_media_with_retry(
    callback,
    user_id,
    file_path,
    mode,
    title,
    uploader,
    caption,
    retry_text=None,
):
    last_exception = None

    for attempt in range(1, MAX_SEND_RETRIES + 1):
        try:
            log(f"[SEND ATTEMPT {attempt}/{MAX_SEND_RETRIES}] user={user_id} path={file_path}")

            media = types.FSInputFile(file_path)

            if mode == "audio":
                await callback.message.answer_audio(
                    media,
                    title=title,
                    performer=uploader or "",
                    caption=caption,
                    request_timeout = REQUEST_TIMEOUT
                )
            else:
                await callback.message.answer_video(
                    media,
                    caption=caption,
                    request_timeout = REQUEST_TIMEOUT
                )

            log(f"[SEND SUCCESS] user={user_id} attempt={attempt}")
            return  # Успешная отправка

        except TelegramBadRequest as e:
            # Неретраимые ошибки Telegram (например, файл слишком большой)
            log(f"[SEND NON-RETRYABLE] user={user_id} error={sanitize_error_text(e)}")
            raise

        except (TelegramNetworkError, asyncio.TimeoutError, ClientError, OSError) as e:
            last_exception = e
            log(
                f"[SEND ERROR] user={user_id} attempt={attempt} "
                f"type={type(e).__name__} error={sanitize_error_text(e)}"
            )

            if attempt < MAX_SEND_RETRIES:
                # Уведомляем пользователя после первой неудачной попытки
                if attempt == 1 and retry_text:
                    await callback.message.answer(retry_text)
                await asyncio.sleep(RETRY_DELAY)
            else:
                log(f"[SEND FAILED] user={user_id} after {MAX_SEND_RETRIES} attempts")
                #await callback.message.answer(t("send_retry_final_fail", user_id))
                raise last_exception