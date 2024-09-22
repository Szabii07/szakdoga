document.addEventListener('DOMContentLoaded', function() {
    const messageForm = document.querySelector('form');
    const messageList = document.querySelector('.message-list');
    const recipientField = messageForm.querySelector('[name="recipient"]');

    // Scroll to the bottom of the message list
    function scrollToBottom() {
        messageList.scrollTop = messageList.scrollHeight;
    }

    // Fetch and display messages
    function fetchMessages() {
        const recipientId = recipientField.value;
        if (!recipientId) return;

        fetch(`/messages/${recipientId}/`)  // Corrected URL format
            .then(response => response.json())
            .then(data => {
                messageList.innerHTML = '';  // Clear message list
                data.messages.forEach(msg => {
                    const messageElement = document.createElement('div');
                    messageElement.classList.add('message', msg.sender === data.currentUser ? 'sent' : 'received');
                    messageElement.innerHTML = `<strong>${msg.sender}:</strong> ${msg.content} <em>(${msg.created_at})</em>`;
                    messageList.appendChild(messageElement);
                });

                // Scroll to the bottom after loading messages
                scrollToBottom();
            });
    }

    // Handle form submission
    messageForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(messageForm);

        fetch(messageForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
            }
        })
        .then(response => response.json())
        .then(() => {
            fetchMessages();  // Refresh messages after sending
        });
    });

    // Automatically refresh messages every 5 seconds
    setInterval(fetchMessages, 5000);

    // Scroll to the latest message on page load
    scrollToBottom();
});
