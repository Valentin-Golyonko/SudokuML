import logging

from sentry_sdk import capture_message, push_scope

from app.core.constants import CoreConstants
from dj_config.settings import USE_SENTRY

logger = logging.getLogger(__name__)


class SendToSentry:
    @staticmethod
    def send_msg(msg: str, msg_lvl: str) -> None:
        """
        Usage:
            from app.core.scripts.sentry_scripts import SendToSentry
            from app.core.constants import CoreConstants
            SendToSentry.send_msg(msg, CoreConstants.SENTRY_MSG_ERROR)
        """
        if USE_SENTRY:
            capture_message(msg, level=msg_lvl)
        return None

    @staticmethod
    def send_scope_msg(scope_data: dict) -> None:
        """
        Usage:
            from app.core.scripts.sentry_scripts import SendToSentry
            from app.core.constants import CoreConstants

            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"Test_message",
                    "level": CoreConstants.SENTRY_MSG_ERROR,
                    "bfi_tag": CoreConstants.SENTRY_TAG_DB_MODEL,
                    "detail": f"Detail_text",
                    "extra_detail": f"{ex = }",
                }
            )
        """
        message = scope_data.get("message")
        level = scope_data.get("level")
        bfi_tag = scope_data.get("bfi_tag")
        detail = scope_data.get("detail")
        extra_detail = scope_data.get("extra_detail")

        if USE_SENTRY:
            with push_scope() as scope:
                scope.set_tag(key="bfi_tag", value=bfi_tag)
                scope.set_extra(key="detail", value=detail)
                scope.set_extra(key="extra_detail", value=extra_detail)
                if level == CoreConstants.SENTRY_MSG_INFO:
                    scope.clear_breadcrumbs()
                capture_message(message=message, level=level)
        else:
            """if debug"""
            logger_msg = f"{message} | {detail} | {extra_detail} | {bfi_tag}"

            if level == CoreConstants.SENTRY_MSG_DEBUG:
                logger.debug(logger_msg)
            elif level == CoreConstants.SENTRY_MSG_INFO:
                logger.info(logger_msg)
            elif level == CoreConstants.SENTRY_MSG_WARNING:
                logger.warning(logger_msg)
            else:
                logger.error(logger_msg)

        return None
