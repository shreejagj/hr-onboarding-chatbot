import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "hr_onboarding.db")

def connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = connect()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS faqs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        category TEXT NOT NULL DEFAULT 'General'
    );

    CREATE TABLE IF NOT EXISTS checklist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT DEFAULT '',
        completed INTEGER NOT NULL DEFAULT 0
    );
    """)
    conn.commit()
    conn.close()

def seed_db():
    conn = connect()
    if conn.execute("SELECT COUNT(*) FROM faqs").fetchone()[0] == 0:
        faqs = [
            ("What documents are required for onboarding?", "Please submit your government ID, educational certificates, address proof, bank details and passport-size photograph to HR.", "Documents"),
            ("What are the working hours?", "The standard working hours are 9:00 AM to 6:00 PM, Monday to Friday. Check your department schedule for exceptions.", "Attendance"),
            ("How do I apply for leave?", "Submit a leave request through the employee portal and wait for manager approval. Contact HR if you need help.", "Leave"),
            ("What is the probation period?", "The standard probation period is six months unless your offer letter states otherwise.", "Policy"),
            ("What is the work from home policy?", "Work-from-home availability depends on your role and manager approval. Check the latest company policy or contact HR.", "Policy"),
            ("What is the dress code?", "Employees should follow professional and role-appropriate attire guidelines. Ask your manager if you are unsure.", "Policy"),
            ("What training is required?", "New employees should complete orientation, information-security training, workplace conduct training and any role-specific training assigned by their department.", "Training"),
            ("How do I contact HR?", "Contact the HR team through the official HR email or employee portal. Your joining documents contain the current contact details.", "HR Support"),
            ("What are the onboarding steps?", "The usual process is document submission, verification, HR registration, ID creation, orientation, department introduction, training and team onboarding.", "Onboarding"),
            ("What employee benefits are available?", "Benefits depend on your employment terms and company policy. HR can provide the current benefits information applicable to you.", "Benefits")
        ]
        conn.executemany("INSERT INTO faqs(question, answer, category) VALUES (?, ?, ?)", faqs)

    if conn.execute("SELECT COUNT(*) FROM checklist").fetchone()[0] == 0:
        items = [
            ("Submit required documents", "Upload or submit all required joining documents to HR."),
            ("Complete document verification", "Wait for HR to verify your submitted documents."),
            ("Complete HR registration", "Finish employee registration and personal details."),
            ("Get employee ID", "Receive your employee ID/card or digital employee identity."),
            ("Attend company orientation", "Attend the new employee orientation session."),
            ("Meet your department", "Meet your manager and department/team members."),
            ("Complete required training", "Finish security, conduct and role-specific training."),
            ("Complete onboarding", "Confirm that all onboarding activities are completed.")
        ]
        conn.executemany("INSERT INTO checklist(title, description) VALUES (?, ?)", items)
    conn.commit()
    conn.close()

def rows(sql, params=()):
    conn = connect()
    result = [dict(r) for r in conn.execute(sql, params).fetchall()]
    conn.close()
    return result

def get_faqs():
    return rows("SELECT * FROM faqs ORDER BY id")

def add_faq(question, answer, category="General"):
    conn = connect()
    cur = conn.execute("INSERT INTO faqs(question, answer, category) VALUES (?, ?, ?)", (question, answer, category))
    conn.commit()
    item = dict(conn.execute("SELECT * FROM faqs WHERE id=?", (cur.lastrowid,)).fetchone())
    conn.close()
    return item

def update_faq(faq_id, question, answer, category="General"):
    conn = connect()
    conn.execute("UPDATE faqs SET question=?, answer=?, category=? WHERE id=?", (question, answer, category, faq_id))
    conn.commit()
    row = conn.execute("SELECT * FROM faqs WHERE id=?", (faq_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def delete_faq(faq_id):
    conn = connect()
    cur = conn.execute("DELETE FROM faqs WHERE id=?", (faq_id,))
    conn.commit()
    conn.close()
    return cur.rowcount > 0

def get_checklist():
    return rows("SELECT * FROM checklist ORDER BY id")

def add_checklist_item(title, description=""):
    conn = connect()
    cur = conn.execute("INSERT INTO checklist(title, description) VALUES (?, ?)", (title, description))
    conn.commit()
    row = dict(conn.execute("SELECT * FROM checklist WHERE id=?", (cur.lastrowid,)).fetchone())
    conn.close()
    return row

def update_checklist_item(item_id, title, description=""):
    conn = connect()
    conn.execute("UPDATE checklist SET title=?, description=? WHERE id=?", (title, description, item_id))
    conn.commit()
    row = conn.execute("SELECT * FROM checklist WHERE id=?", (item_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def delete_checklist_item(item_id):
    conn = connect()
    cur = conn.execute("DELETE FROM checklist WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    return cur.rowcount > 0

def toggle_checklist(item_id, completed):
    conn = connect()
    conn.execute("UPDATE checklist SET completed=? WHERE id=?", (1 if completed else 0, item_id))
    conn.commit()
    row = conn.execute("SELECT * FROM checklist WHERE id=?", (item_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

if __name__ == "__main__":
    init_db()
    seed_db()
    print("Database initialized and seeded.")
