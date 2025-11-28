from datetime import datetime, date
from dateutil import parser
from collections import defaultdict

DEFAULT_WEIGHTS = {
    "urgency": 0.4,
    "importance": 0.3,
    "effort": 0.2,
    "dependency": 0.1,
}

def parse_date(d):
    if not d:
        return None
    try:
        return parser.isoparse(d).date()
    except:
        return None

def detect_cycles(tasks):
    graph = defaultdict(list)
    ids = set()

    for t in tasks:
        tid = t.get("id")
        ids.add(tid)
        for dep in t.get("dependencies", []):
            graph[tid].append(dep)

    visited = set()
    stack = set()
    cycles = []

    def dfs(node, path):
        if node in stack:
            cycles.append(path[path.index(node):])
            return
        if node in visited:
            return
        visited.add(node)
        stack.add(node)

        for nei in graph[node]:
            dfs(nei, path + [nei])

        stack.remove(node)

    for tid in ids:
        if tid not in visited:
            dfs(tid, [tid])

    return cycles

def analyze_tasks(tasks, weights=None):
    if weights is None:
        weights = DEFAULT_WEIGHTS

    today = date.today()
    issues = []
    id_map = {}

    for t in tasks:
        tid = t.get("id") or t.get("title")
        if not tid:
            issues.append("Task missing ID and title.")
            continue

        t_copy = dict(t)
        t_copy.setdefault("dependencies", [])
        t_copy.setdefault("estimated_hours", 4)
        t_copy.setdefault("importance", 5)
        t_copy["parsed_due"] = parse_date(t.get("due_date"))
        id_map[tid] = t_copy

    cycles = detect_cycles(list(id_map.values()))
    if cycles:
        issues.append({"circular_dependencies": cycles})

    blocked_count = defaultdict(int)
    for tid, t in id_map.items():
        for dep in t["dependencies"]:
            blocked_count[dep] += 1

    scored = []

    def clamp(v, mn=0, mx=1):
        return max(mn, min(mx, v))

    for tid, t in id_map.items():
        due = t["parsed_due"]
        if due is None:
            urgency = 0.5
        else:
            days_left = (due - today).days
            if days_left < 0:
                urgency = 1 + clamp(abs(days_left) / 7, 0, 1)
            else:
                urgency = clamp((14 - days_left) / 14, 0, 1)

        importance = clamp(t["importance"] / 10, 0, 1)
        effort_norm = clamp(t["estimated_hours"] / 8, 0, 1)
        quick_win = 1 - effort_norm
        dep_score = clamp(blocked_count[tid] / 5, 0, 1)

        raw = (
            weights["urgency"] * urgency +
            weights["importance"] * importance +
            weights["effort"] * quick_win +
            weights["dependency"] * dep_score
        )

        max_raw = (
            weights["urgency"] * 2 +
            weights["importance"] +
            weights["effort"] +
            weights["dependency"]
        )

        score = (raw / max_raw) * 100

        priority = "High" if score >= 70 else "Medium" if score >= 40 else "Low"

        explanation = []
        if due is None:
            explanation.append("No due date")
        else:
            d = (due - today).days
            if d < 0:
                explanation.append(f"Past due by {abs(d)} days")
            else:
                explanation.append(f"Due in {d} days")

        explanation.append(f"Importance {t['importance']}/10")
        explanation.append(f"Effort {t['estimated_hours']}h")

        if blocked_count[tid] > 0:
            explanation.append(f"Blocks {blocked_count[tid]} tasks")

        scored.append({
            "id": tid,
            "title": t.get("title"),
            "score": round(score, 2),
            "priority": priority,
            "explanation": "; ".join(explanation),
            "circular_dependency": any(tid in c for c in cycles),
        })

    scored_sorted = sorted(scored, key=lambda x: x["score"], reverse=True)
    top_3 = scored_sorted[:3]

    return {
        "scored_tasks": scored_sorted,
        "top_3": top_3,
        "issues": issues
    }
