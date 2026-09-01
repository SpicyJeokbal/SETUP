import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE_NAME = "sample"

app = FastAPI()

#ACL permit any
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          
    allow_methods=["*"],
    allow_headers=["*"],
)

#acl permit
class Task(BaseModel):
    title: str
    done: bool = False
    priority: str = "normal"

@app.get("/tasks")
def get_tasks():
    res = supabase.table(TABLE_NAME).select("*").execute()
    return res.data

@app.post("/tasks")
def create_task(task: Task):
    res = supabase.table(TABLE_NAME).insert(task.model_dump()).execute()
    return res.data

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    res = supabase.table(TABLE_NAME).update(task.model_dump()).eq("id", task_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Task not found")
    return res.data

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    res = supabase.table(TABLE_NAME).delete().eq("id", task_id).execute()
    return {"deleted": task_id}