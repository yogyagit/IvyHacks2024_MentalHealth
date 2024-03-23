// script.js
function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    if (!userInput) return;

    const messageContainer = document.getElementById('chatContainer');
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'userMessage');
    userMessage.textContent = userInput;
    messageContainer.appendChild(userMessage);

    // Clear input field
    document.getElementById('userInput').value = '';

    // Scroll to bottom
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

