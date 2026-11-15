# MatrixGetter

Учебный проект — асинхронная Python-библиотека для загрузки квадратной матрицы с удалённого сервера по HTTP(S), её парсинга и обхода по спирали (против часовой стрелки, начиная с левого верхнего угла).

Ссылка на тестовое задание: https://github.com/avito-tech/python-trainee-assignment

---

## Требования

* Python **3.10** или выше
* Установленный менеджер пакетов `pip`

---

## Установка и запуск с нуля

### 1. Клонирование репозитория
Откройте терминал и скачайте проект на свой компьютер:
```bash
git clone https://github.com/UNDREY123/MatrixGetter
cd MatrixGetter
```

### 2. Создание и активация виртуального окружения
Рекомендуется изолировать зависимости проекта в виртуальном окружении:

* **Для Windows (PowerShell / CMD):**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

* **Для Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Установка зависимостей
Установите HTTP-клиент `httpx` и фреймворк для тестирования `pytest`:
```bash
pip install "httpx[http2]" pytest
```

---

## Пример использования

Создайте файл (например, `example.py`) в корне проекта и запустите его:

```python
import asyncio
from matrix import get_matrix


async def main():
    url = "https://raw.githubusercontent.com/UNDREY123/MatrixGetter/refs/heads/master/tests/even_matrix.txt"
    result = await get_matrix(url)
    print(result)
    # Вывод: [10, 50, 90, 130, 140, 150, 160, 120, 80, 40, 30, 20, 60, 100, 110, 70]


if __name__ == "__main__":
    asyncio.run(main())
```

Запуск скрипта:
```bash
python example.py
```

---

## Запуск тестов

В проекте настроены автоматические тесты (включая проверку сетевых сбоев и граничных случаев парсинга), которые также прогоняются через GitHub Actions при каждом пуше.

Чтобы запустить тесты локально, выполните из корневой папки проекта:
```bash
pytest -v
```