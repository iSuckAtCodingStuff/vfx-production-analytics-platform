from sqlalchemy import text

from pipeline.db import (
    dispose_engine,
    get_engine,
    test_connection,
)


def main():

    if not test_connection():
        print("Database connection failed.")
        return

    engine = get_engine()

    with engine.connect() as conn:
        version = conn.execute(text("SELECT version();")).scalar()

    print(version)

    dispose_engine()


if __name__ == "__main__":
    main()
    