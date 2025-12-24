(function () {
    if (window.IRA_WIDGET_LOADED) return;
    window.IRA_WIDGET_LOADED = true;
  
    const API_URL = "https://web-production-35558.up.railway.app/chat";
  
    /* ========== CSS ========== */
    const style = document.createElement("style");
    style.innerHTML = `
      /* (PASTE YOUR ENTIRE <style> CONTENT HERE EXACTLY AS IS) */
    `;
    document.head.appendChild(style);
  
    /* ========== HTML ========== */
    const container = document.createElement("div");
    container.innerHTML = `
      <!-- Chat Toggle Button -->
      <button class="chat-toggle" id="chatToggle">
        <i class="fas fa-comment-dots"></i>
      </button>
  
      <!-- Chat Widget -->
      <div class="chat-widget" id="chatWidget">
        <div class="chat-header">
          <div class="chat-header-left">
            <div class="chat-avatar">IRA</div>
            <div>
              <div class="chat-title">IRA Sportswear</div>
              <div class="chat-subtitle">We're here to help</div>
            </div>
          </div>
          <button class="chat-close" id="chatClose">&times;</button>
        </div>
  
        <div class="chat-messages" id="chatMessages"></div>
  
        <div class="typing-indicator" id="typingIndicator" style="display:none">
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
        </div>
  
        <div class="chat-input-container">
          <div class="chat-input-wrapper">
            <textarea id="chatInput" class="chat-input" placeholder="Type your message"></textarea>
            <button id="sendButton" class="send-button">➤</button>
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(container);
  
    /* ========== JS LOGIC ========== */
    const toggle = document.getElementById("chatToggle");
    const widget = document.getElementById("chatWidget");
    const close = document.getElementById("chatClose");
    const input = document.getElementById("chatInput");
    const send = document.getElementById("sendButton");
    const messages = document.getElementById("chatMessages");
    const typing = document.getElementById("typingIndicator");
  
    function addMessage(type, text) {
      const div = document.createElement("div");
      div.className = `message ${type}`;
      div.innerHTML = `<div class="message-content">${text}</div>`;
      messages.appendChild(div);
      messages.scrollTop = messages.scrollHeight;
    }
  
    async function sendMessage() {
      const text = input.value.trim();
      if (!text) return;
  
      addMessage("user", text);
      input.value = "";
      typing.style.display = "flex";
  
      try {
        const res = await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text })
        });
  
        const data = await res.json();
        typing.style.display = "none";
        addMessage("bot", data.reply || "No response");
      } catch (e) {
        typing.style.display = "none";
        addMessage("bot", "Service temporarily unavailable.");
      }
    }
  
    toggle.onclick = () => widget.classList.toggle("visible");
    close.onclick = () => widget.classList.remove("visible");
    send.onclick = sendMessage;
  })();
  