async function sendMessage() {
    const input = document.getElementById("user-input");
    const chatBody = document.getElementById("chat-body");

    const text = input.value.trim();
    if (!text) return;

    // User bubble
    const userBubble = document.createElement("div");
    userBubble.classList.add("message", "user-msg");
    userBubble.textContent = text;
    chatBody.appendChild(userBubble);

    input.value = "";
    chatBody.scrollTop = chatBody.scrollHeight;

    // Backend call
    const response = await fetch("/transform", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sentence: text })
    });

    const data = await response.json();
    const botText = data.transformed;

    // Bot bubble wrapper
    const botWrapper = document.createElement("div");
    botWrapper.style.display = "flex";
    botWrapper.style.alignItems = "center";
    botWrapper.style.gap = "5px";

    // Bot bubble
    const botBubble = document.createElement("div");
    botBubble.classList.add("message", "bot-msg");
    botBubble.textContent = botText;

    // Copy button
    const copyBtn = document.createElement("button");
    copyBtn.classList.add("copy-btn");
    copyBtn.textContent = "📋";

    copyBtn.onclick = () => {
        navigator.clipboard.writeText(botText);
        copyBtn.textContent = "✔";
        setTimeout(() => copyBtn.textContent = "📋", 1200);
    };

    botWrapper.appendChild(botBubble);
    botWrapper.appendChild(copyBtn);

    chatBody.appendChild(botWrapper);
    chatBody.scrollTop = chatBody.scrollHeight;
}

function goBack() {
    window.location.href = "/";  // Goes back to home page
}


// ✔ Enter should send the message
document.getElementById("user-input").addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});

