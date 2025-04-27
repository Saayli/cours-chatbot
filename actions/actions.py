from typing import Any, Text, Dict, List

from rasa_sdk import Action, FormValidationAction, Tracker
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import sqlite3
import random
import string
from datetime import datetime

DB_PATH = "reservation_bot.db"

# --- Form validation (optional but recommended) ---
class ValidateReservationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_reservation_form"

    async def validate_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Here you could add real date parsing/validation
        return {"date": slot_value}

    async def validate_time(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Basic format check
        return {"time": slot_value}

    async def validate_people(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        try:
            count = int(slot_value)
            if count > 0:
                return {"people": slot_value}
        except ValueError:
            pass
        dispatcher.utter_message(text="Je n'ai pas compris le nombre de personnes, peux-tu reformuler ?")
        return {"people": None}

    async def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        return {"name": slot_value}

    async def validate_phone_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Basic French phone pattern
        if isinstance(slot_value, str) and slot_value.isdigit() and len(slot_value) == 10:
            return {"phone_number": slot_value}
        dispatcher.utter_message(text="Le numéro de téléphone semble invalide. Veux-tu réessayer ?")
        return {"phone_number": None}

# --- Submit reservation ---
class ActionSubmitReservation(Action):

    def name(self) -> str:
        return "action_submit_reservation"

    def generate_reservation_number(self) -> str:
        """Génère un numéro de réservation aléatoire."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: dict):
        # Récupérer les slots
        date = tracker.get_slot('date')
        time = tracker.get_slot('time')
        people = tracker.get_slot('people')
        name = tracker.get_slot('name')
        phone_number = tracker.get_slot('phone_number')
        comment = tracker.get_slot('comment')

        # Générer un numéro de réservation
        reservation_number = self.generate_reservation_number()

        try:
            # Connexion à la base de données
            conn = sqlite3.connect('reservation_bot.db')
            cursor = conn.cursor()

            # Insertion dans la table reservations
            cursor.execute("""
                INSERT INTO reservations (reservation_number, date, people, name, phone, comment, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                reservation_number,
                f"{date} {time}",  # date et heure combinées
                people,
                name,
                phone_number,
                comment if comment else '',
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))

            conn.commit()
            conn.close()

            # Répondre à l'utilisateur
            dispatcher.utter_message(text=f"✅ Votre réservation est confirmée : {reservation_number}")

            # Retourner aussi un SlotSet si besoin
            return [SlotSet("reservation_number", reservation_number)]

        except Exception as e:
            dispatcher.utter_message(text=f"❌ Erreur lors de l'enregistrement de votre réservation. ({str(e)})")
            return []

# --- Add comment ---
class ActionAddComment(Action):
    def name(self) -> Text:
        return "action_add_comment"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[EventType]:
        comment = tracker.get_slot("comment")
        reservation_number = tracker.get_slot("reservation_number")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE reservations SET comment = ? WHERE reservation_number = ?",
            (comment, reservation_number)
        )
        conn.commit()
        conn.close()

        dispatcher.utter_message(text="J'ai ajouté votre commentaire à la réservation.")
        return []

# --- Show reservation ---
class ActionShowReservation(Action):
    def name(self) -> Text:
        return "action_show_reservation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[EventType]:
        reservation_number = tracker.get_slot("reservation_number")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT date, people, name, phone, comment FROM reservations WHERE reservation_number = ?",
            (reservation_number,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            date, people, name, phone, comment = row
            msg = f"Réservation n°{reservation_number} :\nDate & heure: {date}\nPersonnes: {people}\nNom: {name}\nTél.: {phone}"
            if comment:
                msg += f"\nCommentaire: {comment}"
            dispatcher.utter_message(text=msg)
        else:
            dispatcher.utter_message(text="Je n'ai pas trouvé de réservation avec ce numéro.")
        return []

# --- Cancel reservation ---
class ActionCancelReservation(Action):
    def name(self) -> Text:
        return "action_cancel_reservation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[EventType]:
        reservation_number = tracker.get_slot("reservation_number")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM reservations WHERE reservation_number = ?",
            (reservation_number,)
        )
        conn.commit()
        conn.close()

        dispatcher.utter_message(template="utter_cancel_confirmation")
        return []

# --- Show menu ---
class ActionShowMenu(Action):
    def name(self) -> Text:
        return "action_show_menu"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[EventType]:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name, description FROM dishes WHERE is_daily = 1")
        dishes = cursor.fetchall()
        conn.close()
        if dishes:
            msg = "\n".join([f"- {n}: {d}" for n,d in dishes])
            dispatcher.utter_message(text=f"Voici le menu du jour :\n{msg}")
        else:
            dispatcher.utter_message(text="Désolé, le menu du jour n'est pas disponible.")
        return []

# --- Show allergens ---
class ActionShowAllergens(Action):
    def name(self) -> Text:
        return "action_show_allergens"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[EventType]:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT a.name FROM allergens a JOIN dish_allergens da ON a.id = da.allergen_id GROUP BY a.name"
        )
        allergens = [row[0] for row in cursor.fetchall()]
        conn.close()
        if allergens:
            dispatcher.utter_message(template="utter_allergens_list", allergen_names=", ".join(allergens))
        else:
            dispatcher.utter_message(text="Aucun allergène enregistré.")
        return []

# --- Show full menu ---
class ActionShowFullMenu(Action):
    def name(self) -> Text:
        return "action_show_full_menu"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[EventType]:
        dispatcher.utter_message(template="utter_full_menu_link")
        return []
