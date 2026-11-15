import asyncio
from unittest.mock import AsyncMock, patch
import pytest
import httpx

BASE_URL = "https://raw.githubusercontent.com/UNDREY123/MatrixGetter/refs/heads/master/tests"


@pytest.mark.parametrize(
    "side_effect",
    [
        # Ошибка сервера 500 Internal Server Error
        httpx.HTTPStatusError(
            "500 Internal Server Error",
            request=httpx.Request("GET", BASE_URL),
            response=httpx.Response(500),
        ),
        # Ошибка сервера 502 Bad Gateway
        httpx.HTTPStatusError(
            "502 Bad Gateway",
            request=httpx.Request("GET", BASE_URL),
            response=httpx.Response(502),
        ),
        # Ошибка клиента 404 Not Found
        httpx.HTTPStatusError(
            "404 Not Found",
            request=httpx.Request("GET", BASE_URL),
            response=httpx.Response(404),
        ),
        # Превышение времени ожидания подключения
        httpx.ConnectTimeout("Connection timed out"),
        # Превышение времени ожидания чтения ответа
        httpx.ReadTimeout("Read timed out"),
        # Отказ в соединении
        httpx.ConnectError("Connection refused"),
        # Общая сетевая ошибка
        httpx.RequestError("Network unreachable"),
    ],
    ids=[
        "server_error_500",
        "server_error_502",
        "not_found_404",
        "connection_timeout",
        "read_timeout",
        "connection_refused",
        "general_network_error",
    ],
)
def test_network_errors(side_effect):
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = side_effect

        with pytest.raises(httpx.HTTPError):
            asyncio.run(get_matrix(f"{BASE_URL}/1x1_matrix.txt"))


@pytest.mark.parametrize(
    "filename, expected_result",
    [
        ("1x1_matrix.txt", [10]),
        ("2x2_matrix.txt", [11, 5, 6, 2]),
        (
                "even_matrix.txt",
                [
                    10, 50, 90, 130, 140, 150, 160, 120, 80,
                    40, 30, 20, 60, 100, 110, 70
                ]
        ),
        (
                "odd_matrix.txt",
                [
                    10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
                    110, 120, 130, 140, 150, 160, 170, 180, 190, 200,
                    210, 220, 230, 240, 250
                ],
        ),
    ],
)
def test_valid_matrices(filename: str, expected_result: list[int]):
    """Проверка корректного скачивания, парсинга и обхода валидных матриц."""
    url = f"{BASE_URL}/{filename}"
    result = asyncio.run(get_matrix(url))
    assert result == expected_result


@pytest.mark.parametrize(
    "filename, expected_error_msg",
    [
        ("empty_file.txt", "Неверный формат матрицы"),
        ("matrix_with_extra_enter.txt", "Неверный формат матрицы"),
        ("matrix_with_extra_separator.txt", "Значениями матрицы должны быть числа"),
        ("matrix_without_1_enter.txt", "Неверный формат матрицы"),
        ("matrix_without_separator.txt", "Неверный формат матрицы"),
        ("non_square_matrix.txt", "Матрица должна быть квадратной"),
        ("random_chars.txt", "Неверный формат матрицы"),
        ("with_different_rows.txt", "Строки матрицы должны быть одного размера"),
        ("with_negative_number.txt", "Числа матрицы должны быть больше 0"),
        ("with_non_number_symbol.txt", "Значениями матрицы должны быть числа"),
    ],
)
def test_invalid_matrices(filename: str, expected_error_msg: str):
    url = f"{BASE_URL}/{filename}"

    with pytest.raises(ValueError, match=expected_error_msg):
        asyncio.run(get_matrix(url))