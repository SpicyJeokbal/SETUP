from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

TABLE_NAME = "sample"

#result = supabase.table("tasks").insert({"title": "test task", "done": False, "priority": "high"}).execute()
result = supabase.table(TABLE_NAME).insert([{"id": 123456, "title": "Bitch", "done": True, "priority": "low"},
                                         {"id": 55555, "title": "hello", "done": True, "priority": "low"}]).execute()

for task in result.data:
    print(task)
    print("")