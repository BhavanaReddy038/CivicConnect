from database.database import engine
from sqlalchemy import text

with engine.connect() as connection:

    print("=== ANY POSTGRES RELATION NAMED idx_locations_point ===")

    result = connection.execute(
        text("""
            SELECT
                n.nspname AS schema_name,
                c.relname AS relation_name,
                c.relkind AS relation_type
            FROM pg_class c
            JOIN pg_namespace n
                ON n.oid = c.relnamespace
            WHERE c.relname = 'idx_locations_point';
        """)
    )

    rows = result.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("NO RELATION FOUND")

    print("\n=== LOCATIONS TABLE ===")

    result = connection.execute(
        text("""
            SELECT
                n.nspname AS schema_name,
                c.relname AS table_name,
                c.relkind AS relation_type
            FROM pg_class c
            JOIN pg_namespace n
                ON n.oid = c.relnamespace
            WHERE c.relname = 'locations';
        """)
    )

    rows = result.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("LOCATIONS NOT FOUND")