# FastAPI Приложение: Управление грибами и корзинками

Это простое FastAPI приложение для управления двумя сущностями: **грибы** и **корзинки**. Грибы можно создавать, обновлять и добавлять в корзинки. Корзинки имеют ограниченную вместимость, и грибы можно удалять из них.

## Запуск приложения

1. Установите зависимости:
   ```bash
   pip install fastapi uvicorn
   ```

2. Запустите сервер:
   ```bash
   uvicorn main:app --reload
   ```

3. Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000).

---

## API Endpoints

### Грибы

#### 1. Создать гриб
**POST** `/mushrooms/`

Пример запроса:
```bash
curl -X POST "http://localhost:8000/mushrooms/" -H "Content-Type: application/json" -d '{
  "name": "Белый гриб",
  "edible": true,
  "weight": 150,
  "freshness": 8
}'
```

Пример ответа:
```json
{
  "id": 1,
  "name": "Белый гриб",
  "edible": true,
  "weight": 150,
  "freshness": 8
}
```

---

#### 2. Обновить информацию о грибе
**PUT** `/mushrooms/{mushroom_id}`

Пример запроса:
```bash
curl -X PUT "http://localhost:8000/mushrooms/1" -H "Content-Type: application/json" -d '{
  "name": "Подосиновик",
  "edible": true,
  "weight": 200,
  "freshness": 7
}'
```

Пример ответа:
```json
{
  "id": 1,
  "name": "Подосиновик",
  "edible": true,
  "weight": 200,
  "freshness": 7
}
```

---

#### 3. Получить информацию о грибе
**GET** `/mushrooms/{mushroom_id}`

Пример запроса:
```bash
curl -X GET "http://localhost:8000/mushrooms/1"
```

Пример ответа:
```json
{
  "id": 1,
  "name": "Подосиновик",
  "edible": true,
  "weight": 200,
  "freshness": 7
}
```

---

#### 4. Получить список всех грибов
**GET** `/mushrooms/`

Пример запроса:
```bash
curl -X GET "http://localhost:8000/mushrooms/"
```

Пример ответа:
```json
[
  {
    "id": 1,
    "name": "Подосиновик",
    "edible": true,
    "weight": 200,
    "freshness": 7
  }
]
```

---

### Корзинки

#### 1. Создать корзинку
**POST** `/baskets/`

Пример запроса:
```bash
curl -X POST "http://localhost:8000/baskets/" -H "Content-Type: application/json" -d '{
  "owner": "Иван",
  "capacity": 1000
}'
```

Пример ответа:
```json
{
  "id": 1,
  "owner": "Иван",
  "capacity": 1000,
  "mushrooms": []
}
```

---

#### 2. Добавить гриб в корзинку
**POST** `/baskets/{basket_id}/add?mushroom_id={mushroom_id}`

Пример запроса:
```bash
curl -X POST "http://localhost:8000/baskets/1/add?mushroom_id=1"
```

Пример ответа:
```json
{
  "message": "Mushroom added successfully"
}
```

---

#### 3. Удалить гриб из корзинки
**DELETE** `/baskets/{basket_id}/remove?mushroom_id={mushroom_id}`

Пример запроса:
```bash
curl -X DELETE "http://localhost:8000/baskets/1/remove?mushroom_id=1"
```

Пример ответа:
```json
{
  "message": "Mushroom removed successfully"
}
```

---

#### 4. Получить информацию о корзинке
**GET** `/baskets/{basket_id}`

Пример запроса:
```bash
curl -X GET "http://localhost:8000/baskets/1"
```

Пример ответа:
```json
{
  "id": 1,
  "owner": "Иван",
  "capacity": 1000,
  "mushrooms": [
    {
      "id": 1,
      "name": "Подосиновик",
      "edible": true,
      "weight": 200,
      "freshness": 7
    }
  ]
}
```

---

#### 5. Получить список всех корзинок
**GET** `/baskets/`

Пример запроса:
```bash
curl -X GET "http://localhost:8000/baskets/"
```

Пример ответа:
```json
[
  {
    "id": 1,
    "owner": "Иван",
    "capacity": 1000,
    "mushrooms": [1]
  }
]
```

---

## Модели данных

### Гриб (`Mushroom`)
- **id**: Уникальный идентификатор (int)
- **name**: Название гриба (str)
- **edible**: Съедобность (bool)
- **weight**: Вес в граммах (int)
- **freshness**: Свежесть (int, от 0 до 10)

### Корзинка (`Basket`)
- **id**: Уникальный идентификатор (int)
- **owner**: Владелец корзинки (str)
- **capacity**: Вместимость в граммах (int)
- **mushrooms**: Список ID грибов в корзинке (List[int])

---

## Примеры использования

1. Создайте гриб:
   ```bash
   curl -X POST "http://localhost:8000/mushrooms/" -H "Content-Type: application/json" -d '{
     "name": "Лисичка",
     "edible": true,
     "weight": 100,
     "freshness": 9
   }'
   ```

2. Создайте корзинку:
   ```bash
   curl -X POST "http://localhost:8000/baskets/" -H "Content-Type: application/json" -d '{
     "owner": "Мария",
     "capacity": 500
   }'
   ```

3. Добавьте гриб в корзинку:
   ```bash
   curl -X POST "http://localhost:8000/baskets/1/add?mushroom_id=1"
   ```

4. Проверьте содержимое корзинки:
   ```bash
   curl -X GET "http://localhost:8000/baskets/1"
   ```

---

## Автор
Ваше имя или контактная информация.

## Лицензия
Этот проект распространяется под лицензией MIT.