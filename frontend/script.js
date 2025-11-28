const tasksLocal = [];
const resultsDiv = document.getElementById("results");

function strategyWeights(name) {
  return {
    smart:  { urgency:0.4, importance:0.3, effort:0.2, dependency:0.1 },
    fast:   { urgency:0.2, importance:0.2, effort:0.5, dependency:0.1 },
    impact: { urgency:0.2, importance:0.6, effort:0.1, dependency:0.1 },
    deadline:{ urgency:0.7, importance:0.2, effort:0.05, dependency:0.05 },
  }[name];
}

document.getElementById("addTask").addEventListener("click", () => {
  const title = document.getElementById("title").value.trim();
  if (!title) return alert("Title is required");

  const task = {
    id: "t" + (tasksLocal.length + 1),
    title,
    due_date: document.getElementById("due").value || null,
    estimated_hours: parseFloat(document.getElementById("hours").value) || null,
    importance: parseInt(document.getElementById("importance").value) || null,
    dependencies: document.getElementById("deps").value
      ? document.getElementById("deps").value.split(",").map(s => s.trim())
      : []
  };

  tasksLocal.push(task);
  alert(`Task added with ID: ${task.id}`);
});

document.getElementById("analyze").addEventListener("click", async () => {
  let tasks = [...tasksLocal];

  const bulk = document.getElementById("bulk").value.trim();
  if (bulk) {
    try {
      const arr = JSON.parse(bulk);
      if (Array.isArray(arr)) tasks = tasks.concat(arr);
      else return alert("Bulk JSON should be an array");
    } catch (err) {
      return alert("Invalid bulk JSON");
    }
  }

  if (tasks.length === 0) return alert("No tasks to analyze!");

  resultsDiv.innerHTML = "<p>Analyzing...</p>";

  const strat = document.getElementById("strategy").value;
  const weights = strategyWeights(strat);

  try {
    const res = await fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tasks, weights })
    });

    const data = await res.json();
    render(data);
  } catch (err) {
    resultsDiv.innerHTML = "<p>Error: " + err.message + "</p>";
  }
});

function render(data) {
  let html = "<h3>Top 3</h3>";

  data.top_3.forEach(t => {
    html += `
      <div class="task high">
        <b>${t.title}</b> — Score: ${t.score}
        <div class="small">${t.reason}</div>
      </div>`;
  });

  html += "<h3>All Tasks</h3>";

  data.scored_tasks.forEach(t => {
    const cls = t.priority.toLowerCase();
    html += `
      <div class="task ${cls}">
        <b>${t.title}</b> — Score: ${t.score}
        <div class="small">${t.explanation}</div>
      </div>`;
  });

  if (data.issues.length) {
    html += `<pre>${JSON.stringify(data.issues, null, 2)}</pre>`;
  }

  resultsDiv.innerHTML = html;
}
