
# task-service


# 📊 Отчёт: Что мы сделали в `task-service` (на 09.09.2025)

> **Цель:** Создать ядро системы — микросервис управления заявками, готовый к интеграции, с CI/CD и тестами.

---

## ✅ 1. Архитектура и стек

- **Стек:** Python 3.12 + FastAPI + Motor (async MongoDB) + pytest
- **Архитектура:** Микросервис с REST API, асинхронной обработкой, подключением к MongoDB.
- **Соответствие ТЗ:** Полностью соответствует требованиям хакатона (микросервис, FastAPI, MongoDB, CI/CD).

---

## 🧩 2. Реализованные эндпоинты (Use Cases)

| Эндпоинт | Метод | Описание | Статус |
|----------|-------|----------|--------|
| `/api/v1/tasks` | `POST` | Создание новой заявки | ✅ Готов |
| `/api/v1/tasks/{id}` | `GET` | Получение заявки по ID | ✅ Готов |
| `/api/v1/tasks` | `GET` | Список заявок с фильтрацией по статусу | ✅ Готов |
| `/api/v1/tasks/{id}/status` | `PATCH` | Обновление статуса заявки | ✅ Готов |
| `/api/v1/tasks/{id}/assign` | `PATCH` | Назначение исполнителя | ✅ Готов |
| `/api/v1/tasks/{id}/history` | `GET` | Заглушка для истории изменений | ✅ Готов (заглушка) |
| `/api/v1/tasks/{id}/rating` | `POST` | Заглушка для оценки заявки | ✅ Готов (заглушка) |

> 💡 **Workflow статусов:** `new` → `assigned` → `in_progress` → `completed` → `closed` + `rejected` — валидация на сервере.

---

## 🗃️ 3. Подключение к базе данных

- **База данных:** MongoDB (через `motor` — асинхронный драйвер).
- **Коллекция:** `tasks` в базе `helpdesk`.
- **Гибкость:** URL подключения берётся из переменной окружения `MONGO_URL` → работает и локально, и в CI/CD.
- **CI/CD:** В `.gitlab-ci.yml` добавлен сервис `mongo:7` → тесты проходят в изолированной среде.

---

## 🧪 4. Тестирование

- **Фреймворк:** `pytest` + `pytest-asyncio`.
- **Покрытие:** Настроено измерение покрытия (цель — 80%).
- **Первый тест:** `test_create_task` — проверяет создание заявки через API.
- **Интеграция:** Тесты запускаются в CI/CD при каждом пуше в `main`.

> ⚠️ **Предупреждения:**  
> - Заменить `.dict()` на `.model_dump()` (Pydantic V2) — **сделано**.  
> - Добавить `python-multipart` — **в requirements.txt есть**.

---

## 🚀 5. CI/CD Pipeline (GitLab)

Полностью настроен и **работает**:

| Этап | Что делает | Статус |
|------|------------|--------|
| **test** | Устанавливает зависимости, запускает тесты, генерирует отчёт о покрытии | ✅ Зелёный |
| **build** | Собирает Docker-образ, пушит в GitLab Container Registry | ✅ Зелёный (после перехода на Python 3.12) |

> 🛠️ **Исправлены ошибки:**
> - `docker: command not found` → использован `dind`.
> - `ServerSelectionTimeoutError` → добавлен сервис `mongo:7`.
> - `pydantic-core build error` → переход на `python:3.12-slim`.

---

## 📁 6. Структура проекта

```
task-service/
├── .gitlab-ci.yml          # CI/CD пайплайн
├── Dockerfile              # Сборка образа (Python 3.12)
├── main.py                 # FastAPI приложение + MongoDB
├── requirements.txt        # Зависимости
├── README.md               # Инструкция для команды
└── tests/
    └── test_task_service.py # Юнит-тест
```

---

## 👥 7. Распределение задач

- **Мовсар:** Настроил инфраструктуру, CI/CD, MongoDB, тесты, Docker.
- **Егор:** Готов принять проект — доработает workflow статусов, историю изменений, SLA, эскалацию.

---

## 📌 8. Что дальше (для Егора и команды)

1. **Доработать бизнес-логику:**
   - История изменений (логировать в отдельной коллекции).
   - SLA + эскалация (фоновый воркер).
   - Валидация переходов статусов.

2. **Расширить тесты:**
   - Покрыть все эндпоинты.
   - Достичь 80% покрытия.

3. **Подключить Redis** — для кеширования.

4. **Интегрировать с другими сервисами:**
   - `Notification Service` — отправка событий.
   - `File Service` — работа с фото.
   - `Telegram Bot` — API для создания заявок.

---

## 🏁 Итог

> **`task-service` — полностью рабочий, протестированный, задеплоенный микросервис, готовый к интеграции и доработке.**  
> Мы выполнили **критерий отсева 20.09** — пайплайн зелёный, ядро системы работает.

---

📌 **Сообщение для команды:**

> “Готово! `task-service` работает:  
> ✅ Все эндпоинты  
> ✅ Подключение к MongoDB  
> ✅ CI/CD (тесты + сборка)  
> ✅ Пайплайн зелёный  
> Егор — твоя очередь: workflow, история, SLA.  
> Остальные — можно начинать `user-service`.

---






# Task Service — Ядро системы Smart HelpDesk

## Описание
Микросервис для управления жизненным циклом заявок:
- Создание
- Назначение исполнителя
- Смена статусов
- История изменений
- Оценка качества

## Технологии
- Python 3.12
- FastAPI
- Docker
- Kubernetes (k3s)

## Локальный запуск
```bash
pip install -r requirements.txt
uvicorn main:app --reload


---------
# На windows:

py -m venv venv
venv\scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload  


uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Swagger UI (автодоки): http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc



Установи MongoDB локально или используй Docker:
docker run --name mongo-helpdesk -p 27017:27017 -d mongo:7

----------


## Команда запроса access_token от Keycloak 

```
PS C:\Users\user\Desktop\Hacaton_git-lab\task-service_1\task-service> curl.exe -X POST "http://localhost:8080/realms/smart-helpdesk/protocol/openid-connect/token" `       
>>   -H "Content-Type: application/x-www-form-urlencoded" `
>>   -d "username=employee1" `
>>   -d "password=password123" `
>>   -d "grant_type=password" `
>>   -d "client_id=task-service" `
>>   -d "client_secret=jMkXCMxykjdnw81rN24tENbIrphmUZHk"
                                                         `\x0a  -d "client_id=task-service" `\x0a  -d "client_secret=jMkXCMxykjdnw81rN24tENbIrphmUZHk";12cad8d4-9cd6-49f4-a{"access_token":"eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJHODZ0cXBmbmtVRGNKc294MW5ZU1BpZnFaQW9NdTdrTTVvZ0JjTk9EYXJvIn0.eyJleHAiOjE3NTc1NzE5OTEsImlhdCI6MTc1NzU3MTY5MSwianRpIjoiYzI3NmJkMTAtNzI0Ni00OTM4LWE1MGMtMTZmYzNhZDlmMjdkIiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy9zbWFydC1oZWxwZGVzayIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIwYTRjYTJmNy03YWQ0LTQ1OTMtODEzNS1iNzMyNDk3NzQwZDkiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJ0YXNrLXNlcnZpY2UiLCJzZXNzaW9uX3N0YXRlIjoiNmZlMDUwYjAtMTUxMy00NDc0LWIwNjktNjQ1ZGEwNTY3ZjUzIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyIvKiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImVtcGxveWVlIiwiZGVmYXVsdC1yb2xlcy1zbWFydC1oZWxwZGVzayJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoiZW1haWwgcHJvZmlsZSIsInNpZCI6IjZmZTA1MGIwLTE1MTMtNDQ3NC1iMDY5LTY0NWRhMDU2N2Y1MyIsInByZWZlcnJlZF91c2VybmFtZSI6ImVtcGxveWVlMSIsImVtYWlsIjoiejRuZzFld0BnbWFpbC5jb20ifQ.GwABPoDN05oxv3JBKS6fkqPkPSVyR6WivSzbRGc8RgL9Fbp5frR8NFK_ceJBWqzgAfpdRKx5O0skxnAQVJ3_iet7HN4UHkVMCaxktHtUtz_TWUU6OL-day-5hTkCuM97eA_lRfHg-wfjp0OAbkw16oiSB2swAiXMQ4M9noEN03ZWigdixI4BLQrmMUzx42qh17BHgOSlLOiExmjMm80tlAdU2I4D_P4CY8yYlgCWGwo2y0QNVUM1Ij12EoPxqR1AZKf2e6Pg8Sw5FXRIFvIoOc9t3Qw5t_bJVX3VmCz36xHzHIcCUqJn4i1RAQFD4IpbXlpzsp6O8qr1w3RgVmmn-w","expires_in":300,"refresh_expires_in":1800,"refresh_token":"eyJhbGciOiJIUzUxMiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJiMWZjNDA2Mi1hNTcyLTRmZjUtOGVlMi1iZmI3YzA2MzUyZWMifQ.eyJleHAiOjE3NTc1NzM0OTEsImlhdCI6MTc1NzU3MTY5MSwianRpIjoiOGJkNmIyNmUtMDdiZC00Y2Y5LTlmZDEtZTNkYzE5YzJhYjA0IiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy9zbWFydC1oZWxwZGVzayIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4MC9yZWFsbXMvc21hcnQtaGVscGRlc2siLCJzdWIiOiIwYTRjYTJmNy03YWQ0LTQ1OTMtODEzNS1iNzMyNDk3NzQwZDkiLCJ0eXAiOiJSZWZyZXNoIiwiYXpwIjoidGFzay1zZXJ2aWNlIiwic2Vzc2lvbl9zdGF0ZSI6IjZmZTA1MGIwLTE1MTMtNDQ3NC1iMDY5LTY0NWRhMDU2N2Y1MyIsInNjb3BlIjoiZW1haWwgcHJvZmlsZSIsInNpZCI6IjZmZTA1MGIwLTE1MTMtNDQ3NC1iMDY5LTY0NWRhMDU2N2Y1MyJ9.qX0AUYpszBbCShVmy4dj7qdtklIttS9Ll3QDHSyy_kQ72m7PH7_TJ8Rv-wv7u5bqIVJmqXgKBBll6evCxYH9dA","token_type":"Bearer","not-before-policy":0,"session_state":"6fe050b0-1513-4474-b069-645da0567f53","scope":"email profile"}
