from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Book, Base
from schemas import BookCreate, BookUpdate, BookResponse

import anthropic  # Anthropic SDK for calling Claude
from dotenv import load_dotenv  # reads .env file into environment
from pydantic import BaseModel  # needed for ChatRequest model

load_dotenv()  # load ANTHROPIC_API_KEY from .env before anything else runs

# Create tables in the database if they don't exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Tracker API", version="2.0.0")

# Initialize the Anthropic client — reads ANTHROPIC_API_KEY from environment
ai_client = anthropic.Anthropic()

# Schema for incoming chat requests
class ChatRequest(BaseModel):
    message: str                        # the user's current message
    conversation_history: list[dict] = []  # all prior turns, default empty

# CORS — allows the Next.js frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Book Tracker API v2"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/books", response_model=list[BookResponse])
def get_books(status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Book)
    if status:
        query = query.filter(Book.status == status)
    return query.all()

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(data: BookCreate, db: Session = Depends(get_db)):
    book = Book(**data.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, updates: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if updates.status is not None:
        book.status = updates.status
    if updates.rating is not None:
        book.rating = updates.rating
    db.commit()
    db.refresh(book)
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": f"Book {book_id} deleted"}

@app.post("/ai/chat")
def chat_with_assistant(request: ChatRequest):
    # Combine prior conversation history with the new user message
    messages = request.conversation_history + [
        {"role": "user", "content": request.message}
    ]

    # Send to Claude
    response = ai_client.messages.create(
        model="claude-haiku-4-5-20251001",  # fast and cost-effective
        max_tokens=1024,
        system="""You are a helpful book assistant for a personal book tracking app. 
          Help users discover books, discuss what they've read, and get personalized recommendations.
          Be conversational, enthusiastic about books, and concise in your responses.""",
        messages=messages
    )

    # Extract the text from Claude's response
    reply = response.content[0].text

    # Return the reply plus the full updated history for the frontend to store
    return {
        "reply": reply,
        "updated_history": messages + [{"role": "assistant", "content": reply}]
    }


@app.post("/ai/recommend")
def get_recommendations(request: ChatRequest, db: Session = Depends(get_db)):
    # Pull all books from the database
    books = db.query(Book).all()

    # Separate by status
    read_books = [b for b in books if b.status == "read"]
    reading_books = [b for b in books if b.status == "reading"]

    # Build a plain-text summary of the user's library to inject into the prompt
    book_context = "Here is the user's book library:\n"

    if read_books:
        book_context += "\nBooks they've read:\n"
        for b in read_books:
            rating_str = f" (rated {b.rating}/5)" if b.rating else ""
            book_context += f"- {b.title} by {b.author}{rating_str}\n"

    if reading_books:
        book_context += "\nCurrently reading:\n"
        for b in reading_books:
            book_context += f"- {b.title} by {b.author}\n"

    if not read_books and not reading_books:
        book_context += "No books tracked yet.\n"

    # Inject the library into the system prompt so Claude knows what you've read
    system_prompt = f"""You are a personalized book recommendation assistant.

{book_context}

Based on this reading history, provide thoughtful, personalized recommendations.
Be specific about why each recommendation matches their taste.
Keep responses concise — 2-3 recommendations at most unless asked for more."""

    # Build the messages list the same way as /ai/chat
    messages = request.conversation_history + [
        {"role": "user", "content": request.message}
    ]

    response = ai_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        system=system_prompt,
        messages=messages
    )

    reply = response.content[0].text
    return {
        "reply": reply,
        "updated_history": messages + [{"role": "assistant", "content": reply}]
    }