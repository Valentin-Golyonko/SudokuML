from asgiref.sync import sync_to_async

from app.board.models import Board
from app.core.constants import CoreConstants
from app.core.scripts.sentry_scripts import SendToSentry


class CRUDBoard:

    @staticmethod
    async def get_board(board_id: int) -> Board | None:
        try:
            return await Board.objects.aget(id=board_id)
        except Board.DoesNotExist:
            return None
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"get_board(): Board.get Ex",
                    "level": CoreConstants.SENTRY_MSG_ERROR,
                    "pixel_qa_tag": CoreConstants.SENTRY_TAG_DB_MODEL,
                    "detail": f"{board_id = :,}",
                    "extra_detail": f"{ex = }",
                }
            )
            return None

    @staticmethod
    @sync_to_async
    def boards_ids(
        difficulty: int,
        current_board_id: int,
    ) -> list[int]:
        try:
            return list(
                Board.objects.filter(
                    difficulty=difficulty,
                )
                .exclude(
                    id=current_board_id,
                )
                .values_list(
                    "id",
                    flat=True,
                )
            )
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"boards_ids(): Board.filter Ex",
                    "level": CoreConstants.SENTRY_MSG_ERROR,
                    "pixel_qa_tag": CoreConstants.SENTRY_TAG_DB_MODEL,
                    "detail": f"{difficulty = :,}",
                    "extra_detail": f"{ex = }",
                }
            )
            return []
