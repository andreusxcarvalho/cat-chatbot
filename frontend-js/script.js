document.addEventListener("DOMContentLoaded", function () {
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const chatBox = document.getElementById("chat-box");
    const catButton = document.getElementById("cat-button");
    const catImageContainer = document.getElementById("cat-image-container");
    const errorMessage = document.getElementById("error-message");

    // Function to append messages to the chatbox
    function addMessage(sender, text, className) {
        const messageElement = document.createElement("p");
        messageElement.classList.add(className);
        messageElement.innerHTML = `<strong>${sender}:</strong> ${text}`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
        return messageElement;
    }

    // Function to display cat images
    function displayCatImages(imageUrls, botMessage) {
        catImageContainer.innerHTML = ""; // Clear previous images
        imageUrls.forEach((url) => {
            const img = document.createElement("img");
            img.src = url;
            img.classList.add("cat-image");
            catImageContainer.appendChild(img);
        });

        // ✅ Update the bot message once images are loaded
        botMessage.innerHTML = `<strong>Bot:</strong> Here are your cat images!`;
    }

    // Handle sending message with streaming response
    sendButton.addEventListener("click", async function () {
        const message = userInput.value.trim();
        if (!message) return;

        addMessage("You", message, "user-message");
        userInput.value = "";

        // Show typing indicator
        const botMessage = addMessage("Bot", "Bot is typing...", "bot-message");

        try {
            const response = await fetch("http://localhost:8000/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: message }),
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let botReply = "";
            let accumulatedData = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });

                try {
                    const parsedChunk = JSON.parse(chunk); // ✅ Parse JSON response

                    if (parsedChunk.reply) {
                        botReply = parsedChunk.reply;
                        botMessage.innerHTML = `<strong>Bot:</strong> ${botReply}`;
                    }

                    if (parsedChunk.image_urls) {
                        displayCatImages(parsedChunk.image_urls, botMessage);
                    }
                } catch (err) {
                    console.error("Error parsing JSON chunk:", chunk);
                }
            }
        } catch (error) {
            botMessage.innerHTML = `<strong>Bot:</strong> Failed to fetch response.`;
        }
    });

    // Handle fetching cat image (for button click)
    catButton.addEventListener("click", async function () {
        try {
            const response = await fetch("http://localhost:8000/cat");
            const data = await response.json();

            if (data.image_url) {
                const botMessage = addMessage("Bot", "Bot is typing...", "bot-message");
                displayCatImages([data.image_url], botMessage);
            }
        } catch (error) {
            errorMessage.textContent = "Failed to fetch cat image.";
        }
    });
});


