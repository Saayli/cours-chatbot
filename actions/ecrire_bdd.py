import sqlite3
import random
import string

def inserer_reservation_test(db_path="reservation_bot.db"):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Générer un numéro de réservation aléatoire
        reservation_number = "TEST" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # Insérer une ligne de test
        cursor.execute("""
            INSERT INTO reservations (reservation_number, date, people, name, phone, comment)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            reservation_number,      # reservation_number
            "01/05/2025",             # date
            4,                        # people
            "Testeur",                # name
            "0600000000",              # phone
            "Test d'insertion"         # comment
        ))

        conn.commit()
        print(f"✅ Réservation de test insérée avec numéro : {reservation_number}")

    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")

    finally:
        conn.close()

if __name__ == "__main__":
    inserer_reservation_test()
