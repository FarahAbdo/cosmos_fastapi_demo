# FastAPI Cosmos DB Demo

A simple yet powerful REST API demonstration using FastAPI and Azure Cosmos DB Emulator.

## Features

- CRUD operations with Cosmos DB
- FastAPI implementation
- Local development with Cosmos DB Emulator
- Postman collection included

## Project Structure

cosmos-fastapi-demo/
├── main.py           # Main FastAPI application
├── README.md         # Documentation
└── requirements.txt  # Dependencies


## Quick Start

1. **Prerequisites**
```bash
pip install fastapi uvicorn azure-cosmos pydantic
```

2. **Start Cosmos DB Emulator**

3. **Run the API**
```bash
uvicorn main:app --reload
```


## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | /items/ | Create new item |
| GET | /items/{item_id} | Get single item |
| GET | /items/category/{category} | List items by category |
| PUT | /items/{item_id} | Update item |
| DELETE | /items/{item_id} | Delete item |

