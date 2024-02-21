import numpy as np

from app.board.crud.crud_board import CRUDBoard


class SudokuVL:
    @staticmethod
    async def get_sudoku_game(board_id: int) -> tuple[bool, dict, str]:

        board_obj = await CRUDBoard.get_board(board_id)
        if board_obj is None:
            return False, {}, "Can not get board."

        np_board = np.reshape(a=board_obj.data, newshape=(9, 9))

        board = {}

        out_data = {
            "board_id": board_id,
            "board": board,
        }

        for line_index, line in enumerate(np_board):
            for item_index, value in enumerate(line):
                """
                p00: {
                  value: 0,
                  base: true,
                },
                """

                tmp_data = {
                    f"p{line_index}{item_index}": {
                        "value": int(value),
                        "base": 1 if value != 0 else 0,
                    }
                }

                board.update(tmp_data)

        return True, out_data, ""
