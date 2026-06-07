from database import SessionLocal, engine
from models import Base, Book


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(Book).count() > 0:
        print("Database already has books — skipping seed.")
        db.close()
        return

    books = [
        Book(
            title="Co-Intelligence: Living and Working with AI",
            author="Ethan Mollick",
            status="read",
            rating=5,
        ),
        Book(
            title="The Coming Wave",
            author="Mustafa Suleyman",
            status="read",
            rating=5,
        ),
        Book(
            title="Nexus: A Brief History of Information Networks",
            author="Yuval Noah Harari",
            status="read",
            rating=4,
        ),
        Book(
            title="Power and Progress",
            author="Daron Acemoglu & Simon Johnson",
            status="reading",
            rating=None,
        ),
        Book(
            title="Supremacy: AI, ChatGPT, and the Race That Will Change the World",
            author="Parmy Olson",
            status="read",
            rating=4,
        ),
        Book(
            title="The Worlds I See",
            author="Fei-Fei Li",
            status="read",
            rating=5,
        ),
        Book(
            title="The AI Mirror",
            author="Shannon Vallor",
            status="want_to_read",
            rating=None,
        ),
        Book(
            title="Impromptu: Amplifying Our Humanity Through AI",
            author="Reid Hoffman",
            status="read",
            rating=4,
        ),
        Book(
            title="Genesis: Artificial Intelligence, Hope, Anger and the Human Mind",
            author="Henry Kissinger & Eric Schmidt",
            status="want_to_read",
            rating=None,
        ),
        Book(
            title="The Alignment Problem",
            author="Brian Christian",
            status="read",
            rating=5,
        ),
    ]

    db.add_all(books)
    db.commit()
    print(f"Seeded {len(books)} books successfully.")
    db.close()


if __name__ == "__main__":
    seed()
