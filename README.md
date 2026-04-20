# Order Processing Saga System (Kafka + FastAPI + PostgreSQL)

Мини-система обработки заказов, реализованная в виде **event-driven архитектуры** с использованием **Saga-паттерна**, **Apache Kafka**, **FastAPI**, **PostgreSQL** и **OAuth2 (JWT)**.
Проект демонстрирует построение отказоустойчивой распределённой системы с асинхронным взаимодействием сервисов.

---

## Основные возможности

- Асинхронная обработка заказов через Kafka
- Saga orchestration (с компенсациями)
- Ретраи и DLQ при сбоях
- Идемпотентность сообщений
- JWT-аутентификация и авторизация
- Чёткое разделение ответственности сервисов

---

## Технологический стек

| Компонент           | Технология                              |
|---------------------|------------------------------------------|
| **API**             | FastAPI                                  |
| **Брокер**          | Apache Kafka                             |
| **БД**              | PostgreSQL                               |
| **Аутентификация**  | OAuth2 (JWT) — access + refresh токены   |
| **Клиент Kafka**    | `confluent-kafka-python`                 |
| **Контейнеризация** | Docker + Docker Compose                  |
| **Язык**            | Python                                   |
| **Миграции**        | Alembic                                  |

---

## Сервисы

### Auth Service
- Регистрация и логин
- Выдача JWT (access + refresh)
- Валидация токенов

---

### Order API
- `POST /orders`
- Сохраняет заказ в PostgreSQL
- Публикует `order.created`

---

### Orchestrator
- Управляет сагой
- Хранит состояние
- Запускает компенсации

---

### Inventory Service
- Резервирует товар (80% успеха)
- Обрабатывает команды:
  - `reserve_inventory`
  - `cancel_reservation`
  - Ретраи (3 провала -> event уходит в DLQ)

---

### Payment Service
- Обработка платежей (70% успеха)
- Команды:
  - `charge_payment`
  - `refund_payment`
- Ретраи (3 провала -> event уходит в DLQ)

---

### Notification Service
- Подписан на `order.events`
- Логирует события