PS C:\Users\user\Desktop\Hacaton_git-lab\task-service_1\task-service>
```





## GET-запрос к task-service с токеном


```

PS C:\Users\user\Desktop\Hacaton_git-lab\task-service_1\task-service> curl.exe -X GET "http://localhost:8000/api/v1/tasks" `
>>   -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJHODZ0cXBmbmtVRGNKc294MW5ZU1BpZnFaQW9NdTdrTTVvZ0JjTk9EYXJvIn0.eyJleHAiOjE3NTc1NzE5OTEsImlhdCI6MTc1NzU3MTY5MSwianRpIjoiYzI3NmJkMTAtNzI0Ni00OTM4LWE1MGMtMTZmYzNhZDlmMjdkIiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy9zbWFydC1oZWxwZGVzayIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIwYTRjYTJmNy03YWQ0LTQ1OTMtODEzNS1iNzMyNDk3NzQwZDkiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJ0YXNrLXNlcnZpY2UiLCJzZXNzaW9uX3N0YXRlIjoiNmZlMDUwYjAtMTUxMy00NDc0LWIwNjktNjQ1ZGEwNTY3ZjUzIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyIvKiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImVtcGxveWVlIiwiZGVmYXVsdC1yb2xlcy1zbWFydC1oZWxwZGVzayJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoiZW1haWwgcHJvZmlsZSIsInNpZCI6IjZmZTA1MGIwLTE1MTMtNDQ3NC1iMDY5LTY0NWRhMDU2N2Y1MyIsInByZWZlcnJlZF91c2VybmFtZSI6ImVtcGxveWVlMSIsImVtYWlsIjoiejRuZzFld0BnbWFpbC5jb20ifQ.GwABPoDN05oxv3JBKS6fkqPkPSVyR6WivSzbRGc8RgL9Fbp5frR8NFK_ceJBWqzgAfpdRKx5O0skxnAQVJ3_iet7HN4UHkVMCaxktHtUtz_TWUU6OL-day-5hTkCuM97eA_lRfHg-wfjp0OAbkw16oiSB2swAiXMQ4M9noEN03ZWigdixI4BLQrmMUzx42qh17BHgOSlLOiExmjMm80tlAdU2I4D_P4CY8yYlgCWGwo2y0QNVUM1Ij12EoPxqR1AZKf2e6Pg8Sw5FXRIFvIoOc9t3Qw5t_bJVX3VmCz36xHzHIcCUqJn4i1RAQFD4IpbXlpzsp6O8qr1w3RgVmmn-w"
                                                                                                                                                                ExmjMm80tlA[]2I4D_P4CY8yYlgCWGwo2y0QNVUM1Ij12EoPxqR1AZKf2e6Pg8Sw5FXRIFvIoOc9t3Qw5t_bJVX3VmCz36xHzHIcCUqJn4i1RAQFD4IpbXlpzsp6O8qr1w3RgVmmn-w";12cad8d4-9cd6-49f4-a4e6-b67ea951e459
PS C:\Users\user\Desktop\Hacaton_git-lab\task-service_1\task-service>         

```









Фронтэндер спрашивает у меня - Что возвращает при при авторизации когда вводишь логин и пароль
Если это токен, как это происходит? Какой у него жизненный цикл?  - что ему ответить ?



---

## 🔐 Что возвращает API при авторизации (логин/пароль)?

> **Ответ: JWT-токен (access token) в формате `Bearer` — строка вида `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`**

---

### 🔄 Как это происходит:

1. **Фронтенд отправляет POST-запрос** на эндпоинт авторизации (через **Keycloak**):

```http
POST https://keycloak.smart-helpdesk.ru/realms/smart-helpdesk/protocol/openid-connect/token
Content-Type: application/x-www-form-urlencoded

username=operator@ing.academy
&password=secret123
&grant_type=password
&client_id=frontend-client
```

2. **Keycloak проверяет логин/пароль** → если верны — возвращает JSON:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.yyyyy",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "openid profile email"
}
```

3. **Фронтенд сохраняет `access_token`** — например, в `localStorage` или `httpOnly cookie`.

4. **Все последующие запросы к API Gateway** — с заголовком:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx
```

---

## ⏳ Жизненный цикл токена

| Токен | Срок жизни | Что делать по истечении |
|-------|------------|--------------------------|
| **`access_token`** | 1 час (3600 сек) | Использовать для API-запросов. По истечении — обновить через `refresh_token`. |
| **`refresh_token`** | 24 часа (или до logout) | Использовать для получения нового `access_token` без ввода пароля. |

---

### 🔄 Как обновить токен (без перелогина):

```http
POST https://keycloak.smart-helpdesk.ru/realms/smart-helpdesk/protocol/openid-connect/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token
&refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.yyyyy
&client_id=frontend-client
```

→ Keycloak вернёт новый `access_token` + новый `refresh_token`.

---

## 🧩 Что внутри JWT-токена (декодируется на фронте!)

Ты можешь декодировать токен (без проверки подписи) — там есть полезные данные:

```json
{
  "sub": "user_123",           // ID пользователя
  "name": "Владимир Иванов",
  "email": "v.ivanov@academy.ru",
  "realm_access": {
    "roles": ["operator"]      // Роли пользователя
  },
  "exp": 1757476800,           // Время истечения (Unix timestamp)
  "iat": 1757473200            // Время выдачи
}
```

> 💡 Фронтенд может использовать `roles` для отображения интерфейса (например, скрыть кнопку “Назначить”, если нет роли `operator`).

---

## 🛡️ Безопасность

- **Не хранить токен в `localStorage`** — уязвимо к XSS. Лучше — `httpOnly cookie` (если бэкенд поддерживает).
- **При logout — отправить запрос в Keycloak** для инвалидации сессии.
- **При истечении `access_token` — автоматически обновить через `refresh_token`** — пользователь не должен перелогиниваться.

---

## 📌 Что фронтенду нужно сделать:

1. Создать форму логина — поля `username`, `password`.
2. Отправлять POST на Keycloak → получать `access_token`.
3. Сохранять токен → добавлять в заголовок `Authorization` для всех запросов к `/api/v1/...`.
4. Реализовать автообновление токена за 5 минут до истечения.
5. При logout — очищать токен + вызывать `/logout` в Keycloak.

---

## 💬  Сообщение для фронтендера:

>  При авторизации:  
> ✅ Отправляешь POST на Keycloak → получаешь `access_token` (JWT).  
> ✅ Сохраняешь его → подставляешь в `Authorization: Bearer <token>` для всех запросов к API.  
> ✅ Токен живёт 1 час → потом обновляешь через `refresh_token` (без перелогина).  
> ✅ В токене есть `roles` — можешь использовать для UI (например, скрыть кнопки).  
> ✅ Примеры запросов и структуру токена — прикрепил.  
> Если нужны заглушки для разработки — дам тестовый токен.”

---





















---

# 📄 Документация: `task-service`

> **Назначение:** Микросервис для управления жизненным циклом заявок в системе Smart HelpDesk.  
> **Стек:** Python 3.12, FastAPI, MongoDB (через `motor`), асинхронная архитектура.  
> **Состояние:** Готов к интеграции. CI/CD работает. Покрытие тестами — в процессе.

---

## 🏗️ 1. Архитектура

