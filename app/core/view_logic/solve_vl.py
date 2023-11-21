""""""
import logging
from datetime import timedelta
from time import perf_counter

import numpy as np

from app.core.constants import CoreConstants
from app.core.sudoku_data.sudoku_data import SudokuData
from app.socket.socket_scripts.consumers import ChatConsumer

logger = logging.getLogger(__name__)


class SolveVL:
    @classmethod
    async def solve(cls) -> bool:
        logger.debug(f"Sudoku solver started...")
        time_start = perf_counter()

        sudoku_board = SudokuData.SUDOKU_1

        steps = await cls.solve_loop(sudoku_board)

        time_end = perf_counter()

        logger.info(
            f"Solved; {steps = :,}, time = {timedelta(seconds=time_end - time_start)}"
        )
        return True

    @classmethod
    async def solve_loop(cls, sudoku_board: list[int]) -> int:
        np_board: np.ndarray = np.reshape(a=sudoku_board, newshape=(9, 9))

        # sudoku_board_2 = [[i, list(range(10))] for i in sudoku_board]
        # sudoku_board_3 = [list(range(10)) for i in sudoku_board]

        """
        np_board[:,2] ->
            array([0, 0, 7, 6, 4, 0, 0, 0, 0])
        
        np_board[:,0:3] -> 
            array([[1, 0, 0],
                   [6, 0, 0],
                   [0, 4, 7],
                   [0, 0, 6],
                   [0, 0, 4],
                   [9, 0, 0],
                   [2, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0]])
        
        np_board[0:3,0:3] -> 
            array([[1, 0, 0],
                   [6, 0, 0],
                   [0, 4, 7]])
        """

        zeros = len([i for i in sudoku_board if i == 0])
        for step in range(zeros):
            if np_board.all():
                return step

            for line_index, line in enumerate(np_board):
                for item_index, value in enumerate(line):
                    if value != 0:
                        continue

                    await cls.solver(np_board, line_index, item_index)

        return zeros

    @classmethod
    async def solver(
        cls,
        np_board: np.ndarray,
        line_index: int,
        item_index: int,
    ) -> None:
        """sudoku solver"""

        position = f"p{line_index}{item_index}"
        # if position == "p05":
        #     print()

        """board sector/cube with clean values"""
        cube, cube_values_clean = cls.get_cube_values(np_board, line_index, item_index)

        """vertical and horizontal arrays with clean values"""
        v_arr_clean, h_arr_clean = cls.get_vh_values(np_board, line_index, item_index)

        forbidden_values = sorted({*cube_values_clean, *v_arr_clean, *h_arr_clean})

        allowed_values = sorted(set(range(1, 10)).difference(forbidden_values))

        if len(allowed_values) == 1:
            allowed_value = allowed_values[0]
            np_board[line_index, item_index] = allowed_value
            await ChatConsumer.send_ws_msg(
                position=position,
                value=allowed_value,
                status=CoreConstants.STATUS_SOLVED,
            )
            return None

        h_cube_2_values_clean, h_cube_3_values_clean = cls.get_horizontal_cubes_values(
            np_board, line_index, item_index
        )

        v_cube_2_values_clean, v_cube_3_values_clean = cls.get_vertical_cubes_values(
            np_board, line_index, item_index
        )

        for av in allowed_values:
            av_in_h_cube_2 = av in h_cube_2_values_clean
            av_in_h_cube_3 = av in h_cube_3_values_clean

            av_in_v_cube_2 = av in v_cube_2_values_clean
            av_in_v_cube_3 = av in v_cube_3_values_clean

            av_in_vh_cubes = all(
                [av_in_h_cube_2, av_in_h_cube_3, av_in_v_cube_2, av_in_v_cube_3]
            )

            if av_in_vh_cubes:
                np_board[line_index, item_index] = av
                await ChatConsumer.send_ws_msg(
                    position=position,
                    value=av,
                    status=CoreConstants.STATUS_SOLVED,
                )
                return None

            await ChatConsumer.send_ws_msg(
                position=position,
                value=av,
                status=CoreConstants.STATUS_WIP,
            )

        await ChatConsumer.send_ws_msg(
            position=position,
            value=0,
            status=CoreConstants.STATUS_ZERO,
        )
        return None

    @staticmethod
    def get_cube_values(
        np_board: np.ndarray,
        line_index: int,
        item_index: int,
    ) -> tuple[np.ndarray, list[int]]:
        """
        np_board[0:3,0:3] ->
         array([[1, 0, 0],
                [6, 0, 0],
                [0, 4, 7]])
        """

        if line_index in range(0, 3):
            x1 = 0
            x2 = 3
        elif line_index in range(3, 6):
            x1 = 3
            x2 = 6
        else:
            x1 = 6
            x2 = 9

        if item_index in range(0, 3):
            y1 = 0
            y2 = 3
        elif item_index in range(3, 6):
            y1 = 3
            y2 = 6
        else:
            y1 = 6
            y2 = 9

        cube = np_board[x1:x2, y1:y2]

        cube_values = cube.reshape(1, 9)[0]
        cube_values_clean = sorted([i for i in cube_values.tolist() if i != 0])

        return cube, cube_values_clean

    @staticmethod
    def get_vh_values(
        np_board: np.ndarray,
        line_index: int,
        item_index: int,
    ) -> tuple[list[int], list[int]]:
        """
        np_board[:,2] ->
            array([0, 0, 7, 6, 4, 0, 0, 0, 0])
        """

        v_arr = np_board[:, item_index]
        v_arr_clean = sorted([i for i in v_arr.tolist() if i != 0])

        h_arr = np_board[line_index, :]
        h_arr_clean = sorted([i for i in h_arr.tolist() if i != 0])

        return v_arr_clean, h_arr_clean

    @staticmethod
    def get_horizontal_cubes_values(
        np_board: np.ndarray,
        line_index: int,
        item_index: int,
    ) -> tuple[list[int], list[int]]:
        """tba"""

        if line_index in range(0, 3):
            x1 = 0
            x2 = 3
        elif line_index in range(3, 6):
            x1 = 3
            x2 = 6
        else:
            x1 = 6
            x2 = 9

        if item_index in range(0, 3):
            cube_2 = np_board[x1:x2, 3:6]
            cube_3 = np_board[x1:x2, 6:9]
        elif item_index in range(3, 6):
            cube_2 = np_board[x1:x2, 0:3]
            cube_3 = np_board[x1:x2, 6:9]
        else:
            cube_2 = np_board[x1:x2, 0:3]
            cube_3 = np_board[x1:x2, 3:6]

        cube_2_values = cube_2.reshape(1, 9)[0]
        cube_2_values_clean = sorted([i for i in cube_2_values.tolist() if i != 0])

        cube_3_values = cube_3.reshape(1, 9)[0]
        cube_3_values_clean = sorted([i for i in cube_3_values.tolist() if i != 0])

        return cube_2_values_clean, cube_3_values_clean

    @staticmethod
    def get_vertical_cubes_values(
        np_board: np.ndarray,
        line_index: int,
        item_index: int,
    ) -> tuple[list[int], list[int]]:
        """tba"""

        if item_index in range(0, 3):
            y1 = 0
            y2 = 3
        elif item_index in range(3, 6):
            y1 = 3
            y2 = 6
        else:
            y1 = 6
            y2 = 9

        if line_index in range(0, 3):
            cube_2 = np_board[3:6, y1:y2]
            cube_3 = np_board[6:9, y1:y2]
        elif line_index in range(3, 6):
            cube_2 = np_board[0:3, y1:y2]
            cube_3 = np_board[6:9, y1:y2]
        else:
            cube_2 = np_board[0:3, y1:y2]
            cube_3 = np_board[3:6, y1:y2]

        cube_2_values = cube_2.reshape(1, 9)[0]
        cube_2_values_clean = sorted([i for i in cube_2_values.tolist() if i != 0])

        cube_3_values = cube_3.reshape(1, 9)[0]
        cube_3_values_clean = sorted([i for i in cube_3_values.tolist() if i != 0])

        return cube_2_values_clean, cube_3_values_clean
