const chatForm = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");

// Fonction pour afficher un message
function appendMessage(text, sender) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", sender);
  messageDiv.textContent = text;
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Envoi du message à Rasa
async function sendMessage(message) {
  appendMessage(message, "user");

  try {
    const response = await fetch("http://localhost:5005/webhooks/rest/webhook", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        sender: "user",  // peut être un ID unique si multi-utilisateurs
        message: message
      })
    });

    const data = await response.json();

    if (data.length === 0) {
      appendMessage("🤖 (aucune réponse de Rasa)", "bot");
    } else {
      data.forEach((msg) => {
        if (msg.text) {
          appendMessage(msg.text, "bot");
        }
        // Tu peux aussi gérer les images, boutons, etc. ici
      });
    }

  } catch (err) {
    appendMessage("❌ Erreur lors de la connexion à Rasa.", "bot");
    console.error(err);
  }
}

// Événement d’envoi de formulaire
chatForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const message = userInput.value.trim();
  if (message) {
    sendMessage(message);
    userInput.value = "";
  }
});
