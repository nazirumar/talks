const roomName = JSON.parse(document.getElementById("room-name").textContent);
const requestUser = JSON.parse(document.getElementById("request-user").textContent);
const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/room/${roomName}/`);
console.log(requestUser);

chatSocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const chatBox = document.getElementById("chat-box");
    const dateOptions = { hour: "numeric", minute: "numeric", hour12: true };
    const datetime = new Date(data.datetime).toLocaleString("en", dateOptions);
    const isMe = data.user === requestUser;
    const messageHtml = `
        <div class="message ${isMe ? 'me' : 'other'}">
            <strong>${isMe ? 'Me' : data.user}</strong>
            <span class="date">${datetime}</span><br>
            ${data.message}
        </div>
    `;
    chatBox.innerHTML += messageHtml;
    chatBox.scrollTop = chatBox.scrollHeight;
};

chatSocket.onclose = function(event) {
    console.error("Chat socket closed unexpectedly");
};

document.getElementById("chat-message-submit").onclick = function() {
    const inputField = document.getElementById("chat-message-input");
    const message = inputField.value;
    if (message) {
        chatSocket.send(JSON.stringify({ message: message }));
        inputField.value = '';
        inputField.focus();
    }
};

document.getElementById("chat-message-input").onkeypress = function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("chat-message-submit").click();
    }
};