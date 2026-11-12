import asyncio
import httpx
import logging
from math import ceil
from typing import List

logger = logging.getLogger(__name__)


async def fetch_matrix(url: str) -> str | None:
    timeout = httpx.Timeout(10.0) # Установка времени ожидания

    # Получение матрицы
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.text

        # Обработка ошибок
        except httpx.TimeoutException:
            logger.error(f"Превышено время ожидания ответа от {url}")
        except httpx.HTTPStatusError as exc:
            logger.error(f"Ошибка сервера {exc.response.status_code} при запросе к {url}")
        except httpx.RequestError as exc:
            logger.error(f"Сетевая ошибка при подключении к {url}: {exc}")

    return None


async def get_matrix(url: str) -> List[int]:
    """
    Возвращает матрицу в виде списка, содержащего результат обхода полученной
    матрицы по спирали: против часовой стрелки, начиная с левого верхнего угла
    """
    # Получение матрицы
    text_matrix = await fetch_matrix(url)
    if not text_matrix:
        return []

    # Преобразование матрицы из текстового вида во вложенные списки
    matrix: List[List[int]] = []
    matrix_rows = text_matrix.split("\n")
    for i in range(len(matrix_rows) - 1):
        print(matrix_rows[i])
    for i in range(len(matrix_rows) - 1):
        if i % 2 == 1:
            new_row = list(map(int, matrix_rows[i].split("|")[1:-1]))
            matrix.append(new_row)

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

async def main():
    url = "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"
    matrix = await get_matrix(url)
    print(matrix)

if __name__ == "__main__":
    asyncio.run(main())