import asyncio
import httpx
import logging
from math import ceil
from typing import List

__all__ = ["get_matrix"]

logger = logging.getLogger(__name__)


async def _fetch_matrix(url: str) -> str | None:
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

    for curr_iter in range(ceil(matrix_size / 2)):
        # Левая часть
        for j_left in range(curr_iter, matrix_size - curr_iter * 2 + curr_iter):
            matrix_list.append(matrix[j_left][curr_iter])
        # Нижняя часть
        for j_down in range(curr_iter + 1, matrix_size - curr_iter * 2 + curr_iter):
            matrix_list.append(matrix[matrix_size - (curr_iter + 1)][j_down])
        # Правая часть
        for j_right in range(matrix_size - curr_iter - 2, curr_iter - 1, -1):
            matrix_list.append(matrix[j_right][matrix_size - (curr_iter + 1)])
        # Верхняя часть
        for j_top in range(matrix_size - curr_iter - 2, curr_iter, -1):
            matrix_list.append(matrix[curr_iter][j_top])

    return matrix_list


async def get_matrix(url: str) -> List[int]:
    """
    Возвращает матрицу в виде списка, содержащего результат обхода полученной
    матрицы по спирали: против часовой стрелки, начиная с левого верхнего угла
    """
    # Получение матрицы
    # text_matrix = await _fetch_matrix(url)
    text_matrix = "+-----+\n| 507 | 56 |\n----+\n"
    if not text_matrix:
        return []

    # Преобразование матрицы из текстового вида во вложенные списки
    matrix: List[List[int]] = []
    matrix_rows = text_matrix.split("\n")
    matrix_size = -1
    for i in range(1, len(matrix_rows) - 1, 2):
        matrix.append([])
        for j in matrix_rows[i].split("|")[1:-1]:
            try:
                number = int(j)
            except ValueError:
                raise ValueError(f"Значениями матрицы должны быть числа")
            else:
                if number < 0:
                    raise ValueError(f"Числа матрицы должны быть больше 0")
                matrix[i // 2].append(number)
        if matrix_size == -1:
            matrix_size = len(matrix[0])
        if len(matrix[i // 2]) != matrix_size:
            raise ValueError("Строки матрицы должны быть одного размера")
    if len(matrix) != len(matrix[0]):
        raise ValueError("Матрица должна быть квадратной")
    return _matrix_parser(matrix)


async def main():
    url = "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"
    matrix = await get_matrix(url)
    print(matrix)

if __name__ == "__main__":
    asyncio.run(main())