from db import SessionLocal


# Dependency
def get_db():
    db = SessionLocal()
    try:
        # for sqlite3
        db.execute("PRAGMA foreign_keys = ON;")
        yield db
    finally:
        db.close()
