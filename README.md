# Task Analyzer – Priority Scoring System  
A simple Django + Vanilla JS project that analyzes a list of tasks and scores them based on urgency, importance, effort, and dependencies.  
The goal is to help users understand which tasks they should focus on first.

---

## Features
- REST API built in Django + Django REST Framework  
- Smart scoring algorithm using:
  - Urgency based on due date  
  - Importance (0–10)  
  - Estimated effort (hours)  
  - Number of dependencies  
- Automatically detects:
  - Past-due tasks (boosts urgency)  
  - Circular dependencies  
  - Missing or invalid data  
- Multiple scoring strategies (weight presets):
  - Smart Balanced  
  - Fastest Wins  
  - High Impact  
  - Deadline Driven  
- Frontend built using plain HTML, CSS, JavaScript  
- Fully working UI with:
  - Add-task form  
  - Bulk JSON panel  
  - Priority color coding  
  - Top 3 tasks section  
  - Issues panel  
- Includes 3+ unit tests for scoring logic

---

##  Installation & Setup

### 1. Clone the project
```
git clone <your-repository-url>
cd task-analyzer
```

### 2. Create & activate virtual environment
```
python3 -m venv venv
source venv/bin/activate     # Mac/Linux
```

### 3. Install all dependencies
```
pip install -r requirements.txt
```

### 4. Apply migrations
```
cd backend
python manage.py migrate
```

### 5. Start the backend server
```
python manage.py runserver
```
Runs at:
```
http://127.0.0.1:8000/
```

### 6. Start the frontend
Open new terminal:

```
cd frontend
python3 -m http.server 5500
```

Open browser:
```
http://localhost:5500
```

---

## API Documentation

### ▶ `POST /api/tasks/analyze/`
Analyzes a list of tasks and calculates scores.

#### **Request Example**
```json
{
  "tasks": [
    {
      "id": "t1",
      "title": "Fix login bug",
      "due_date": "2025-11-30",
      "estimated_hours": 3,
      "importance": 8,
      "dependencies": ["t2"]
    }
  ],
  "strategy": "smart"
}
```

#### **Response Example**
```json
{
  "scored_tasks": [...],
  "top_3": [...],
  "issues": [...],
  "explanations": {...}
}
```

---

##  How the Scoring Algorithm Works

Each task receives a score based on the following factors:

### 1️ Urgency  
- Tasks closer to deadline → higher urgency  
- Overdue tasks → major urgency boost  

### 2️ Importance  
- Higher importance → higher priority  

### 3️ Effort  
- Low effort tasks get slight score boost (quick wins)  

### 4️ Dependencies  
- Tasks that are blocking others → higher priority  

---

### Simplified Formula  
```
score = 
(urgency * Wu) + 
(importance * Wi) + 
(effort_factor * We) + 
(dependency_factor * Wd)
```

###  Weight Presets
Strategy | Meaning
-------- | --------
Smart | Balanced scoring
Fastest | Low-effort tasks boosted
High Impact | Importance-focused
Deadline Driven | Urgency-focused

---

##  Issues Handling  
API returns a list of issues such as:
- Circular dependencies  
- Missing or invalid fields  
- malformed dates  
- empty titles or IDs  

These help the user fix task input problems.

---

##  Running Unit Tests

The project includes tests for:
- Past-due urgency effect  
- Fastest strategy weight logic  
- Circular dependency detection  

Run tests:
```
python manage.py test
```

Expected output:
```
Ran 3 tests ... OK
```

---

##  Project Structure
```
task-analyzer/
│
├── backend/
│   ├── task_analyzer/        # Django settings
│   ├── tasks/                # Scoring + API logic
│   │   ├── scoring.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   │        └── test_scoring.py
│   └── manage.py
│
└── frontend/
    ├── index.html
    ├── script.js
    └── styles.css
```

---

##  What This Project Demonstrates
- Backend API development  
- Algorithm design & implementation  
- Frontend–backend communication  
- Writing unit tests  
- Handling dependencies and task relationships  
- Clean, organized code structure  

---

##  Notes
- Built using Python 3.12  
- Django 4+ and Django REST Framework  
- No external JS framework used  
- Fully satisfies project instructions  

---

##  Conclusion
Task Analyzer is a clean and extendable system for prioritizing tasks.  
You can easily expand it with graphs, timelines, or machine learning in the future.

