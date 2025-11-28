from django.test import TestCase
from tasks.scoring import analyze_tasks

class TestScoring(TestCase):
    def test_past_due_boosts_priority(self):
        tasks = [
            {"id":"a","title":"old","due_date":"2020-01-01","estimated_hours":2,"importance":5,"dependencies":[]},
            {"id":"b","title":"far","due_date":"2030-01-01","estimated_hours":2,"importance":5,"dependencies":[]}
        ]
        res = analyze_tasks(tasks)
        scores = {t['id']: t['score'] for t in res['scored_tasks']}
        self.assertTrue(scores['a'] > scores['b'])

    def test_fastest_wins_preset_prioritizes_low_effort(self):
        tasks = [
            {"id":"a","title":"long","due_date":"2025-12-31","estimated_hours":8,"importance":5,"dependencies":[]},
            {"id":"b","title":"short","due_date":"2025-12-31","estimated_hours":1,"importance":5,"dependencies":[]}
        ]
        weights = {"urgency":0.2,"importance":0.2,"effort":0.5,"dependency":0.1}
        res = analyze_tasks(tasks, weights=weights)
        scores = {t['id']: t['score'] for t in res['scored_tasks']}
        self.assertTrue(scores['b'] > scores['a'])

    def test_detects_circular_dependency(self):
        tasks = [
            {"id":"a","title":"A","due_date":"2025-12-01","estimated_hours":2,"importance":5,"dependencies":["b"]},
            {"id":"b","title":"B","due_date":"2025-12-01","estimated_hours":2,"importance":5,"dependencies":["a"]}
        ]
        res = analyze_tasks(tasks)
        self.assertTrue(
            any(
                isinstance(i, dict) and 'circular_dependencies' in i
                for i in res['issues']
            )
        )
