""""""

import logging

import numpy as np

from app.board.crud.crud_board import CRUDBoard
from app.core.constants import CoreConstants
from app.core.scripts.utils import time_it
from app.socket.socket_scripts.consumers import ChatConsumer

logger = logging.getLogger(__name__)


class SolveVL:
    """"""

    @classmethod
    @time_it
    async def solve(cls, board_id: int) -> tuple[bool, dict, str]:
        logger.debug(f"Sudoku solver started...")

        board_obj = await CRUDBoard.get_board(board_id)
        if board_obj is None:
            return False, {}, "Can not get board."

        steps = await cls.solve_loop(board_obj.data)

        logger.info(f"Solved; {steps = :,}")

        return True, {}, ""

    @classmethod
    async def solve_loop(cls, sudoku_board: list[int]) -> int:
        np_board: np.ndarray = np.reshape(a=sudoku_board, newshape=(9, 9))

        """
        sudoku_board_2d = [list(range(10)) for i in sudoku_board]
        np_board_3d = np.reshape(a=sudoku_board_2d, newshape=(9, 9, 10))
        
        sudoku_board_3d = [[[i, *[0 for _ in range(9)]], list(range(10))] for i in sudoku_board]
        np_board_4d = np.reshape(a=sudoku_board_3d, newshape=(9, 9, 2, 10))
        """

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

        """create a dict that contains 0-9 ints possible for avery position."""
        remaining_values = {}
        for line_index, line in enumerate(np_board):
            for item_index, value in enumerate(line):
                position = f"p{line_index}{item_index}"
                if value != 0:
                    remaining_values[position] = []
                else:
                    remaining_values[position] = [i for i in range(10)]

        """main loop"""
        zeros_count = len([i for i in sudoku_board if i == 0])
        for step in range(zeros_count):
            if np_board.all():
                """exit if solved == all positions filled."""
                return step

            for line_index, line in enumerate(np_board):
                for item_index, value in enumerate(line):
                    """
                    double loop for avery non zero position.
                    from left (top) to right (top),
                    from top to bottom.
                    """
                    if value != 0:
                        continue

                    await cls.solver(np_board, line_index, item_index, remaining_values)

        return zeros_count

    @classmethod
    async def solver(
        cls,
        np_board: np.ndarray,
        line_index: int,
        item_index: int,
        remaining_values: dict[str, list[int]],
    ) -> None:
        """
        sudoku solver.
        modifies np_board in place.
        """

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
            remaining_values[position] = []
            await ChatConsumer.send_ws_msg(
                position=position,
                value=allowed_value,
                status=CoreConstants.STATUS_SOLVED,
            )
            return None

        neighbor_values = cls.get_neighbor_values(
            np_board, line_index, item_index, remaining_values
        )

        # h_cube_2_values_clean, h_cube_3_values_clean = cls.get_horizontal_cubes_values(
        #     np_board, line_index, item_index
        # )
        #
        # v_cube_2_values_clean, v_cube_3_values_clean = cls.get_vertical_cubes_values(
        #     np_board, line_index, item_index
        # )

        for av in allowed_values:
            if av not in neighbor_values:
                np_board[line_index, item_index] = av
                remaining_values[position] = []
                await ChatConsumer.send_ws_msg(
                    position=position,
                    value=av,
                    status=CoreConstants.STATUS_SOLVED,
                )
                return None

            # av_in_h_cube_2 = av in h_cube_2_values_clean
            # av_in_h_cube_3 = av in h_cube_3_values_clean
            #
            # av_in_v_cube_2 = av in v_cube_2_values_clean
            # av_in_v_cube_3 = av in v_cube_3_values_clean
            #
            # av_in_vh_cubes = all(
            #     [av_in_h_cube_2, av_in_h_cube_3, av_in_v_cube_2, av_in_v_cube_3]
            # )
            #
            # if av_in_vh_cubes:
            #     np_board[line_index, item_index] = av
            #     remaining_values[position] = []
            #     await ChatConsumer.send_ws_msg(
            #         position=position,
            #         value=av,
            #         status=CoreConstants.STATUS_SOLVED,
            #     )
            #     return None

            await ChatConsumer.send_ws_msg(
                position=position,
                value=av,
                status=CoreConstants.STATUS_WIP,
            )

        remaining_values[position] = allowed_values

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

    @staticmethod
    def get_neighbor_values(
        np_board: np.ndarray,
        line_index: int,
        item_index: int,
        remaining_values: dict[str, list[int]],
    ) -> set[int]:
        """tba"""

        if line_index in range(0, 3):
            x = list(range(0, 3))
        elif line_index in range(3, 6):
            x = list(range(3, 6))
        else:
            x = list(range(6, 9))

        if item_index in range(0, 3):
            y = list(range(0, 3))
        elif item_index in range(3, 6):
            y = list(range(3, 6))
        else:
            y = list(range(6, 9))

        neighbor_values = set()
        for x_pos in x:
            for y_pos in y:
                if x_pos == line_index and y_pos == item_index:
                    continue

                rv = remaining_values.get(f"p{x_pos}{y_pos}", [])
                neighbor_values.update(rv)

        return neighbor_values
