import sqlite3
from tabulate import tabulate

def lire_reservations(db_path="reservation_bot.db"):
    try:
        # Connexion à la base en lecture seule
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()

        # Lire toutes les réservations
        cursor.execute("SELECT id, reservation_number, date, people, name, phone, comment, created_at FROM reservations")
        rows = cursor.fetchall()

        # Affichage propre avec tabulate
        headers = ["ID", "Numéro réservation", "Date", "Personnes", "Nom", "Téléphone", "Commentaire", "Créé le"]
        print(tabulate(rows, headers=headers, tablefmt="grid"))

    except sqlite3.OperationalError as e:
        print(f"Erreur SQLite: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    lire_reservations()
