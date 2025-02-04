# FastAPI: Грибы и корзинки

Простое FastAPI приложение для управления грибами и корзинками. Грибы можно создавать, обновлять и добавлять в корзинки. Корзинки имеют ограниченную вместимость.

---

## Запуск

1.1 Установите зависимости:
   ```bash
   pip install fastapi uvicorn
   ```

1.2 Установите зависимости (ДЛЯ GUI):
   ```bash
   pip install requests tkinter
   ```

2. Запустите сервер:
   ```bash
   uvicorn main:app --reload
   ```

3. Приложение доступно по адресу: [http://localhost:8000](http://localhost:8000).

4. Графический интерфейс gui.py использует tkinter для упрощения манипуляций с АПИ. Необходимо запускать его после запуска сервера.

---

## API

### Грибы

#### Создать гриб
**POST** `/mushrooms/`
```bash
curl -X POST "http://localhost:8000/mushrooms/" -H "Content-Type: application/json" -d '{ "name": "Белый гриб","edible": true,"weight": 150,"freshness": 8}'
```

#### Обновить гриб
**PUT** `/mushrooms/{mushroom_id}`
```bash
curl -X PUT "http://localhost:8000/mushrooms/1" -H "Content-Type: application/json" -d '{ "name": "Подосиновик","edible": true,"weight": 200,"freshness": 7}'
```

#### Получить гриб
**GET** `/mushrooms/{mushroom_id}`
```bash
curl -X GET "http://localhost:8000/mushrooms/1"
```

#### Получить все грибы
**GET** `/mushrooms/`
```bash
curl -X GET "http://localhost:8000/mushrooms/"
```

---

### Корзинки

#### Создать корзинку
**POST** `/baskets/`
```bash
curl -X POST "http://localhost:8000/baskets/" -H "Content-Type: application/json" -d '{"owner": "Иван","capacity": 1000}'
```

#### Добавить гриб в корзинку
**POST** `/baskets/{basket_id}/add?mushroom_id={mushroom_id}`
```bash
curl -X POST "http://localhost:8000/baskets/1/add?mushroom_id=1"
```

#### Удалить гриб из корзинки
**DELETE** `/baskets/{basket_id}/remove?mushroom_id={mushroom_id}`
```bash
curl -X DELETE "http://localhost:8000/baskets/1/remove?mushroom_id=1"
```

#### Получить корзинку
**GET** `/baskets/{basket_id}`
```bash
curl -X GET "http://localhost:8000/baskets/1"
```

#### Получить все корзинки
**GET** `/baskets/`
```bash
curl -X GET "http://localhost:8000/baskets/"
```

---

## Модели

### Гриб
- **id**: Уникальный ID (int)
- **name**: Название (str)
- **edible**: Съедобный? (bool)
- **weight**: Вес в граммах (int)
- **freshness**: Свежесть (int, от 0 до 10)

### Корзинка
- **id**: Уникальный ID (int)
- **owner**: Владелец (str)
- **capacity**: Вместимость в граммах (int)
- **mushrooms**: Список ID грибов (List[int])

---

## Примеры

1. Создайте гриб:
   ```bash
   curl -X POST "http://localhost:8000/mushrooms/" -H "Content-Type: application/json" -d '{"name": "лисичка","edible": true,"weight": 100,"freshness": 9 }'
   ```

2. Создайте корзинку:
   ```bash
   curl -X POST "http://localhost:8000/baskets/" -H "Content-Type: application/json" -d '{"owner": "andrew","capacity": 500}'
   ```

3. Добавьте гриб в корзинку:
   ```bash
   curl -X POST "http://localhost:8000/baskets/1/add?mushroom_id=1"
   ```

4. Проверьте корзинку:
   ```bash
   curl -X GET "http://localhost:8000/baskets/1"
   ```

---
