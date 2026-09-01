// server.js
const express = require("express");
const cors = require("cors");
const { createClient } = require("@supabase/supabase-js");
require("dotenv").config();

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);

const TABLE_NAME = "tasks";   // <- change only this to switch tables

const app = express();
app.use(cors());              // same ACL role as CORSMiddleware in Python
app.use(express.json());      // lets Express read JSON request bodies

// GET — read all rows
app.get("/tasks", async (req, res) => {
  const { data, error } = await supabase.from(TABLE_NAME).select("*");
  if (error) return res.status(500).json({ error: error.message });
  res.json(data);
});

// POST — create a new row
app.post("/tasks", async (req, res) => {
  const { title, done = false } = req.body;
  const { data, error } = await supabase.from(TABLE_NAME).insert({ title, done }).select();
  if (error) return res.status(500).json({ error: error.message });
  res.json(data);
});

// PUT — update an existing row by ID
app.put("/tasks/:id", async (req, res) => {
  const { title, done } = req.body;
  const { data, error } = await supabase
    .from(TABLE_NAME)
    .update({ title, done })
    .eq("id", req.params.id)
    .select();
  if (error) return res.status(500).json({ error: error.message });
  if (!data.length) return res.status(404).json({ detail: "Task not found" });
  res.json(data);
});

// DELETE — remove a row by ID
app.delete("/tasks/:id", async (req, res) => {
  const { error } = await supabase.from(TABLE_NAME).delete().eq("id", req.params.id);
  if (error) return res.status(500).json({ error: error.message });
  res.json({ deleted: req.params.id });
});

app.listen(8000, () => console.log("Server running on http://localhost:8000"));