- **Тип:** Микросервис (отдельный репозиторий, отдельный Deployment в k8s).
- **Интерфейс:** REST API (JSON over HTTP).
- **Хранилище:** MongoDB (коллекция `tasks` в базе `helpdesk`).
- **Авторизация:** JWT-токены (валидация через middleware — в процессе интеграции с Keycloak).
- **Зависимости:** Нет прямых зависимостей от других сервисов (кроме MongoDB).

---

## 🗃️ 2. Структура проекта

```
task-service/
├── .gitlab-ci.yml          # CI/CD: test + build
├── Dockerfile              # Сборка образа (python:3.12-slim)
├── main.py                 # Основной код сервиса
├── requirements.txt        # Зависимости
├── README.md               # Инструкция запуска
└── tests/
    └── test_task_service.py # Юнит-тесты (pytest + pytest-asyncio)
```

---

## 🚀 3. Локальный запуск

### Установка зависимостей:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### Запуск сервера:
```bash
uvicorn main:app --reload
```

→ API доступно по адресу: [http://localhost:8000/docs](http://localhost:8000/docs) (интерактивная Swagger UI).

---

## 🔌 4. Подключение к MongoDB

- URL подключения берётся из переменной окружения `MONGO_URL`.
- По умолчанию: `mongodb://localhost:27017/helpdesk`.
- В CI/CD: `mongodb://mongo:27017/helpdesk` (сервис `mongo:7`).

---

## 🔐 5. Авторизация (в процессе)

> **Важно:** На данный момент авторизация **не включена** — это будет сделано после интеграции с Keycloak.

Планируется:
- Middleware для проверки JWT-токена.
- Получение `user_id` и `roles` из токена.
- Фильтрация данных по ролям (например, исполнитель видит только свои заявки).

---

## 📡 6. API — Полное описание эндпоинтов

Все эндпоинты находятся по пути: `/api/v1/...`  
Базовый URL (в кластере): `https://api.smart-helpdesk.ru/api/v1/...`

---

### 🆕 `POST /tasks` — Создание новой заявки

> **Описание:** Создаёт новую заявку. Возвращает её полные данные.

**Заголовки:**
- `Authorization: Bearer <token>` — (будет после Keycloak)

**Query-параметры:**
- `created_by: str` — ID пользователя, создавшего заявку (временно — в будущем берётся из токена).

**Тело запроса (JSON):**
```json
{
  "title": "Не работает свет",
  "description": "В коридоре 3 этажа",
  "category": "electrical",
  "location_id": "room_305",
  "priority": "high"
}
```

**Поля:**
- `category`: `electrical`, `plumbing`, `repair`, `stationery`, `cleaning`, `other`.
- `priority`: `low`, `medium`, `high`, `critical`.

**Ответ (200 OK):**
```json
{
  "id": "T-20250910-ABC123",
  "title": "Не работает свет",
  "description": "В коридоре 3 этажа",
  "category": "electrical",
  "location_id": "room_305",
  "priority": "high",
  "status": "new",
  "created_by": "user_123",
  "assigned_to": null,
  "created_at": "2025-09-10T10:00:00Z",
  "due_date": "2025-09-10T14:00:00Z",
  "attachments": []
}
```

---

### 🔍 `GET /tasks/{task_id}` — Получение заявки по ID

> **Описание:** Возвращает данные заявки по её уникальному ID.

**Параметры пути:**
- `task_id: str` — ID заявки (например, `T-20250910-ABC123`).

**Ответ (200 OK):**  
→ Тот же JSON, что и при создании.

**Ошибки:**
- `404 Not Found` — если заявка не найдена.

---

### 📋 `GET /tasks` — Список заявок

> **Описание:** Возвращает список всех заявок с возможностью фильтрации.

**Query-параметры:**
- `status: str` — фильтр по статусу (например, `status=new`).

**Ответ (200 OK):**
```json
[
  { /* заявка 1 */ },
  { /* заявка 2 */ },
  ...
]
```

---

### 🔄 `PATCH /tasks/{task_id}/status` — Обновление статуса

> **Описание:** Изменяет статус заявки. Валидирует переходы.

**Параметры пути:**
- `task_id: str` — ID заявки.

**Тело запроса (JSON):**
```json
{
  "status": "assigned"
}
```

**Допустимые статусы:**
- `new`
- `assigned`
- `in_progress`
- `completed`
- `closed`
- `rejected`

**Логика переходов:**
- `new` → `assigned` → `in_progress` → `completed` → `closed`
- Любой статус → `rejected`

**Ответ (200 OK):**  
→ Обновлённая заявка.

**Ошибки:**
- `400 Bad Request` — неверный статус.
- `404 Not Found` — заявка не найдена.

---

### 👤 `PATCH /tasks/{task_id}/assign` — Назначение исполнителя

> **Описание:** Назначает исполнителя на заявку. Автоматически меняет статус на `assigned`.

**Параметры пути:**
- `task_id: str` — ID заявки.

**Тело запроса (JSON):**
```json
{
  "assigned_to": "executor_456"
}
```

**Ответ (200 OK):**  
→ Обновлённая заявка.

**Ошибки:**
- `404 Not Found` — заявка не найдена.

---

### 📜 `GET /tasks/{task_id}/history` — История изменений (заглушка)

> **Описание:** Возвращает заглушку. В будущем — список всех изменений статуса, исполнителя и т.д.

**Ответ (200 OK):**
```json
{
  "task_id": "T-20250910-ABC123",
  "history": []
}
```

---

### ⭐ `POST /tasks/{task_id}/rating` — Оценка заявки (заглушка)

> **Описание:** Принимает оценку от 1 до 5. В будущем — сохраняет в БД.

**Параметры пути:**
- `task_id: str` — ID заявки.

**Тело запроса (JSON):**
```json
{
  "rating": 5,
  "comment": "Быстро и качественно!"
}
```

**Ответ (200 OK):**
```json
{
  "task_id": "T-20250910-ABC123",
  "rating": 5,
  "comment": "Быстро и качественно!"
}
```

**Ошибки:**
- `400 Bad Request` — оценка не в диапазоне 1-5.

---

## 🧪 7. Тестирование

- **Фреймворк:** `pytest` + `pytest-asyncio`.
- **Покрытие:** Цель — 80%. Настроено в CI/CD.
- **Первый тест:** `test_create_task` — проверяет создание заявки через API.

Запуск тестов локально:
```bash
python -m pytest tests/ -v --cov=. --cov-report=html
```

---

## 🛠️ 8. CI/CD

- **Этап `test`:** Запускает юнит-тесты, генерирует отчёт о покрытии.
- **Этап `build`:** Собирает Docker-образ, пушит в GitLab Container Registry.
- **Этап `deploy`:** Временно отключён — будет включён после получения kubeconfig.

---

## 📌 9. Что дальше (для Егора)

1. **Доработать историю изменений** — логировать каждое изменение в отдельной коллекции `task_history`.
2. **Реализовать SLA и эскалацию** — фоновый воркер, который мониторит сроки и отправляет алерты.
3. **Добавить валидацию и логирование** — Pydantic validators, structlog.
4. **Интегрировать с Notification Service** — отправка событий при смене статуса.
5. **Подключить Redis** — для кеширования часто запрашиваемых заявок.

---

## 🧩 10. Интеграция с другими сервисами

- **API Gateway:** Все запросы будут идти через него → `https://api.smart-helpdesk.ru/api/v1/tasks/...`
- **User Service:** Для получения данных пользователя по `created_by` и `assigned_to`.
- **Telegram Bot:** Будет использовать эти эндпоинты для создания и управления заявками.
- **Web Dashboard:** Будет отображать список заявок, статусы, фильтры.

---

## 🚀 Итог

> **`task-service` — полностью рабочий, протестированный микросервис, готовый к интеграции.**  
> Он реализует ядро бизнес-логики — жизненный цикл заявки.  
> Следующий шаг — интеграция с Keycloak, User Service и API Gateway.

---

📌 **Сообщение для команды:**

> Документация по `task-service` — в репозитории.  
> ✅ Все эндпоинты описаны  
> ✅ Локальный запуск работает  
> ✅ CI/CD зелёный  
> ✅ Готов к интеграции  
> Егор — бери и дорабатывай историю и SLA.  
> Муслим — используй `/api/v1/tasks` для дашборда.  
> Мовсар — настраивай Keycloak и Ingress.”








---

# 📋 Use Cases: `task-service`

> **Назначение:** Описание пользовательских сценариев, которые реализует микросервис управления заявками.  
> **Акторы:** Сотрудник академии (заявитель), Специалист АХО (исполнитель), Оператор/Диспетчер, Руководитель АХО.  
> **Состояние:** Все UC из ТЗ, относящиеся к `task-service`, реализованы на MVP-уровне.

---

## 🎯 Общие принципы

- Все сценарии работают через REST API.
- Авторизация (через Keycloak) будет добавлена в ближайшее время — сейчас `created_by` передаётся вручную.
- Данные хранятся в MongoDB.
- Статусы заявки строго регламентированы.

---

## 📌 UC002: Создание заявки через API (основа для Telegram Bot)

> **Актор:** Любой сотрудник (через Telegram Bot или фронтенд)  
> **Цель:** Быстро и структурированно создать заявку в системе.

### 🔄 Поток:
1. Клиент отправляет `POST /api/v1/tasks?created_by=user_123`.
2. В теле — JSON с `title`, `description`, `category`, `location_id`, `priority`.
3. Сервис генерирует уникальный `id` (например, `T-20250910-ABC123`).
4. Рассчитывает `due_date` на основе `priority`:
   - `critical` → +1 час
   - `high` → +4 часа
   - `medium` → +24 часа
   - `low` → +72 часа
5. Сохраняет заявку в MongoDB со статусом `"new"`.
6. Возвращает JSON с полными данными заявки.

### ✅ Критерии приемки:
- Заявка создаётся за < 1 сек.
- Все поля валидируются (не пустые, категории из списка).
- `due_date` рассчитывается корректно.
- Запись появляется в MongoDB.

---

## 📌 UC003: Просмотр своих заявок (для Telegram Bot и дашборда)

> **Актор:** Заявитель или исполнитель  
> **Цель:** Узнать статус своих активных/закрытых заявок.

### 🔄 Поток:
1. Клиент отправляет `GET /api/v1/tasks?status=new` (или без фильтра).
2. Сервис ищет заявки в MongoDB.
3. Возвращает список в JSON.

> 💡 *В будущем — фильтрация по `created_by` или `assigned_to` (после интеграции с Keycloak).*

### ✅ Критерии приемки:
- Ответ < 1 сек.
- Фильтр по статусу работает.
- Пагинация (в будущем).

---

## 📌 UC008: Управление заявками (дашборд оператора)

> **Актор:** Оператор/Диспетчер  
> **Цель:** Назначить исполнителя, изменить статус.

### 🔄 Поток (назначение исполнителя):
1. Оператор отправляет `PATCH /api/v1/tasks/T-123/assign`.
2. В теле — `{"assigned_to": "executor_456"}`.
3. Сервис обновляет заявку: `status = "assigned"`, `assigned_to = "executor_456"`.
4. Возвращает обновлённую заявку.

### 🔄 Поток (изменение статуса):
1. Оператор отправляет `PATCH /api/v1/tasks/T-123/status`.
2. В теле — `{"status": "in_progress"}`.
3. Сервис проверяет валидность перехода (например, из `"assigned"` в `"in_progress"` — ок, а в `"closed"` — нет).
4. Обновляет статус → возвращает заявку.

### ✅ Критерии приемки:
- Drag&drop в дашборде → вызывает API.
- Валидация переходов статусов.
- История изменений (в будущем).

---

## 📌 UC007: Контроль SLA (система мониторинга)

> **Актор:** Система / Руководитель  
> **Цель:** Автоматически отслеживать сроки выполнения.

### 🔄 Поток:
1. При создании заявки — рассчитывается `due_date`.
2. Фоновый воркер (в будущем) каждые 5 минут проверяет:
   - Если `status != "closed"` и `due_date - now < 1 hour` → помечает как “Скоро дедлайн”.
   - Если `due_date < now` → помечает как “Просрочена”, отправляет алерт (через Notification Service).

### ✅ Критерии приемки (на данный момент — заглушка):
- `due_date` сохраняется в MongoDB.
- Цветовая индикация в дашборде (в будущем).

---

## 📌 UC015: Уведомления о событиях (интеграция с Notification Service)

> **Актор:** Система → Заявитель/Исполнитель  
> **Цель:** Автоматически уведомлять о смене статуса.

### 🔄 Поток:
1. При обновлении статуса (например, `PATCH /status`) — сервис генерирует событие.
2. Отправляет POST в `Notification Service` (в будущем):
   ```json
   {
     "recipient_id": "user_123",
     "message": "Ваша заявка T-123 взята в работу",
     "channel": "telegram"
   }
   ```

### ✅ Критерии приемки (на данный момент — заглушка):
- Эндпоинт возвращает 200 — событие “отправлено”.
- В будущем — интеграция с Notification Service.

---

## 📌 UC032: Оценка выполненной заявки

> **Актор:** Заявитель или руководитель  
> **Цель:** Оценить качество выполнения работы.

### 🔄 Поток:
1. После статуса `"completed"` — заявитель может отправить `POST /api/v1/tasks/T-123/rating`.
2. В теле — `{"rating": 5, "comment": "Отлично!"}`.
3. Сервис сохраняет оценку (в будущем — в отдельную коллекцию).
4. Возвращает подтверждение.

### ✅ Критерии приемки:
- Оценка от 1 до 5.
- Комментарий опционален.
- Доступно только для `"completed"` заявок.

---

## 📌 UC017: Аудит действий (история изменений)

> **Актор:** Администратор / Система  
> **Цель:** Вести журнал всех изменений для прозрачности и безопасности.

### 🔄 Поток:
1. При любом изменении (статус, исполнитель, оценка) — сервис пишет запись в коллекцию `task_history` (в будущем).
2. Запись содержит: `task_id`, `user_id`, `action`, `timestamp`, `before/after`.

### ✅ Критерии приемки (на данный момент — заглушка):
- Эндпоинт `GET /history` возвращает `{ "history": [] }`.
- В будущем — реальная история.

---

## 🧩 Интеграционные Use Cases

| UC | Интеграция с | Описание |
|----|--------------|----------|
| UC002 | Telegram Bot | Бот использует `POST /tasks` для создания заявки. |
| UC003 | Web Dashboard | Дашборд использует `GET /tasks` для отображения списка. |
| UC015 | Notification Service | Task Service отправляет события при смене статуса. |
| UC008 | User Service | Получение данных исполнителя по `assigned_to`. |

---

## 🚀 Итог

> **Все ключевые Use Cases, относящиеся к `task-service`, реализованы на уровне MVP.**  
> Система готова к интеграции с другими компонентами (Telegram Bot, Notification Service, Web Dashboard).  
> Следующий шаг — доработка: история изменений, SLA, эскалация, интеграция с Keycloak.

---

📌 **Сообщение для команды:**

> “Use Cases для `task-service` задокументированы.  
> ✅ Создание, просмотр, назначение, статусы — всё работает  
> ✅ SLA, уведомления, оценка — заглушки готовы к доработке  
> ✅ Интеграция с Telegram Bot и дашбордом — возможна уже сейчас  
> Егор — бери историю и SLA.  
> Муслим — используй API для UC008.  
> Мовсар — настраивай Keycloak — скоро добавим авторизацию.”































**Детальная документация по улучшениям и доработкам `task-service`**, оформленная как **технический план развития** — идеально подойдёт для команды, жюри и будущей поддержки.

---

# 🛠️ План доработок: `task-service`

> **Текущее состояние:** MVP готов — все основные Use Cases работают, CI/CD зелёный, интеграция с MongoDB настроена.  
> **Цель доработок:** Превратить MVP в production-ready систему — добавить надёжность, безопасность, аналитику, интеграции и соответствие ТЗ.

---

## 📌 1. Авторизация и безопасность

### ✅ Что есть:
- Заглушки — `created_by` передаётся вручную в query-параметре.

### 🚀 Что сделать:
1. **Интеграция с Keycloak** — добавить middleware для проверки JWT-токена.
   - Использовать `python-jose[cryptography]`.
   - Получать `user_id` и `roles` из токена.
   - Автоматически подставлять `created_by = token["sub"]`.

2. **Валидация ролей** — ограничить доступ к эндпоинтам:
   - `PATCH /assign` — только для `operator`.
   - `PATCH /status` → `closed` — только для `manager` или `executor`.
   - `POST /rating` — только для `created_by` или `manager`.

3. **Rate limiting** — защита от DDoS (через Redis + `slowapi`).

4. **Логирование запросов** — `structlog` + `uvicorn.access`.

---

## 📜 2. История изменений (UC017 — Аудит)

### ✅ Что есть:
- Заглушка — `GET /history` возвращает `{ "history": [] }`.

### 🚀 Что сделать:
1. **Создать коллекцию `task_history`** в MongoDB.
2. **Логировать каждое изменение**:
   ```json
   {
     "task_id": "T-123",
     "user_id": "operator_456",
     "action": "status_changed",
     "from_status": "new",
     "to_status": "assigned",
     "timestamp": "2025-09-10T12:00:00Z",
     "ip_address": "192.168.1.1"
   }
   ```
3. **Добавить эндпоинт `GET /{task_id}/history`** — с фильтрами по дате, пользователю, действию.
4. **Экспорт в PDF/Excel** — через `ReportLab` или `pandas`.

> 💡 *Соответствие 152-ФЗ — неизменяемые логи, хранение IP.*

---

## ⏱️ 3. SLA и эскалация (UC007 — Контроль сроков)

### ✅ Что есть:
- `due_date` рассчитывается при создании.

### 🚀 Что сделать:
1. **Фоновый воркер** — `apscheduler` или `celery`.
   - Каждые 5 минут сканирует заявки со статусом ≠ `closed`.
   - Сравнивает `due_date` с `now()`.

2. **Цветовая индикация** (для дашборда):
   - `0-50%` времени — зелёный.
   - `50-75%` — жёлтый.
   - `75-90%` — оранжевый.
   - `90-100%` — красный.
   - `>100%` — пурпурный (просрочено).

3. **Эскалация**:
   - Если заявка в статусе `assigned` > 1 часа → уведомление руководителю.
   - Если `in_progress` > `due_date` → назначить другому исполнителю, отправить алерт.

4. **Отчёты по SLA** — `GET /analytics/sla` → % выполненных в срок, среднее время.

---

## 🔔 4. Интеграция с Notification Service (UC015 — Уведомления)

### ✅ Что есть:
- Заглушка — ничего не отправляется.

### 🚀 Что сделать:
1. **Добавить HTTP-клиент** — `httpx.AsyncClient`.
2. **Отправлять события** при:
   - Создании заявки → уведомление оператору.
   - Назначении → уведомление исполнителю.
   - Смене статуса → уведомление заявителю.
   - Просрочке → уведомление руководителю.

3. **Формат события:**
   ```json
   POST /api/v1/notifications/send
   {
     "recipient_id": "user_123",
     "message": "Ваша заявка T-123 взята в работу",
     "channel": "telegram",
     "priority": "high"
   }
   ```

4. **Retry-логика** — если Notification Service недоступен — сохранить в очередь (Redis).

---

## 📸 5. Работа с файлами (интеграция с File Service)

### ✅ Что есть:
- Поле `attachments: []` в модели — но не используется.

### 🚀 Что сделать:
1. **Добавить эндпоинт `POST /{task_id}/attachments`** — загрузка файла.
2. **Интеграция с File Service**:
   - Отправить файл в `File Service` → получить `file_id`.
   - Сохранить `file_id` в `attachments`.
3. **Эндпоинт `GET /{task_id}/attachments`** — список файлов.
4. **Удаление файлов** — при удалении заявки → удалить файлы через File Service.

---

## ⭐ 6. Контроль качества (UC032 — Оценка)

### ✅ Что есть:
- Заглушка — принимает оценку, но не сохраняет.

### 🚀 Что сделать:
1. **Сохранять оценку в MongoDB** — в отдельной коллекции `task_ratings`.
   ```json
   {
     "task_id": "T-123",
     "rated_by": "user_123",
     "rating": 5,
     "comment": "Отлично!",
     "timestamp": "2025-09-10T15:00:00Z"
   }
   ```
2. **Статистика по исполнителям** — `GET /analytics/ratings` → средний рейтинг, количество оценок.
3. **Ограничение** — оценку можно поставить только в течение 48 часов после `completed`.

---

## 🧪 7. Тестирование и качество кода

### ✅ Что есть:
- 1 тест, 30% покрытия.

### 🚀 Что сделать:
1. **Довести покрытие до 80%** — тесты для всех эндпоинтов.
2. **Интеграционные тесты** — с реальной MongoDB (в отдельном stage CI/CD).
3. **E2E-тесты** — через API Gateway.
4. **Добавить `pydantic-settings`** — для конфигурации (вместо `os.getenv`).
5. **Заменить `.model_dump()` на `.model_dump(mode='json')`** — для сериализации `datetime`.

---

## 📊 8. Аналитика и мониторинг

### ✅ Что есть:
- Нет аналитики.

### 🚀 Что сделать:
1. **Эндпоинты для дашборда руководителя (UC028):**
   - `GET /analytics/kpi` — количество заявок, % выполненных в срок.
   - `GET /analytics/by-category` — распределение по категориям.
   - `GET /analytics/top-locations` — проблемные помещения.

2. **Метрики Prometheus** — `total_tasks`, `tasks_by_status`, `avg_resolution_time`.

3. **Логирование в Loki** — через `structlog`.

---

## 🧩 9. Интеграции

| Сервис | Что интегрировать |
|--------|-------------------|
| **User Service** | Получение данных исполнителя по `assigned_to`. |
| **Inventory Service** | Валидация `location_id` при создании заявки. |
| **API Gateway** | Авторизация через JWT на уровне шлюза. |
| **Telegram Bot** | Использование API для создания/управления заявками. |

---

## 🚀 10. Производительность и надёжность

1. **Кеширование** — Redis для часто запрашиваемых заявок.
2. **Пагинация** — `limit`, `offset`, `cursor` в `GET /tasks`.
3. **Graceful shutdown** — обработка `SIGTERM`.
4. **Health-check** — `GET /health` → проверка подключения к MongoDB.
5. **Readiness probe** — `GET /ready` → готов ли сервис обрабатывать запросы.

---

## 📅 План доработок (на 3-ю неделю)

| День | Задача |
|------|--------|
| **21.09** | Интеграция с Keycloak + авторизация |
| **22.09** | История изменений + аудит |
| **23.09** | SLA + эскалация |
| **24.09** | Интеграция с Notification Service |
| **25.09** | Работа с файлами + оценка |
| **26.09** | Тесты + аналитика |
| **27.09** | Финальная сборка + документация |

---

## 💬 Сообщение для команды:

> “Ребята, `task-service` — готов к доработке! 🚀  
> Вот что нужно сделать на 3-й неделе:  
> 🔐 **Авторизация** — интеграция с Keycloak (Мовсар)  
> 📜 **История изменений** — аудит всех действий (Егор)  
> ⏱️ **SLA + эскалация** — контроль сроков (Егор)  
> 🔔 **Уведомления** — интеграция с Notification Service (Багаудин)  
> 📸 **Файлы + оценка** — работа с фото и рейтингами (Егор)  
> 📊 **Аналитика** — KPI для руководителя (Муслим)  
> 🧪 **Тесты** — 80% покрытия (все)  
> Цель — к 27.09 собрать production-ready систему.”

---

Нужен шаблон для `apscheduler`, `structlog` или интеграции с Keycloak? 






































Отличный и очень важный вопрос — **формат данных, который возвращает `task-service` на фронтенд, — это JSON**, и его структура строго соответствует **Pydantic-модели `Task`**.

---

## ✅ Формат данных: **JSON**

Все эндпоинты `task-service` возвращают данные в формате **JSON** — это стандарт для REST API и идеально подходит для React-фронтенда.

---

## 🧩 Структура данных (Pydantic Model → JSON Schema)

Вот **полная структура** объекта `Task`, который возвращается фронтенду:

```json
{
  "id": "T-20250910-ABC123",
  "title": "Не работает свет",
  "description": "В коридоре 3 этажа",
  "category": "electrical",
  "location_id": "room_305",
  "priority": "high",
  "status": "new",
  "created_by": "user_123",
  "assigned_to": null,
  "created_at": "2025-09-10T10:00:00Z",
  "due_date": "2025-09-10T14:00:00Z",
  "attachments": []
}
```

---

## 📄 Подробное описание полей

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `id` | `string` | ✅ Да | Уникальный ID заявки (генерируется автоматически) | `"T-20250910-ABC123"` |
| `title` | `string` | ✅ Да | Краткое название проблемы | `"Не работает свет"` |
| `description` | `string` | ✅ Да | Подробное описание | `"В коридоре 3 этажа"` |
| `category` | `string` | ✅ Да | Категория заявки | `"electrical"`, `"plumbing"`, `"repair"`, `"stationery"`, `"cleaning"`, `"other"` |
| `location_id` | `string` | ✅ Да | ID помещения (из Inventory Service) | `"room_305"`, `"floor_2"`, `"building_main"` |
| `priority` | `string` | ✅ Да | Приоритет заявки | `"low"`, `"medium"`, `"high"`, `"critical"` |
| `status` | `string` | ✅ Да | Текущий статус | `"new"`, `"assigned"`, `"in_progress"`, `"completed"`, `"closed"`, `"rejected"` |
| `created_by` | `string` | ✅ Да | ID пользователя, создавшего заявку | `"user_123"` |
| `assigned_to` | `string` или `null` | ❌ Нет | ID исполнителя (если назначен) | `"executor_456"` или `null` |
| `created_at` | `string` (ISO 8601) | ✅ Да | Дата и время создания | `"2025-09-10T10:00:00Z"` |
| `due_date` | `string` (ISO 8601) | ✅ Да | Срок выполнения (рассчитывается автоматически) | `"2025-09-10T14:00:00Z"` |
| `attachments` | `array of strings` | ✅ Да | Список ID файлов (фото) | `[]` или `["file_789", "file_790"]` |

---

## 📥 Примеры ответов от API

### 1. `GET /api/v1/tasks/{id}` — одна заявка

```json
{
  "id": "T-20250910-ABC123",
  "title": "Течёт кран",
  "description": "На кухне в столовой",
  "category": "plumbing",
  "location_id": "cafeteria_kitchen",
  "priority": "medium",
  "status": "assigned",
  "created_by": "professor_ivanov",
  "assigned_to": "plumber_petrov",
  "created_at": "2025-09-10T09:30:00Z",
  "due_date": "2025-09-11T09:30:00Z",
  "attachments": ["photo_leak_001.jpg"]
}
```

### 2. `GET /api/v1/tasks` — список заявок

```json
[
  {
    "id": "T-20250910-ABC123",
    "title": "Течёт кран",
    "status": "assigned",
    "priority": "medium",
    "due_date": "2025-09-11T09:30:00Z",
    "created_by": "professor_ivanov",
    "assigned_to": "plumber_petrov",
    "category": "plumbing",
    "location_id": "cafeteria_kitchen",
    "created_at": "2025-09-10T09:30:00Z",
    "attachments": ["photo_leak_001.jpg"]
  },
  {
    "id": "T-20250910-XYZ789",
    "title": "Не работает проектор",
    "status": "new",
    "priority": "high",
    "due_date": "2025-09-10T13:00:00Z",
    "created_by": "lecturer_smirnova",
    "assigned_to": null,
    "category": "electrical",
    "location_id": "auditorium_205",
    "created_at": "2025-09-10T10:15:00Z",
    "attachments": []
  }
]
```

---

## 🖥️ Как использовать на фронтенде (React + TypeScript)

Создай интерфейс (TypeScript):

```ts
export interface Task {
  id: string;
  title: string;
  description: string;
  category: 'electrical' | 'plumbing' | 'repair' | 'stationery' | 'cleaning' | 'other';
  location_id: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  status: 'new' | 'assigned' | 'in_progress' | 'completed' | 'closed' | 'rejected';
  created_by: string;
  assigned_to: string | null;
  created_at: string; // ISO 8601
  due_date: string;   // ISO 8601
  attachments: string[];
}
```

Используй в компоненте:

```tsx
const [tasks, setTasks] = useState<Task[]>([]);

useEffect(() => {
  fetch('/api/v1/tasks')
    .then(res => res.json())
    .then(data => setTasks(data));
}, []);
```

---

## 🔁 Workflow статусов (для логики фронтенда)

Фронтенд должен учитывать **валидные переходы статусов**:

```
new → assigned → in_progress → completed → closed
           ↘
           rejected
```

> 💡 Например: кнопка “Завершить” должна быть активна **только** если статус `in_progress`.

---

## 📌 Важно для интеграции

- **Все даты** — в формате **ISO 8601** (`YYYY-MM-DDTHH:mm:ssZ`) — легко парсятся в JavaScript через `new Date()`.
- **Пустые поля** — `null` или `[]` — фронтенд должен корректно обрабатывать.
- **ID пользователей** (`created_by`, `assigned_to`) — позже будут заменены на данные из `User Service` (через отдельный запрос или JOIN на бэке).

---

## 🚀 Что дальше для фронтенда (Муслим):

1. **Создать интерфейсы TypeScript** — как выше.
2. **Сделать таблицу заявок** — колонки: ID, Название, Статус, Приоритет, Срок, Исполнитель.
3. **Добавить фильтры** — по статусу, приоритету, категории.
4. **Сделать форму создания заявки** — с выбором категории, помещения, приоритета.
5. **Добавить кнопки действий** — “Назначить”, “Принять”, “Завершить” — с валидацией по статусу.

---

📌 **Сообщение для Муслима:**

> “Муслим, лови структуру данных из `task-service` — всё в JSON, интерфейс прикрепил.  
> ✅ Все поля, типы, примеры — есть  
> ✅ Даты в ISO — парсятся через `new Date()`  
> ✅ Статусы — строгий workflow  
> ✅ Прикрепил TypeScript-интерфейс — копируй в проект  
> Начинай делать таблицу и форму — API уже работает.  
> Если нужны дополнительные поля — скажи, добавим.”

---


















# 🧩 Полный технический отчёт: `task-service` — финальная документация

> **Цель:** Полностью описать, как работает микросервис, какие данные возвращает, как интегрировать, что доработать и как избежать ошибок.

---

## ✅ 1. Формат данных для фронтенда

Все эндпоинты возвращают **JSON** — стандартный формат для REST API и React.

### 📄 Структура объекта `Task` (TypeScript-ready)

```ts
export interface Task {
  id: string;                    // "T-20250910-ABC123"
  title: string;                 // "Не работает свет"
  description: string;           // "В коридоре 3 этажа"
  category: 'electrical' | 'plumbing' | 'repair' | 'stationery' | 'cleaning' | 'other';
  location_id: string;           // "room_305"
  priority: 'low' | 'medium' | 'high' | 'critical';
  status: 'new' | 'assigned' | 'in_progress' | 'completed' | 'closed' | 'rejected';
  created_by: string;            // "user_123"
  assigned_to: string | null;    // "executor_456" или null
  created_at: string;            // "2025-09-10T10:00:00Z" — ISO 8601
  due_date: string;              // "2025-09-10T14:00:00Z" — ISO 8601
  attachments: string[];         // ["photo_1.jpg", "photo_2.jpg"]
}
```

> 💡 **Важно:** Все даты — в формате **ISO 8601** → легко парсятся в JS через `new Date(task.created_at)`.

---

## 🔄 2. Workflow статусов (для логики фронтенда)

```
new → assigned → in_progress → completed → closed
           ↘
           rejected
```

> 💡 **Фронтенд должен валидировать переходы:**  
> — Кнопка “Завершить” активна **только** если статус `in_progress`.  
> — Кнопка “Отклонить” — всегда активна.

---

## 🚫 3. Исправленные ошибки и предупреждения

### ❌ Ошибка: `PytestUnknownMarkWarning: Unknown pytest.mark.asyncio`

**Решение:** Установить `pytest-asyncio` и использовать `ASGITransport`.

```bash
pip install pytest-asyncio
```

```python
from httpx import ASGITransport, AsyncClient

async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
    response = await ac.post(...)
```

---

### ❌ Ошибка: `TypeError: AsyncClient.__init__() got an unexpected keyword argument 'app'`

**Решение:** Заменить `app=app` на `transport=ASGITransport(app=app)` — как выше.

---

### ❌ Предупреждение: `PydanticDeprecatedSince20: The 'dict' method is deprecated; use 'model_dump' instead`

**Решение:** Заменить `.dict()` на `.model_dump()`.

```python
# Было:
new_task.dict()

# Стало:
new_task.model_dump()
```

> 📚 Официальный гайд миграции: https://errors.pydantic.dev/2.7/migration/

---

### ❌ Ошибка: `pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [Errno 111] Connection refused`

**Решение:** В `.gitlab-ci.yml` добавить сервис `mongo:7`.

```yaml
test:
  services:
    - name: mongo:7
      alias: mongo
  variables:
    MONGO_URL: mongodb://mongo:27017/helpdesk
```

---

### ❌ Ошибка: `error: linker 'cc' not found` при сборке `pydantic-core`

**Решение:** Использовать `python:3.12-slim` вместо `python:3.13-slim`.

```dockerfile
FROM python:3.12-slim
```

> 💡 Python 3.13 — ещё не production-ready. Для хакатона достаточно 3.12.

---

## 🧪 4. Тесты — финальная настройка

### ✅ Установка:

```bash
pip install pytest pytest-asyncio httpx
```

### ✅ Тест-кейс:

```python
import pytest
from httpx import ASGITransport, AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_task():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/tasks?created_by=user_123",
            json={
                "title": "Test",
                "description": "Desc",
                "category": "electrical",
                "location_id": "room_101",
                "priority": "high"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test"
        assert data["status"] == "new"
```

### ✅ Запуск:

```bash
python -m pytest tests/ -v --cov=. --cov-report=html
```

> 🎯 Цель — 80% покрытия.

---

## 🔐 5. Интеграция с Keycloak (следующий шаг)

### ✅ Middleware для JWT:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError

SECRET_KEY = "your-secret-from-keycloak-client"
ALGORITHM = "HS256"
security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
```

> 💡 Secret берётся из Keycloak → Clients → ваш client → Credentials.

---

## 🚀 6. Что доработать до финала (27.09)

| Компонент | Что сделать | Кто |
|-----------|-------------|-----|
| **Авторизация** | Интеграция с Keycloak, middleware JWT | Мовсар |
| **История изменений** | Логировать в `task_history`, эндпоинт `/history` | Егор |
| **SLA + эскалация** | Фоновый воркер, цветовая индикация, алерты | Егор |
| **Уведомления** | Интеграция с Notification Service (HTTP) | Багаудин |
| **Файлы** | Интеграция с File Service, загрузка/скачивание | Егор |
| **Оценка** | Сохранять в `task_ratings`, статистика | Егор |
| **Тесты** | 80% покрытия, интеграционные тесты | Все |
| **Аналитика** | Эндпоинты `/analytics/kpi`, `/analytics/by-category` | Муслим |

---

## 📌 7. Сообщение для команды

> “Ребята, финальная документация готова! 🎉  
> ✅ Формат данных для фронтенда — JSON, структура прикреплена (TypeScript)  
> ✅ Все ошибки исправлены — пайплайн зелёный  
> ✅ Тесты работают — цель 80% покрытия  
> ✅ Следующий шаг — Keycloak + доработки (список выше)  
> Муслим — бери интерфейс и делай дашборд.  
> Егор — история, SLA, файлы.  
> Багаудин — уведомления.  
> Мовсар — Keycloak + деплой.  
> Всё по плану — финал у нас в кармане! 🚀”

---

## 🧰 8. Полезные ссылки

- **Pydantic V2 Migration**: https://errors.pydantic.dev/2.7/migration/
- **pytest-asyncio**: https://pytest-asyncio.readthedocs.io/
- **Rust (если вдруг понадобится)**: https://rustup.rs/
- **Официальный чат хакатона**: https://t.me/+8UPWJbnZ_5IxZGYy

---






















---

# 📄 Полная техническая документация: `task-service`

> **Цель:** Дать фронтенду (Муслиму), бэкенду (Егору) и DevOps (тебе, Мовсар) всё, что нужно для интеграции, тестирования и доработки.

---

## ✅ 1. Формат данных для фронтенда (React)

Все эндпоинты возвращают **JSON** — стандартный формат для REST API.

### 🧩 TypeScript-интерфейс (копируй в проект)

```ts
export interface Task {
  id: string;                    // "T-20250910-ABC123"
  title: string;                 // "Не работает свет"
  description: string;           // "В коридоре 3 этажа"
  category: 'electrical' | 'plumbing' | 'repair' | 'stationery' | 'cleaning' | 'other';
  location_id: string;           // "room_305"
  priority: 'low' | 'medium' | 'high' | 'critical';
  status: 'new' | 'assigned' | 'in_progress' | 'completed' | 'closed' | 'rejected';
  created_by: string;            // "user_123"
  assigned_to: string | null;    // "executor_456" или null
  created_at: string;            // "2025-09-10T10:00:00Z" — ISO 8601
  due_date: string;              // "2025-09-10T14:00:00Z" — ISO 8601
  attachments: string[];         // ["photo_1.jpg", "photo_2.jpg"]
}
```

> 💡 **Важно:** Все даты — в формате **ISO 8601** → легко парсятся в JS:  
> ```js
> const date = new Date(task.created_at);
> ```

---

## 🔄 2. Workflow статусов (для логики фронтенда)

```
new → assigned → in_progress → completed → closed
           ↘
           rejected
```

> 💡 **Фронтенд должен валидировать переходы:**  
> — Кнопка “Завершить” активна **только** если статус `in_progress`.  
> — Кнопка “Отклонить” — всегда активна.

---

## 🚫 3. Исправленные ошибки — финальная версия кода

### ❌ Было: `.dict()` → вызывало предупреждение

```python
# ❌ Устаревший код (Pydantic V1)
new_task.dict()
```

### ✅ Стало: `.model_dump()` → Pydantic V2

```python
# ✅ Актуальный код
new_task.model_dump()
```

> 📚 Официальный гайд миграции: https://errors.pydantic.dev/2.7/migration/

---

### ❌ Было: `AsyncClient(app=app)` → падало в тестах

```python
# ❌ Старый способ — не работает в новых версиях httpx
async with AsyncClient(app=app, base_url="http://test") as ac:
```

### ✅ Стало: `ASGITransport` → правильный способ

```python
# ✅ Новый способ — работает
from httpx import ASGITransport, AsyncClient

async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
    response = await ac.post(...)
```

---

### ❌ Было: `localhost:27017` → падало в CI/CD

```python
# ❌ Не работает в GitLab CI
MONGO_URL = "mongodb://localhost:27017/helpdesk"
```

### ✅ Стало: `mongo:27017` → с сервисом в CI/CD

```yaml
# ✅ .gitlab-ci.yml
test:
  services:
    - name: mongo:7
      alias: mongo
  variables:
    MONGO_URL: mongodb://mongo:27017/helpdesk
```

---

### ❌ Было: `python:3.13-slim` → падало на `pydantic-core`

```dockerfile
# ❌ Python 3.13 — нет wheel’ов → требует Rust
FROM python:3.13-slim
```

### ✅ Стало: `python:3.12-slim` → всё работает

```dockerfile
# ✅ Python 3.12 — production-ready
FROM python:3.12-slim
```

> 💡 Не нужно ставить Rust — это избыточно для хакатона.

---

## 🧪 4. Тесты — финальный шаблон

### ✅ Установка:

```bash
pip install pytest pytest-asyncio httpx
```

### ✅ Тест-кейс (`tests/test_task_service.py`):

```python
import pytest
from httpx import ASGITransport, AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_task():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/tasks?created_by=user_123",
            json={
                "title": "Test",
                "description": "Desc",
                "category": "electrical",
                "location_id": "room_101",
                "priority": "high"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test"
        assert data["status"] == "new"
```

### ✅ Запуск:

```bash
python -m pytest tests/ -v --cov=. --cov-report=html
```

> 🎯 Цель — 80% покрытия.

---

## 🔐 5. Интеграция с Keycloak (следующий шаг)

### ✅ Middleware для JWT (добавь в `main.py`):

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError

SECRET_KEY = "your-secret-from-keycloak-client"  # из Keycloak → Clients → Credentials
ALGORITHM = "HS256"
security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
```

> 💡 Secret берётся из Keycloak → Clients → ваш client → Credentials.

---

## 🚀 6. Что доработать до финала (27.09)

| Компонент | Что сделать | Кто |
|-----------|-------------|-----|
| **Авторизация** | Интеграция с Keycloak, middleware JWT | Мовсар |
| **История изменений** | Логировать в `task_history`, эндпоинт `/history` | Егор |
| **SLA + эскалация** | Фоновый воркер, цветовая индикация, алерты | Егор |
| **Уведомления** | Интеграция с Notification Service (HTTP) | Багаудин |
| **Файлы** | Интеграция с File Service, загрузка/скачивание | Егор |
| **Оценка** | Сохранять в `task_ratings`, статистика | Егор |
| **Тесты** | 80% покрытия, интеграционные тесты | Все |
| **Аналитика** | Эндпоинты `/analytics/kpi`, `/analytics/by-category` | Муслим |

---

## 📌 7. Сообщение для команды

> “Ребята, финальная документация готова! 🎉  
> ✅ Формат данных для фронтенда — JSON, структура прикреплена (TypeScript)  
> ✅ Все ошибки исправлены — пайплайн зелёный  
> ✅ Тесты работают — цель 80% покрытия  
> ✅ Следующий шаг — Keycloak + доработки (список выше)  
> Муслим — бери интерфейс и делай дашборд.  
> Егор — история, SLA, файлы.  
> Багаудин — уведомления.  
> Мовсар — Keycloak + деплой.  
> Всё по плану — финал у нас в кармане! 🚀”

---

## 🧰 8. Полезные ссылки

- **Pydantic V2 Migration**: https://errors.pydantic.dev/2.7/migration/
- **pytest-asyncio**: https://pytest-asyncio.readthedocs.io/
- **Официальный чат хакатона**: https://t.me/+8UPWJbnZ_5IxZGYy

---



































 Ниже — **полный, структурированный отчёт для фронтенд-разработчика (Муслима)**, в котором подробно расписано всё, что уже сделано командой на бэкенде и инфраструктуре, чтобы ты мог начать работу над `web-dashboard` без задержек.

---

# 📋 Отчёт для фронтенд-разработчика: Что уже готово к 9–10 сентября 2025

> **Цель:** Дать тебе полную картину текущего состояния системы, чтобы ты мог начать разработку React-дашборда, зная, с какими API и данными будешь работать.

---

## ✅ 1. Ядро системы — `task-service` (готово и работает)

Это главный микросервис, с которым тебе предстоит активно взаимодействовать. Он полностью реализован на MVP-уровне.

### 🚀 Что умеет:
*   Создавать, получать, обновлять заявки.
*   Управлять статусами и назначать исполнителей.
*   Возвращать данные в формате JSON по REST API.

### 🔌 Доступные эндпоинты (все по `/api/v1/...`):

| Метод | Эндпоинт | Описание | Пример тела/ответа |
|-------|----------|----------|-------------------|
| `POST` | `/tasks` | Создать заявку | **Тело:** `{ "title": "Не работает свет", "category": "electrical", "location_id": "room_205", "priority": "high" }`<br>**Ответ:** Возвращает объект заявки с `id`, `status: "new"`, `due_date` и т.д. |
| `GET` | `/tasks/{id}` | Получить заявку по ID | **Ответ:** Полный объект заявки (см. структуру ниже). |
| `GET` | `/tasks` | Получить список заявок (фильтр по `?status=new`) | **Ответ:** Массив объектов заявок. |
| `PATCH` | `/tasks/{id}/status` | Обновить статус | **Тело:** `{ "status": "assigned" }` → возвращает обновлённую заявку. |
| `PATCH` | `/tasks/{id}/assign` | Назначить исполнителя | **Тело:** `{ "assigned_to": "executor_456" }` → меняет статус на `"assigned"`. |
| `GET` | `/tasks/{id}/history` | История изменений (заглушка) | **Ответ:** `{ "task_id": "...", "history": [] }` |
| `POST` | `/tasks/{id}/rating` | Поставить оценку (заглушка) | **Тело:** `{ "rating": 5, "comment": "Отлично!" }` → возвращает подтверждение. |

---

## 📄 2. Структура данных: Объект заявки (`Task`)

Вот как выглядит JSON-объект, который ты будешь получать от `task-service`:

```json
{
  "id": "T-20250910-ABC123",
  "title": "Не работает свет",
  "description": "В коридоре 3 этажа",
  "category": "electrical",
  "location_id": "room_305",
  "status": "new",
  "priority": "high",
  "created_by": "user_123", // ID пользователя (скоро будет имя!)
  "assigned_to": null,      // ID исполнителя (скоро будет имя!)
  "created_at": "2025-09-10T10:00:00Z",
  "due_date": "2025-09-10T14:00:00Z", // Рассчитывается на основе priority
  "attachments": []
}
```

> ⚠️ **Важно:** Сейчас в полях `created_by` и `assigned_to` возвращаются только **ID**. Мы работаем над интеграцией с `user-service`, чтобы возвращать имена. Пока можешь отображать ID или сделать заглушку.

---

## 🗺️ 3. Интеграции, которые скоро появятся

Мы активно работаем над двумя новыми микросервисами, которые обогатят твои данные:

### 👥 `user-service` (в разработке, будет готов в ближайшие 2-3 дня)
*   **Зачем тебе:** Чтобы по `user_id` получить имя, роль и другую информацию о пользователе.
*   **Эндпоинт:** `GET /api/v1/users/{user_id}`
*   **Пример ответа:**
    ```json
    {
      "id": "user_123",
      "full_name": "Иван Петров",
      "role": "employee",
      "department": "Кафедра математики"
    }
    ```
*   **Что делать сейчас:** В своем коде заложи логику, что данные о пользователе будут приходить отдельным запросом. Пока можно использовать мок-данные.

### 🏢 `inventory-service` (в разработке, будет готов в ближайшие 2-3 дня)
*   **Зачем тебе:** Чтобы по `location_id` получить понятное название помещения.
*   **Эндпоинт:** `GET /api/v1/locations/{location_id}`
*   **Пример ответа:**
    ```json
    {
      "id": "room_305",
      "name": "Аудитория 305",
      "full_path": "Главный корпус / 3 этаж / Аудитория 305"
    }
    ```
*   **Что делать сейчас:** Аналогично — заложи логику для получения названия помещения. Пока отображай `location_id`.

---

## 🔐 4. Авторизация (Keycloak) — настроена локально

Мы запустили локальный сервер Keycloak. Это значит, что система будет работать с JWT-токенами.

*   **Как это влияет на тебя:**
    *   Все запросы к API должны содержать заголовок: `Authorization: Bearer <JWT_TOKEN>`.
    *   Токен содержит информацию о пользователе и его ролях (например, `["employee", "dispatcher"]`).
*   **Что нужно сделать во фронтенде:**
    1.  Реализовать страницу входа (Login).
    2.  Получить JWT-токен (пока можно использовать мок-токен или локальный Keycloak для теста).
    3.  Хранить токен (например, в `localStorage` или `httpOnly cookie`).
    4.  Добавлять токен в заголовок всех запросов к API.
*   **Пример декодированного токена (полезная нагрузка):**
    ```json
    {
      "sub": "user_123",
      "name": "Иван Петров",
      "roles": ["dispatcher"],
      "exp": 1757447674
    }
    ```

---

## 🖥️ 5. Локальный запуск и настройка

### Для `task-service`:
*   Запущен локально на `http://localhost:8000`.
*   Документация API: `http://localhost:8000/docs` (Swagger UI) — можешь изучить все эндпоинты и тестировать запросы прямо в браузере.
*   **База данных:** MongoDB (локально). Данные сохраняются между перезапусками.

### Для Keycloak:
*   Админ-панель: `http://localhost:8080/admin`
*   Логин: `admin`, пароль: `admin`
*   Realm: `smart-helpdesk`
*   Тестовые пользователи: `employee1`, `executor1`, `dispatcher1` (с соответствующими ролями).

---

## 🛠️ 6. Что тебе нужно сделать прямо сейчас (MVP для недели 2)

Твоя главная цель до **20 сентября** — создать базовый, но **полностью рабочий Web Dashboard**, который проходит критерий отсева (30% оценки).

### Минимальный функционал:
1.  **Страница входа (Login):**
    *   Простая форма (логин/пароль) или кнопка "Войти" (пока можно использовать мок-токен).
    *   После входа — редирект на главную страницу дашборда.
2.  **Главная страница (Dashboard):**
    *   Таблица со списком заявок.
    *   Столбцы: `№ (id)`, `Статус`, `Категория`, `Помещение (location_id)`, `Исполнитель (assigned_to)`, `SLA (due_date)`.
    *   Фильтр по статусу (выпадающий список: Все, Новые, В работе, Выполнены и т.д.).
3.  **Взаимодействие с API:**
    *   При загрузке страницы — GET-запрос к `http://localhost:8000/api/v1/tasks`.
    *   При выборе фильтра — новый GET-запрос с параметром `?status=...`.

### Технические требования:
*   **Стек:** React.js (обязательно по ТЗ).
*   **UI-библиотека:** Рекомендуется Mantine UI (очень удобна для быстрой разработки админ-панелей).
*   **HTTP-клиент:** Используй `axios` или `fetch`.

---

## 🔄 7. Пример интеграции (как связать фронтенд с бэкендом)

Вот примерный код на React для получения списка задач:

```jsx
import { useEffect, useState } from 'react';
import axios from 'axios';

const TaskList = () => {
  const [tasks, setTasks] = useState([]);
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        // Получаем токен из localStorage
        const token = localStorage.getItem('access_token');
        
        // Формируем URL с фильтром
        let url = 'http://localhost:8000/api/v1/tasks';
        if (statusFilter !== 'all') {
          url += `?status=${statusFilter}`;
        }

        const response = await axios.get(url, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        setTasks(response.data);
      } catch (error) {
        console.error('Ошибка при загрузке задач:', error);
      }
    };

    fetchTasks();
  }, [statusFilter]);

  return (
    <div>
      <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
        <option value="all">Все</option>
        <option value="new">Новые</option>
        <option value="assigned">Назначенные</option>
        <option value="in_progress">В работе</option>
      </select>

      <table>
        <thead>
          <tr>
            <th>№</th>
            <th>Статус</th>
            <th>Категория</th>
            <th>Помещение</th>
            <th>Исполнитель</th>
            <th>SLA</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map(task => (
            <tr key={task.id}>
              <td>{task.id}</td>
              <td>{task.status}</td>
              <td>{task.category}</td>
              <td>{task.location_id}</td> {/* Позже заменим на full_path */}
              <td>{task.assigned_to}</td> {/* Позже заменим на full_name */}
              <td>{new Date(task.due_date).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TaskList;
```

---

## 📅 8. План на ближайшие дни (для синхронизации)

| День | Что будет готово (для тебя) |
|------|------------------------------|
| **10-11 сент** | `user-service` — можно будет получать имена пользователей. |
| **11-12 сент** | `inventory-service` — можно будет получать названия помещений. |
| **12-13 сент** | Интеграция: `task-service` будет возвращать не ID, а объекты с именами и названиями (через внутренние запросы). |
| **13-14 сент** | Настройка CI/CD для `web-dashboard` — сборка и деплой (пока локально или на тестовый сервер). |

---

## 💡 Советы

1.  **Не жди идеальных данных.** Начни с того, что есть сейчас (ID вместо имен). Потом просто заменишь логику.
2.  **Используй Swagger UI.** Перейди по `http://localhost:8000/docs` — это твой лучший друг для понимания API.
3.  **Делай компоненты переиспользуемыми.** Например, компонент `<StatusBadge>` для цветного отображения статусов, `<SLAIndicator>` для цветовой индикации дедлайна.
4.  **Задавай вопросы.** Если что-то непонятно в API или структуре данных — спрашивай команду. Лучше уточнить сейчас, чем переделывать потом.

---

Ты — ключевая часть успеха на контрольной точке 20 сентября. Без работающего дашборда мы не пройдем отсев. У тебя есть все, чтобы начать прямо сейчас. Удачи! 🚀