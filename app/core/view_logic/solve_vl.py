""""""
import logging
from time import perf_counter
from datetime import timedelta
import asyncio
from random import random, randint
from app.core.sudoku_data.sudoku_data import SudokuData
import numpy as np

from app.socket.socket_scripts.consumers import ChatConsumer

logger = logging.getLogger(__name__)


class SolveVL:
    @classmethod
    async def solve(cls) -> bool:
        logger.debug(f"Sudoku solver started...")
        time_start = perf_counter()

        sudoku_board = SudokuData.SUDOKU_1

        await cls.ws_test(sudoku_board)

        await asyncio.sleep(randint(1, 2) + random())
        time_end = perf_counter()

        logger.info(f"Solve time = {timedelta(seconds=time_end-time_start)}")
        return True

    @staticmethod
    async def ws_test(sudoku_board: list[int]) -> None:
        np_board = np.reshape(a=sudoku_board, newshape=(9, 9))

        for line_index, line in enumerate(np_board):
            for item_index, value in enumerate(line):
                value = int(value)

                position = f"p{line_index}{item_index}"

                if value == 0:
                    for i in range(10):
                        await ChatConsumer.send_ws_msg(
                            position=position, value=i, status=2
                        )
                        await asyncio.sleep(0.1)

                    await ChatConsumer.send_ws_msg(
                        position=position, value=value, status=0
                    )

        return None
