async function sendChat(message) {
    const messages = document.getElementById("chatMessages");
    if (!messages) return;
    const user = document.createElement("div");
    user.className = "message user";
    user.textContent = message;
    messages.appendChild(user);

    const bot = document.createElement("div");
    bot.className = "message bot";
    bot.textContent = "Thinking...";
    messages.appendChild(bot);
    messages.scrollTop = messages.scrollHeight;

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message})
        });
        const data = await response.json();
        bot.textContent = data.answer;
    } catch {
        bot.textContent = "Something went wrong. Please try again or contact HR.";
    }
    messages.scrollTop = messages.scrollHeight;
}

function askSuggestion(text) {
    const input = document.getElementById("chatInput");
    if (input) input.value = text;
    sendChat(text);
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("chatForm");
    if (form) {
        form.addEventListener("submit", e => {
            e.preventDefault();
            const input = document.getElementById("chatInput");
            const message = input.value.trim();
            if (!message) return;
            input.value = "";
            sendChat(message);
        });
    }

    const checks = document.querySelectorAll(".check-item input");
    const updateProgress = () => {
        const total = checks.length;
        const done = [...checks].filter(c => c.checked).length;
        const percent = total ? Math.round(done / total * 100) : 0;
        const bar = document.getElementById("progressBar");
        const text = document.getElementById("progressText");
        if (bar) bar.style.width = percent + "%";
        if (text) text.textContent = percent + "%";
        checks.forEach(c => c.closest(".check-item").classList.toggle("done", c.checked));
    };

    checks.forEach(check => {
        check.addEventListener("change", async () => {
            await fetch(`/api/onboarding/${check.dataset.id}/toggle`, {
                method:"POST",
                headers:{"Content-Type":"application/json"},
                body:JSON.stringify({completed:check.checked})
            });
            updateProgress();
        });
    });
    updateProgress();

    const faqForm = document.getElementById("faqForm");
    if (faqForm) {
        faqForm.addEventListener("submit", async e => {
            e.preventDefault();
            const payload = {
                question: document.getElementById("faqQuestion").value,
                category: document.getElementById("faqCategory").value,
                answer: document.getElementById("faqAnswer").value
            };
            const res = await fetch("/api/admin/faqs", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload)});
            if (res.ok) location.reload(); else alert("Could not add FAQ.");
        });
    }

    const checkForm = document.getElementById("checkForm");
    if (checkForm) {
        checkForm.addEventListener("submit", async e => {
            e.preventDefault();
            const payload = {
                title: document.getElementById("checkTitle").value,
                description: document.getElementById("checkDescription").value
            };
            const res = await fetch("/api/admin/checklist", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload)});
            if (res.ok) location.reload(); else alert("Could not add step.");
        });
    }
});

async function deleteFaq(id) {
    if (!confirm("Delete this FAQ?")) return;
    const res = await fetch(`/api/admin/faqs/${id}`, {method:"DELETE"});
    if (res.ok) document.getElementById(`faq-${id}`).remove();
}

async function deleteChecklist(id) {
    if (!confirm("Delete this onboarding step?")) return;
    const res = await fetch(`/api/admin/checklist/${id}`, {method:"DELETE"});
    if (res.ok) document.getElementById(`check-${id}`).remove();
}
