# Todo App

Una API RESTful para gestionar tareas (todos) construida con FastAPI, SQLAlchemy y SQLite.

## Características
- Crear, leer, actualizar y eliminar tareas (CRUD)
- Filtrar tareas por prioridad
- Validación de datos con Pydantic
- Base de datos SQLite lista para usar

## Instalación

1. Clona este repositorio:
   ```bash
   git clone <url-del-repo>
   cd todo-app
   ```
2. (Opcional) Crea y activa un entorno virtual:
   ```bash
   python -m venv .venv
   # En Windows
   .venv\Scripts\activate
   # En Linux/Mac
   source .venv/bin/activate
   ```
3. Instala las dependencias:
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic starlette
   ```

## Uso

Inicia el servidor de desarrollo:
```bash
uvicorn main:app --reload
```

La API estará disponible en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

La documentación interactiva está en: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Endpoints principales

### Obtener todas las tareas
- **GET** `/mytodos`

#### Ejemplo de respuesta
```json
[
  {
    "id": 1,
    "title": "Comprar víveres",
    "description": "Comprar leche, pan y huevos en el supermercado",
    "priority": 2,
    "complete": false
  }
]
```

### Obtener tarea por ID
- **GET** `/mytodos/{todo_id}`

#### Ejemplo de respuesta
```json
{
  "id": 1,
  "title": "Comprar víveres",
  "description": "Comprar leche, pan y huevos en el supermercado",
  "priority": 2,
  "complete": false
}
```

### Obtener tareas por prioridad
- **GET** `/mytodos/priority/{todo_priority}`

#### Ejemplo de respuesta
```json
[
  {
    "id": 2,
    "title": "Estudiar para el examen",
    "description": "Repasar los temas de matemáticas",
    "priority": 1,
    "complete": false
  }
]
```

### Crear una tarea
- **POST** `/mytodos/createtodo/`

#### Ejemplo de request
```json
{
  "title": "Llamar al médico",
  "description": "Pedir turno para chequeo anual",
  "priority": 3,
  "complete": false
}
```

#### Ejemplo de respuesta
```json
{
  "message": "Todo with id 3 created successfully",
  "todo": {
    "id": 3,
    "title": "Llamar al médico",
    "description": "Pedir turno para chequeo anual",
    "priority": 3,
    "complete": false
  }
}
```

### Actualizar una tarea
- **PUT** `/mytodos/updatetodo/{todo_id}`

#### Ejemplo de request
```json
{
  "title": "Llamar al médico",
  "description": "Pedir turno para chequeo anual y llevar estudios",
  "priority": 3,
  "complete": true
}
```

#### Ejemplo de respuesta
```json
{
  "message": "Todo with id 3 updated successfully",
  "todo": {
    "id": 3,
    "title": "Llamar al médico",
    "description": "Pedir turno para chequeo anual y llevar estudios",
    "priority": 3,
    "complete": true
  }
}
```

### Eliminar una tarea
- **DELETE** `/mytodos/deletetodo/{todo_id}`

#### Ejemplo de respuesta
```json
{
  "message": "Todo with id 3 deleted successfully"
}
```

---

## Estructura del proyecto

```
├── database.py         # Configuración de la base de datos
├── main.py             # Endpoints y lógica principal de la API
├── models.py           # Definición del modelo de datos (ORM)
├── todo_request.py     # Esquema de validación para requests
└── ...
```

---