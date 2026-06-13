let conversationHistory = [];

const inputField = document.getElementById('queryInput');
const sendBtn = document.getElementById('sendBtn');
const feed = document.getElementById('chat-feed');

// Listeners for click and enter key
inputField.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendQuery();
});
sendBtn.addEventListener('click', sendQuery);

async function sendQuery() {
    const query = inputField.value.trim();
    if (!query) return;

    // 1. Render User Message
    const userDiv = document.createElement('div');
    userDiv.className = 'message user-msg';
    userDiv.innerText = query;
    feed.appendChild(userDiv);
    
    inputField.value = '';
    
    // 2. Render Temporary AI Loading State
    const aiMessageDiv = document.createElement('div');
    aiMessageDiv.className = 'message ai-msg';
    aiMessageDiv.style.color = '#8b8682';
    aiMessageDiv.innerText = 'Connecting to web stream and searching archives...';
    feed.appendChild(aiMessageDiv);
    feed.scrollTop = feed.scrollHeight;

    try {
        // 3. Open the Network Stream
        const response = await fetch('/research', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                history: conversationHistory,
                query: query
            })
        });
        
        if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullResponse = "";
        
        // Reset styles for actual response
        aiMessageDiv.style.color = ''; 
        aiMessageDiv.innerText = '';

        // 4. Stream Loop: Read data chunks as they arrive
        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            
            fullResponse += decoder.decode(value, { stream: true });
            aiMessageDiv.innerHTML = marked.parse(fullResponse);
            feed.scrollTop = feed.scrollHeight;
        }

        // 5. Save context to short-term memory
        conversationHistory.push({ role: "user", content: query });
        conversationHistory.push({ role: "model", content: fullResponse });

    } catch (err) {
        console.error(err);
        aiMessageDiv.style.color = '#ef4444'; // Tailwind Red-500
        aiMessageDiv.innerText = 'Stream connection interrupted. Please try again.';
    }
}