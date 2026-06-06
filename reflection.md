# Week 04 API Reflection

## 1. What is the difference between the SQLAlchemy model and the Pydantic schema? They're both about "Book" but they serve different purposes?

The SQLAlchemy model defines the actual database table and its columns — it talks to PostgreSQL. The Pydantic schema defines what data is allowed in and out of the API — it talks to the outside world.

## 2. What does `Depends(get_db)` do? Why does every endpoint need it

It automatically opens a database session before the endpoint runs and closes it when done. Every endpoint needs it because without a session there is no way to read or write to PostgreSQL.

## 3. When you restarted the server and your data was still there — how does that feel compared to storing data in a Python list? What changed architecturally?

With a Python list the data lived in RAM and died with the server. Now data lives in PostgreSQL which is completely separate from the Python process — the server can restart without touching the database.

## 4. What was the most confusing part of connecting the frontend to the backend?

Understanding that the frontend and backend are completely separate processes that only communicate over HTTP fetch calls — the frontend imports nothing from the backend.

## 5. When does CORS become a problem and why? In your own words.

CORS blocks requests when the frontend and backend run on different origins — in our case different ports (3000 vs 8000). The browser blocks it by default as a security measure until the backend explicitly allows it.

## 6. What is the difference between useEffect with [] and without it?

useEffect with [] runs once when the page loads. Without [] it runs after every re-render, which would cause an infinite fetch loop.