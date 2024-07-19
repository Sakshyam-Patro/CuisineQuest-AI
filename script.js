const chatWidget = document.getElementById('chat-widget-button');
const chatContainer = document.getElementById('chat-container');
const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const closeChat = document.getElementById('close-chat');

function toggleChat() {
    chatContainer.classList.toggle('hidden');
}

chatWidget.addEventListener('click', toggleChat);
closeChat.addEventListener('click', toggleChat);

function addMessage(message, isUser) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.classList.add(isUser ? 'user-message' : 'bot-message');
    messageElement.textContent = message;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
const clearButton = document.getElementById('clear-button');

// Add this function to clear the chat messages
function clearChat() {
    chatMessages.innerHTML = '';
}

// Add this event listener for the clear button
clearButton.addEventListener('click', clearChat);

async function sendMessage() {
    const message = messageInput.value.trim();
    if (message.toLowerCase() === 'clear') {
        clearChat();
        messageInput.value = '';
    } else {
        addMessage(message, true);
        messageInput.value = '';

        const loadingIndicator = showLoadingIndicator();

        try {
            const response = await fetch('http://localhost:5005/webhooks/rest/webhook', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    sender: 'user',
                    message: message
                }),
            });

            const data = await response.json();
            
            // Remove loading indicator
            loadingIndicator.remove();

            // Add a delay before showing each message
            for (const reply of data) {
                if (reply.text) {
                    await new Promise(resolve => setTimeout(resolve, 400)); // 1 second delay
                    addMessage(reply.text, false);
                }
            }
        } catch (error) {
            console.error('Error:', error);
            loadingIndicator.remove();
            addMessage('Sorry, there was an error processing your request.', false);
        }
    }
}

messageInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

sendButton.addEventListener('click', sendMessage);

function showLoadingIndicator() {
    const loadingElement = document.createElement('div');
    loadingElement.classList.add('message', 'bot-message', 'loading');
    loadingElement.textContent = '...';
    chatMessages.appendChild(loadingElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return loadingElement;
}