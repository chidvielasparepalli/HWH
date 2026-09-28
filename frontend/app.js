const $ = (id) => document.getElementById(id);

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || "Request failed");
  return data;
}

function setConnection(text, state = "") {
  const el = $("connection");
  el.className = "connection " + state;
  el.innerHTML = "<i></i> " + text;
}

async function checkHealth() {
  try {
    const data = await api("/api/health");
    setConnection(data.status === "connected" ? "Hindsight connected" : "Hindsight unavailable", data.status === "connected" ? "ok" : "bad");
  } catch {
    setConnection("Backend offline", "bad");
  }
}

$("exampleBtn").onclick = () => {
  $("service").value = "payment-service";
  $("incident").value = "Payment requests are timing out during a traffic spike. Database connection pool is at 100%, p95 latency is 8.9 seconds, and errors started after traffic doubled.";
};

$("seedBtn").onclick = async () => {
  const button = $("seedBtn");
  button.disabled = true;
  button.textContent = "Seeding Hindsight…";
  try {
    const data = await api("/api/demo-seed", { method: "POST" });
    button.textContent = data.stored + " failures loaded";
  } catch (error) {
    alert(error.message);
    button.textContent = "Seed failed";
  } finally {
    setTimeout(() => {
      button.disabled = false;
      button.textContent = "Load 12 historical failures";
    }, 2500);
  }
};

$("analyzeBtn").onclick = async () => {
  const button = $("analyzeBtn");
  button.disabled = true;
  button.textContent = "AEGIS is recalling + reflecting…";

  try {
    const data = await api("/api/analyze", {
      method: "POST",
      body: JSON.stringify({ service: $("service").value, incident: $("incident").value }),
    });

    const a = data.analysis;
    $("resultSection").classList.remove("hidden");
    $("patternTitle").textContent = a.pattern_detected || "Pattern detected";
    $("confidence").textContent = a.confidence || "UNKNOWN";
    $("rootCause").textContent = a.root_cause || "—";
    $("risk").textContent = a.risk || "—";
    $("fix").textContent = a.recommended_fix || "—";
    $("regression").textContent = a.regression_test || "—";
    $("evidenceCount").textContent = data.evidence_count;

    const evidence = $("evidence");
    evidence.innerHTML = "";

    (data.evidence || []).slice(0, 6).forEach((item, index) => {
      const card = document.createElement("div");
      card.className = "evidence-item";

      const meta = document.createElement("div");
      meta.className = "meta";
      meta.textContent = "MEMORY " + String(index + 1).padStart(2, "0") + " • " + (item.type || "experience");

      const text = document.createElement("p");
      text.textContent = item.text;

      card.appendChild(meta);
      card.appendChild(text);
      evidence.appendChild(card);
    });

    $("lesson").textContent = "Hindsight reflection: " + (a.memory_lesson || data.reflection_text || "No lesson returned.");

    $("learnCause").value = a.root_cause || "";
    $("learnFix").value = a.recommended_fix || "";
    $("learnTest").value = a.regression_test || "";
    $("learnOutcome").value = "";

    window.scrollTo({ top: $("resultSection").offsetTop - 20, behavior: "smooth" });
  } catch (error) {
    alert(error.message);
  } finally {
    button.disabled = false;
    button.innerHTML = "Run AEGIS diagnosis <span>↗</span>";
  }
};

$("learnBtn").onclick = async () => {
  try {
    const data = await api("/api/learn", {
      method: "POST",
      body: JSON.stringify({
        service: $("service").value,
        incident: $("incident").value,
        root_cause: $("learnCause").value,
        fix: $("learnFix").value,
        outcome: $("learnOutcome").value,
        regression_test: $("learnTest").value,
      }),
    });
    $("learnStatus").textContent = data.message + " Re-run the incident to test the new memory.";
  } catch (error) {
    alert(error.message);
  }
};

$("profileBtn").onclick = async () => {
  try {
    const data = await api("/api/memory-profile");
    $("profileSection").classList.remove("hidden");
    $("profileText").textContent = data.summary;
    window.scrollTo({ top: $("profileSection").offsetTop - 20, behavior: "smooth" });
  } catch (error) {
    alert(error.message);
  }
};

checkHealth();
