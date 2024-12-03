import bcrypt
import sqlite3
import time
from datetime import datetime, timedelta
from datetime import datetime

# Initialize all databases
def init_databases():
    conn = sqlite3.connect("health_system.db")
    cursor = conn.cursor()

    # Users table for authentication
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    # Patients table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        contact TEXT NOT NULL
    )
    """)

    # Doctors table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        availability TEXT NOT NULL
    )
    """)

    # Invoices table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        status TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )
    """)

    # Prescriptions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prescriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor TEXT NOT NULL,
        prescription TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )
    """)
    conn.commit()
    conn.close()

# User Authentication System
def register_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (admin/doctor/patient): ").lower()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = sqlite3.connect("health_system.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       (username, hashed_password, role))
        conn.commit()
        print("User registered successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists!")
    conn.close()

def login_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    conn = sqlite3.connect("health_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
        print(f"Login successful! Role: {result[1]}")
        return result[1]
    else:
        print("Invalid username or password!")
        return None

# Billing and Invoicing System
def add_invoice():
    patient_id = int(input("Enter patient ID: "))
    amount = float(input("Enter amount to be billed: "))
    status = input("Enter payment status (paid/unpaid): ").lower()
    conn = sqlite3.connect("health_system.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO invoices (patient_id, amount, status, date) VALUES (?, ?, ?, ?)",
                   (patient_id, amount, status, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    print("Invoice added successfully!")
    conn.close()

def view_invoices():
    conn = sqlite3.connect("health_system.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT i.id, p.name, i.amount, i.status, i.date
    FROM invoices i
    JOIN patients p ON i.patient_id = p.id
    """)
    invoices = cursor.fetchall()
    print("\n--- Invoices ---")
    for invoice in invoices:
        print(f"ID: {invoice[0]}, Patient: {invoice[1]}, Amount: {invoice[2]}, Status: {invoice[3]}, Date: {invoice[4]}")
    conn.close()

# Prescription Management
def add_prescription():
    patient_id = int(input("Enter patient ID: "))
    doctor = input("Enter doctor's name: ")
    prescription = input("Enter prescription details: ")
    conn = sqlite3.connect("health_system.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prescriptions (patient_id, doctor, prescription, date) VALUES (?, ?, ?, ?)",
                   (patient_id, doctor, prescription, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    print("Prescription added successfully!")
    conn.close()

def view_prescriptions():
    patient_id = int(input("Enter patient ID to view prescriptions: "))
    conn = sqlite3.connect("health_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT doctor, prescription, date FROM prescriptions WHERE patient_id = ?", (patient_id,))
    prescriptions = cursor.fetchall()
    print("\n--- Prescriptions ---")
    for prescription in prescriptions:
        print(f"Doctor: {prescription[0]}, Prescription: {prescription[1]}, Date: {prescription[2]}")
    conn.close()

# Doctor Management
def add_doctor():
    name = input("Enter doctor's name: ")
    specialty = input("Enter doctor's specialty: ")
    availability = input("Enter doctor's availability (e.g., Mon-Fri, 10AM-4PM): ")
    conn = sqlite3.connect("health_system.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO doctors (name, specialty, availability) VALUES (?, ?, ?)",
                   (name, specialty, availability))
    conn.commit()
    print("Doctor added successfully!")
    conn.close()

def view_doctors():
    conn = sqlite3.connect("health_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    print("\n--- Doctors ---")
    for doctor in doctors:
        print(f"ID: {doctor[0]}, Name: {doctor[1]}, Specialty: {doctor[2]}, Availability: {doctor[3]}")
    conn.close()

# Advanced Search
def search_patients():
    keyword = input("Enter patient name or ID to search: ")
    conn = sqlite3.connect("health_system.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM patients
    WHERE name LIKE ? OR id = ?
    """, (f"%{keyword}%", keyword if keyword.isdigit() else None))
    patients = cursor.fetchall()
    print("\n--- Search Results ---")
    for patient in patients:
        print(f"ID: {patient[0]}, Name: {patient[1]}, Age: {patient[2]}, Gender: {patient[3]}, Contact: {patient[4]}")
    conn.close()

def add_reminder():
    title = input("Enter the reminder title (e.g., Appointment, Prescription Refill): ")
    patient_id = int(input("Enter patient ID: "))
    reminder_date = input("Enter reminder date (YYYY-MM-DD): ")
    reminder_time = input("Enter reminder time (HH:MM, 24-hour format): ")

    # Combine date and time for the reminder
    reminder_datetime = datetime.strptime(f"{reminder_date} {reminder_time}", "%Y-%m-%d %H:%M")

    conn = sqlite3.connect("health_system.db")
    cursor = conn.cursor()

    # Create reminders table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        reminder_time TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Pending',
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )
    """)
    cursor.execute("INSERT INTO reminders (patient_id, title, reminder_time, status) VALUES (?, ?, ?, ?)",
                   (patient_id, title, reminder_datetime.strftime("%Y-%m-%d %H:%M:%S"), 'Pending'))
    conn.commit()
    print("Reminder added successfully!")
    conn.close()

def view_reminders():
    conn = sqlite3.connect("health_system.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT r.id, p.name, r.title, r.reminder_time, r.status
    FROM reminders r
    JOIN patients p ON r.patient_id = p.id
    ORDER BY r.reminder_time ASC
    """)
    reminders = cursor.fetchall()
    
    print("\n--- Upcoming Reminders ---")
    for reminder in reminders:
        print(f"ID: {reminder[0]}, Patient: {reminder[1]}, Title: {reminder[2]}, Time: {reminder[3]}, Status: {reminder[4]}")
    conn.close()

def trigger_notifications():
    conn = sqlite3.connect("health_system.db")
    cursor = conn.cursor()

    current_time = datetime.now()
    next_hour = current_time + timedelta(hours=1)

    cursor.execute("""
    SELECT r.id, p.name, r.title, r.reminder_time
    FROM reminders r
    JOIN patients p ON r.patient_id = p.id
    WHERE datetime(r.reminder_time) BETWEEN ? AND ?
    AND r.status = 'Pending'
    """, (current_time.strftime("%Y-%m-%d %H:%M:%S"), next_hour.strftime("%Y-%m-%d %H:%M:%S")))

    upcoming_reminders = cursor.fetchall()

    if upcoming_reminders:
        print("\n--- Notifications ---")
        for reminder in upcoming_reminders:
            print(f"Reminder ID: {reminder[0]}, Patient: {reminder[1]}, Title: {reminder[2]}, Time: {reminder[3]}")
            # Update status to "Notified"
            cursor.execute("UPDATE reminders SET status = 'Notified' WHERE id = ?", (reminder[0],))
        conn.commit()
    else:
        print("No upcoming reminders in the next hour.")
    conn.close()

# Main Menu
def main_menu():
    while True:
        print("\n--- Health Administration System ---")
        print("1. Register User")
        print("2. Login")
        print("3. Add Doctor")
        print("4. View Doctors")
        print("5. Add Invoice")
        print("6. View Invoices")

def main_menu():
    while True:
        print("\n--- Health Administration System ---")
        print("1. Register User")
        print("2. Login")
        print("3. Add Doctor")
        print("4. View Doctors")
        print("5. Add Invoice")
        print("6. View Invoices")
        print("7. Add Prescription")
        print("8. View Prescriptions")
        print("9. Search Patients")
        print("10. Add Reminder")
        print("11. View Reminders")
        print("12. Check Notifications")
        print("13. Exit")
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            register_user()
        elif choice == 2:
            login_user()
        elif choice == 3:
            add_doctor()
        elif choice == 4:
            view_doctors()
        elif choice == 5:
            add_invoice()
        elif choice == 6:
            view_invoices()
        elif choice == 7:
            add_prescription()
        elif choice == 8:
            view_prescriptions()
        elif choice == 9:
            search_patients()
        elif choice == 10:
            add_reminder()
        elif choice == 11:
            view_reminders()
        elif choice == 12:
            trigger_notifications()
        elif choice == 13:
            print("Exiting... Goodbye!")
            break
        elif choice == 14:
            add_patient()
        elif choice == 15:
            view_patients()
        elif choice == 16:
            schedule_appointment()
        elif choice == 17:
            view_appointments()
        elif choice == 18:
            search_doctors_by_specialty()
        elif choice == 19:
            search_invoices_by_status()
        elif choice == 20:
            generate_summary_report()
        elif choice == 21:
            mark_reminder_as_complete()
        else:
            print("Invalid choice!")

# Initialize and run the application
if __name__ == "__main__":
    init_databases()
    main_menu()
