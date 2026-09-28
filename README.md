# HR Onboarding Chatbot

An AI/NLP-based HR onboarding assistant built with Python, Flask, SQLite and TF-IDF/cosine similarity.

## Features

- HR FAQ chatbot
- TF-IDF + cosine similarity question matching
- Company policy knowledge base
- Onboarding checklist with progress tracking
- HR admin login
- Add/delete FAQs
- Add/delete onboarding steps
- Responsive UI
- Automated tests
- No paid API required

## Technology

- Python
- Flask
- SQLite
- Scikit-learn
- HTML/CSS/JavaScript
- TF-IDF and cosine similarity

## Project structure

```text
hr-onboarding-chatbot/
├── app.py
├── chatbot.py
├── database.py
├── seed.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
├── templates/
├── static/
└── tests/
```

## Installation on Windows

Open the project folder in VS Code terminal.

### 1. Create virtual environment

```powershell
python -m venv venv
```

### 2. Activate it

```powershell
venv\Scripts\activate
```

### 3. Install packages

```powershell
pip install -r requirements.txt
```

### 4. Create database and sample data

```powershell
python seed.py
```

### 5. Run the application

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Admin login

URL:

```text
http://127.0.0.1:5000/admin/login
```

Demo credentials:

```text
Username: admin
Password: admin123
```

Change these credentials before using the project outside a classroom/demo environment.

## How the chatbot works

1. HR FAQs are stored in SQLite.
2. The chatbot converts FAQ questions into TF-IDF vectors.
3. The employee's question is also converted into a vector.
4. Cosine similarity compares the employee question with stored questions.
5. The highest matching FAQ is selected.
6. If the similarity is below the threshold, the chatbot asks the employee to contact HR.

## Run tests

```powershell
pytest
```

## Future improvements

- Employee authentication
- Role-based admin access
- PDF/document knowledge base
- Multilingual chatbot
- LLM/RAG integration
- Email notifications
- Employee-specific onboarding
- Analytics dashboard
