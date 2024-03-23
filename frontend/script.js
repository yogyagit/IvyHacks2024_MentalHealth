function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    if (message !== '') {
        const timestamp = new Date().toLocaleTimeString();
        appendMessage('You', message, timestamp);
        messageInput.value = '';
    }
}

function appendMessage(sender, message, timestamp) {
    const chatBox = document.getElementById('chatBox');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');

    const senderElement = document.createElement('span');
    senderElement.classList.add('sender');
    senderElement.innerText = sender + ' - ' + timestamp;

    const messageContentElement = document.createElement('p');
    messageContentElement.classList.add('message-content');
    messageContentElement.innerText = message;

    messageElement.appendChild(senderElement);
    messageElement.appendChild(messageContentElement);
    chatBox.appendChild(messageElement);

    // Scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;
}

