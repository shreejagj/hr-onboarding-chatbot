from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from database import init_db, get_faqs, add_faq, update_faq, delete_faq, get_checklist, add_checklist_item, update_checklist_item, delete_checklist_item
from chatbot import HRChatbot

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
init_db()

bot = HRChatbot()

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return fn(*args, **kwargs)
    return wrapper

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat")
def chat():
    return render_template("chatbot.html")

@app.post("/api/chat")
def api_chat():
    data = request.get_json(silent=True) or {}
    question = (data.get("message") or "").strip()
    if not question:
        return jsonify({"answer": "Please enter a question.", "confidence": 0})
    result = bot.answer(question)
    return jsonify(result)

@app.route("/onboarding")
def onboarding():
    return render_template("onboarding.html", items=get_checklist())

@app.post("/api/onboarding/<int:item_id>/toggle")
def toggle_onboarding(item_id):
    data = request.get_json(silent=True) or {}
    from database import toggle_checklist
    item = toggle_checklist(item_id, bool(data.get("completed")))
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect(url_for("admin"))
        error = "Invalid username or password."
    return render_template("admin_login.html", error=error)

@app.get("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/admin")
@admin_required
def admin():
    return render_template("admin.html", faqs=get_faqs(), checklist=get_checklist())

@app.get("/api/admin/faqs")
@admin_required
def api_faqs():
    return jsonify(get_faqs())

@app.post("/api/admin/faqs")
@admin_required
def api_add_faq():
    data = request.get_json(silent=True) or {}
    if not data.get("question") or not data.get("answer"):
        return jsonify({"error": "Question and answer are required"}), 400
    faq = add_faq(data["question"], data["answer"], data.get("category", "General"))
    bot.reload()
    return jsonify(faq), 201

@app.put("/api/admin/faqs/<int:faq_id>")
@admin_required
def api_update_faq(faq_id):
    data = request.get_json(silent=True) or {}
    faq = update_faq(faq_id, data.get("question"), data.get("answer"), data.get("category", "General"))
    if not faq:
        return jsonify({"error": "FAQ not found"}), 404
    bot.reload()
    return jsonify(faq)

@app.delete("/api/admin/faqs/<int:faq_id>")
@admin_required
def api_delete_faq(faq_id):
    if not delete_faq(faq_id):
        return jsonify({"error": "FAQ not found"}), 404
    bot.reload()
    return jsonify({"message": "FAQ deleted"})

@app.post("/api/admin/checklist")
@admin_required
def api_add_checklist():
    data = request.get_json(silent=True) or {}
    if not data.get("title"):
        return jsonify({"error": "Title is required"}), 400
    return jsonify(add_checklist_item(data["title"], data.get("description", ""))), 201

@app.put("/api/admin/checklist/<int:item_id>")
@admin_required
def api_update_checklist(item_id):
    data = request.get_json(silent=True) or {}
    item = update_checklist_item(item_id, data.get("title"), data.get("description", ""))
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)

@app.delete("/api/admin/checklist/<int:item_id>")
@admin_required
def api_delete_checklist(item_id):
    if not delete_checklist_item(item_id):
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"message": "Checklist item deleted"})

if __name__ == "__main__":
    app.run(debug=True)
