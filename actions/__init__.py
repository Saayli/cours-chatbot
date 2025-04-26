import sqlite3

conn = sqlite3.connect("reservation_bot.db")
cursor = conn.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS reservations ( id INTEGER PRIMARY KEY AUTOINCREMENT, reservation_number TEXT UNIQUE, date TEXT NOT NULL, people INTEGER NOT NULL, name TEXT NOT NULL, phone TEXT NOT NULL, comment TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ) """)
cursor.execute(""" CREATE TABLE IF NOT EXISTS menus ( id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL, description TEXT ) """)
cursor.execute(""" CREATE TABLE IF NOT EXISTS dishes ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT, type TEXT, is_daily BOOLEAN DEFAULT 0, menu_id INTEGER, FOREIGN KEY (menu_id) REFERENCES menus(id) ) """)
cursor.execute(""" CREATE TABLE IF NOT EXISTS allergens ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE ) """)
cursor.execute(""" CREATE TABLE IF NOT EXISTS dish_allergens ( dish_id INTEGER NOT NULL, allergen_id INTEGER NOT NULL, PRIMARY KEY (dish_id, allergen_id), FOREIGN KEY (dish_id) REFERENCES dishes(id), FOREIGN KEY (allergen_id) REFERENCES allergens(id) ) """)


conn.commit()
conn.close()