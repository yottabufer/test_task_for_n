# Тестовое задание

<details>
  <summary>Подробности задания</summary>
# Тестовое задание веб-программист (Python)

Сделать API метод, который можно будет запустить POST запросом с параметрами:

1. data = Текстовое содержимое файла
2. name = Название файла

Необходимо создать в google drive документ с названием = name и содержимым = data

Предварительно нужно создать Гугл аккаунт пустой и авторизовать приложение, чтобы получить токены

<aside>
💡 Ориентировочное время решения - до 2ч. Решение нужно прислать в течение недели после получения.

</aside>

**Нужно использовать:**

- Фреймворк Django

**Критерии оценки:**

- Работоспособность согласно ТЗ
- Архитектура решения
- Удобство чтения кода и комментарии
- Удобство проверки(GIT + развернутый рабочий сервер на момент проверки)

Сервер достаточно держать в течение 2х дней после отправки решения, чтобы мы могли провести тесты

Результат тестового задания необходимо отправить в HH:

1. Ссылка на [репозиторий](https://github.com/)
2. URL и описание метода
3. Ссылка на публичную папку на google drive с созданными файлами

С уважением, Анна, NOVA.
</details>

### Как протестировать:
1. Сделать POST-запрос по адресу
```python
https://yottabufer.pythonanywhere.com/api/upload/
```

2. Тело запроса должно включать:
```python
name: test_str
```

```python
data: test_str
```

3. Перейти ГуглДиск и проверить папку:
```python
https://drive.google.com/drive/folders/1KHnntufZ0aWA1m05v42dkDwJw8Fd6DhW?hl=ru
```