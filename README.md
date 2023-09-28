# test_framework

<details>
<summary>Версия Python</summary>
    3.11+

</details>

<details>
<summary>Установка окружения</summary>

##### Перейти в папку с проектом
```bash
cd ../project_dir
```
##### Перейти создать локальное окружение:
```bash
python -m venv venv
```
##### Запустить локальное окружение:
```bash
venv\Scripts\activate.bat
```
##### Установить зависимости:
```bash
pip install -r req.txt
```

</details>

<details>
<summary>Команды запуска тестов</summary>

##### Запустить все тесты:
```bash
pytest -v
```
##### Запустить все тесты без багов:
```bash
pytest -v -m "not bug"
```
##### Запустить api тесты:
```bash
pytest -v -m "api"
```
##### Запустить api тесты без багов:
```bash
pytest -v -m "api and not bug"
```
##### Запустить web тесты:
```bash
pytest -v -m "web"
```
##### Запустить web тесты без багов:
```bash
pytest -v -m "web and not bug"
```
</details>