import sqlite3

def inspect_db(db_path="reservation_bot.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Liste toutes les tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables existantes :", tables)

    if tables:
        for table_name, in tables:
            print(f"\nContenu de la table {table_name} :")
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
    else:
        print("⚠️ Aucune table trouvée.")

    conn.close()

if __name__ == "__main__":
    inspect_db()
