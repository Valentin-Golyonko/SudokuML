import numpy as np

from app.board.sudoku_data.sudoku_data import SudokuData


class SudokuVL:
    @staticmethod
    async def get_sudoku_game():
        np_board = np.reshape(a=SudokuData.DEFAULT, newshape=(9, 9))

        out_data = {}

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

                out_data.update(tmp_data)

        return out_data
