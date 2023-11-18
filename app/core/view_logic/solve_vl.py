""""""
import logging
from time import perf_counter
from datetime import timedelta
import asyncio
from random import random, randint
from app.core.sudoku_data.sudoku_data import SudokuData

logger = logging.getLogger(__name__)


class SolveVL:
    @classmethod
    async def solve(cls) -> bool:
        logger.debug(f"Sudoku solver started...")
        time_start = perf_counter()

        sudoku_board = SudokuData.SUDOKU_1

        await asyncio.sleep(randint(1, 3) + random())
        time_end = perf_counter()

        logger.info(f"Solve time = {timedelta(seconds=time_end-time_start)}")
        return True
