from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import mysql.connector
import os

app = FastAPI()

# Modelo de dados
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    purchased: bool = False


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "rootpass"),
        database=os.getenv("DB_NAME", "listdb")
    )


@app.get("/")
def main():
    return {
        "/list": "Listagem de tarefas",
        "/create": "Criar uma nova tarefa",
        "/update": "Atualizar uma tarefa",
        "/delete": "Deletar uma tarefa"
    }


@app.get("/list")
def list_items():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM list;")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


@app.post("/create")
def create_item(item: Item):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO list (name, description, purchased) VALUES (%s, %s, %s);",
        (item.name, item.description, item.purchased)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Item criado com sucesso!", "item": item}


@app.put("/update/{item_id}")
def update_item(item_id: int, item: Item):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE list SET name = %s, description = %s, purchased = %s WHERE id = %s;",
        (item.name, item.description, item.purchased, item_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Item atualizado com sucesso!", "item": item}


@app.delete("/delete/{item_id}")
def delete_item(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM list WHERE id = %s;", (item_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": f"Item {item_id} deletado com sucesso!"}
