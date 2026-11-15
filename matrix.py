import logging
from math import ceil
from typing import List

import httpx

__all__ = ["get_matrix"]

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

async def _fetch_matrix(url: str) -> str:
    timeout = httpx.Timeout(10.0) # Установка времени ожидания

    # Получение матрицы
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()

        # Обработка ошибок
        except httpx.TimeoutException:
            logger.error(f"Превышено время ожидания при запросе к {url}")
            raise

        except httpx.ConnectError as exc:
            logger.error(f"Не удалось установить соединение с {url}: {exc}")
            raise

        except httpx.HTTPStatusError as exc:
            logger.error(f"Сервер {url} вернул ошибку: HTTP {exc.response.status_code}")
            raise

        except httpx.RequestError as exc:
            logger.error(f"Сетевая ошибка при запросе к {url}: {exc}")
            raise

        else:
            return response.text


def _matrix_parser(matrix: List[List[int]]) -> List[int]:
    # Создание из матрицы списка путём обхода
    matrix_list: List[int] = []
    matrix_size = len(matrix)

    for layer in range(ceil(size / 2)):
        end = size - layer
        # Левая часть
        for row in range(layer, end):
            result.append(matrix[row][layer])
        # Нижняя часть
        for col in range(layer + 1, end):
            result.append(matrix[end - 1][col])
        # Правая часть
        for row in range(end - 2, layer - 1, -1):
            result.append(matrix[row][end - 1])
        # Верхняя часть
        for col in range(end - 2, layer, -1):
            result.append(matrix[layer][col])

    return matrix_list


async def get_matrix(url: str) -> List[int]:
    """
    Возвращает матрицу в виде списка, содержащего результат обхода полученной
    матрицы по спирали: против часовой стрелки, начиная с левого верхнего угла
    """
    # Получение матрицы
    text_matrix = await _fetch_matrix(url)

    # Преобразование матрицы из текстового вида во вложенные списки
    matrix_rows = text_matrix.split("\n")
    if len(matrix_rows) < 3 or "" in matrix_rows:
        raise ValueError("Неверный формат матрицы")

    matrix: List[List[int]] = []
    expected_row_len: int | None = None

    for i in range(1, len(matrix_rows) - 1, 2):
        row_cells = matrix_rows[i].split("|")
        if row_cells[0] != "" or row_cells[-1] != "":
            raise ValueError("Неверный формат матрицы")

        parsed_row: List[int] = []
        for cell in row_cells[1:-1]:
            try:
                number = int(cell)
            except ValueError as exc:
                raise ValueError("Значениями матрицы должны быть числа") from exc

            if number < 0:
                raise ValueError("Числа матрицы должны быть больше 0")

            parsed_row.append(number)

        if expected_row_len is None:
            expected_row_len = len(parsed_row)
        elif len(parsed_row) != expected_row_len:
            raise ValueError("Строки матрицы должны быть одного размера")

        matrix.append(parsed_row)

    if not matrix or len(matrix) != len(matrix[0]):
        raise ValueError("Матрица должна быть квадратной")

    return _matrix_parser(matrix)