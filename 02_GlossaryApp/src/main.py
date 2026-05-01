import os
from dotenv import load_dotenv
from database.db_manager import DatabaseManager
from gui.app import GlossaryApp

def main():
    # Load enviroiment variable
    load_dotenv()

    # Get database name from .env file, if not found, use default value
    db_name = os.getenv("DATABASE_NAME", "glossary.db")

    try:
        # Init DatabaseManager
        db_manager = DatabaseManager(db_name)

        app = GlossaryApp(db_manager)
        app.mainloop()

    except Exception as e:
        print(f"Error : {e}")
    finally:
        if 'db_manager' in locals():
            db_manager.close()

if __name__ == "__main__":
    main()
