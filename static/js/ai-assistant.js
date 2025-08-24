// HackHub AI Assistant - Sidebar Version

class AIAssistant {
    constructor() {
        this.isLoading = false;
        this.messages = [];
        this.maxMessages = 50;

        this.init();
    }

    init() {
        this.bindEvents();
        this.loadChatHistory();
        this.showSuggestedQuestions();
    }

    bindEvents() {
        // Send button
        const sendBtn = document.getElementById('aiSendButton');
        if (sendBtn) {
            sendBtn.addEventListener('click', () => this.sendMessage());
        }

        // Input field
        const aiInput = document.getElementById('aiInput');
        if (aiInput) {
            aiInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });

            aiInput.addEventListener('input', () => {
                this.updateSendButton();
            });
        }

        // Chat close button
        const closeBtn = document.querySelector('.chat-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.close());
        }
    }

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        const container = document.getElementById('chatContainer');
        const badge = document.getElementById('chatBadge');

        if (container) {
            container.classList.add('active');
            this.isOpen = true;

            // Hide badge when open
            if (badge) {
                badge.style.display = 'none';
            }

            // Focus input
            setTimeout(() => {
                const input = document.getElementById('aiInput');
                if (input) input.focus();
            }, 300);

            // Scroll to bottom
            this.scrollToBottom();
        }
    }

    close() {
        const container = document.getElementById('chatContainer');
        const badge = document.getElementById('chatBadge');

        if (container) {
            container.classList.remove('active');
            this.isOpen = false;

            // Show badge when closed
            if (badge) {
                badge.style.display = 'flex';
            }
        }
    }

    async sendMessage(message = null, context = null) {
        const input = document.getElementById('aiInput');
        const messageText = message || (input ? input.value.trim() : '');

        if (!messageText || this.isLoading) return;

        // Clear input
        if (input && !message) {
            input.value = '';
        }

        // Add user message
        this.addMessage('user', messageText);

        // Show loading
        this.setLoading(true);

        try {
            const response = await fetch('/api/ai-chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: messageText,
                    context: context || this.getContext()
                })
            });

            const data = await response.json();

            if (data.success) {
                this.addMessage('ai', data.response);
            } else {
                this.addMessage('ai', 'Sorry, I encountered an error. Please try again.');
            }
        } catch (error) {
            console.error('AI Chat Error:', error);
            this.addMessage('ai', 'I\'m having trouble connecting right now. Please try again in a moment.');
        } finally {
            this.setLoading(false);
        }
    }

    addMessage(type, content) {
        const messagesContainer = document.getElementById('aiMessages');
        if (!messagesContainer) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `${type}-message`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'ai-content';
        contentDiv.textContent = content;

        messageDiv.appendChild(contentDiv);
        messagesContainer.appendChild(messageDiv);

        // Store message
        this.messages.push({
            type,
            content,
            timestamp: new Date().toISOString()
        });

        // Limit message history
        if (this.messages.length > this.maxMessages) {
            this.messages = this.messages.slice(-this.maxMessages);

            // Remove old DOM elements
            const oldMessages = messagesContainer.querySelectorAll('.ai-message, .user-message');
            if (oldMessages.length > this.maxMessages) {
                for (let i = 0; i < oldMessages.length - this.maxMessages; i++) {
                    oldMessages[i].remove();
                }
            }
        }

        this.scrollToBottom();
        this.saveChatHistory();
        this.updateSendButton();
    }

    addWelcomeMessage() {
        // Don't add welcome message if there's already chat history
        if (this.messages.length === 0) {
            const welcomeMessage = "👋 Hi! I'm your HackHub AI assistant. I can help you with team formation, project ideas, and hackathon advice. What would you like to know?";
            // Don't add to messages array since this is already in HTML
        }
    }

    setLoading(loading) {
        this.isLoading = loading;
        const sendBtn = document.getElementById('aiSendButton');
        const input = document.getElementById('aiInput');

        if (sendBtn) {
            sendBtn.disabled = loading;
            sendBtn.innerHTML = loading ?
                '<i class="fas fa-spinner fa-spin"></i>' :
                '<i class="fas fa-paper-plane"></i>';
        }

        if (input) {
            input.disabled = loading;
        }

        if (loading) {
            this.addTypingIndicator();
        } else {
            this.removeTypingIndicator();
        }
    }

    addTypingIndicator() {
        const messagesContainer = document.getElementById('aiMessages');
        if (!messagesContainer) return;

        // Remove existing typing indicator
        this.removeTypingIndicator();

        const typingDiv = document.createElement('div');
        typingDiv.className = 'ai-message typing-indicator';
        typingDiv.innerHTML = `
            <div class="message-content">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;

        messagesContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }

    removeTypingIndicator() {
        const indicator = document.querySelector('.typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    scrollToBottom() {
        const messagesContainer = document.getElementById('aiMessages');
        if (messagesContainer) {
            setTimeout(() => {
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }, 100);
        }
    }

    updateSendButton() {
        const input = document.getElementById('aiInput');
        const sendBtn = document.getElementById('aiSendButton');

        if (input && sendBtn) {
            const hasText = input.value.trim().length > 0;
            sendBtn.disabled = !hasText || this.isLoading;
            sendBtn.style.opacity = (hasText && !this.isLoading) ? '1' : '0.5';
        }
    }

    getContext() {
        // Gather context from current page
        const context = {
            page: window.location.pathname,
            url: window.location.href
        };

        // Add page-specific context
        if (context.page.includes('participants')) {
            context.type = 'participants';
            context.participant_count = document.querySelectorAll('.participant-card').length;
        } else if (context.page.includes('teams')) {
            context.type = 'teams';
            context.team_count = document.querySelectorAll('.team-card').length;
        } else if (context.page.includes('hackathons')) {
            context.type = 'hackathons';
            context.hackathon_count = document.querySelectorAll('.hackathon-card').length;
        } else if (context.page.includes('register')) {
            context.type = 'registration';
        } else {
            context.type = 'dashboard';
        }

        return context;
    }

    saveChatHistory() {
        try {
            const history = {
                messages: this.messages.slice(-20), // Save last 20 messages
                timestamp: new Date().toISOString()
            };
            localStorage.setItem('hackhub_chat_history', JSON.stringify(history));
        } catch (error) {
            console.error('Failed to save chat history:', error);
        }
    }

    loadChatHistory() {
        try {
            const history = localStorage.getItem('hackhub_chat_history');
            if (history) {
                const parsed = JSON.parse(history);
                const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);

                // Only load recent history (within 24 hours)
                if (new Date(parsed.timestamp) > oneDayAgo) {
                    this.messages = parsed.messages || [];
                    this.renderChatHistory();
                }
            }
        } catch (error) {
            console.error('Failed to load chat history:', error);
        }
    }

    renderChatHistory() {
        const messagesContainer = document.getElementById('aiMessages');
        if (!messagesContainer || this.messages.length === 0) return;

        // Clear existing messages (except welcome message)
        const existingMessages = messagesContainer.querySelectorAll('.ai-message:not(:first-child), .user-message');
        existingMessages.forEach(msg => msg.remove());

        // Render stored messages
        this.messages.forEach(message => {
            const messageDiv = document.createElement('div');
            messageDiv.className = `${message.type}-message`;

            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = message.content;

            messageDiv.appendChild(contentDiv);
            messagesContainer.appendChild(messageDiv);
        });

        this.scrollToBottom();
    }

    clearHistory() {
        this.messages = [];
        localStorage.removeItem('hackhub_chat_history');

        const messagesContainer = document.getElementById('chatMessages');
        if (messagesContainer) {
            // Clear all messages except welcome message
            const messages = messagesContainer.querySelectorAll('.ai-message:not(:first-child), .user-message');
            messages.forEach(msg => msg.remove());
        }
    }

    // Enhanced suggested prompts for comprehensive hackathon help
    getSuggestedPrompts() {
        const suggestions = {
            dashboard: [
                "What is a hackathon and how do they work?",
                "How do I form effective hackathon teams?",
                "Give me project ideas for my team",
                "What should I bring to a hackathon?",
                "How can I win a hackathon?"
            ],
            participants: [
                "How do I find the right teammates?",
                "What skills should I look for in team members?",
                "How do I present my skills effectively?",
                "What if I have no experience?",
                "How to network at hackathons?"
            ],
            teams: [
                "How do we decide on a project quickly?",
                "What's the best way to manage our time?",
                "How do we divide the work effectively?",
                "Technical tips for rapid development?",
                "How to prepare a winning demo?"
            ],
            hackathons: [
                "How do I choose the right hackathon?",
                "What should I know before attending?",
                "How do I prepare for my first hackathon?",
                "What are common hackathon pitfalls?",
                "How to stay motivated during long hours?"
            ],
            registration: [
                "What experience level should I select?",
                "How do I describe my skills effectively?",
                "What makes a good team member?",
                "What role should I choose?",
                "How to prepare for team formation?"
            ]
        };

        const context = this.getContext();
        return suggestions[context.type] || suggestions.dashboard;
    }

    showSuggestedQuestions() {
        const messagesContainer = document.getElementById('aiMessages');
        if (!messagesContainer) return;

        // Only show if there are no messages yet
        if (this.messages.length > 0) return;

        const suggestions = this.getSuggestedPrompts();
        const suggestionsDiv = document.createElement('div');
        suggestionsDiv.className = 'suggested-prompts';
        suggestionsDiv.innerHTML = `
            <div class="prompts-title">💡 Try asking me:</div>
            <div class="prompts-grid">
                ${suggestions.map(prompt => `
                    <button class="prompt-button" onclick="window.aiAssistant.sendMessage('${prompt.replace(/'/g, "\\'")}')">${prompt}</button>
                `).join('')}
            </div>
        `;

        messagesContainer.appendChild(suggestionsDiv);
        this.scrollToBottom();
    }

    addSuggestedPrompts() {
        const messagesContainer = document.getElementById('aiMessages');
        if (!messagesContainer) return;

        const suggestions = this.getSuggestedPrompts();
        const suggestionsDiv = document.createElement('div');
        suggestionsDiv.className = 'suggested-prompts';
        suggestionsDiv.innerHTML = `
            <div class="prompts-title">💡 Try asking me:</div>
            <div class="prompts-grid">
                ${suggestions.map(prompt => `
                    <button class="prompt-button" onclick="window.aiAssistant.sendMessage('${prompt.replace(/'/g, "\\'")}')">${prompt}</button>
                `).join('')}
            </div>
        `;

        messagesContainer.appendChild(suggestionsDiv);
        this.scrollToBottom();
    }
}

// Global functions for external access
function toggleAIChat() {
    if (window.aiAssistant) {
        window.aiAssistant.toggle();
    }
}

function sendMessage() {
    if (window.aiAssistant) {
        window.aiAssistant.sendMessage();
    }
}

// Function to send AI message with context (used by other components)
function sendAIMessage(message, context) {
    if (window.aiAssistant) {
        // Open chat if not already open
        if (!window.aiAssistant.isOpen) {
            window.aiAssistant.open();
        }

        // Send message with context
        window.aiAssistant.sendMessage(message, context);
    }
}

// Initialize AI Assistant when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing AI Assistant...');
    window.aiAssistant = new AIAssistant();

    // Make sendAIMessage globally available
    window.sendAIMessage = sendAIMessage;

    // Add additional click handler as backup
    const chatToggle = document.querySelector('.chat-toggle');
    if (chatToggle) {
        chatToggle.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Chat toggle clicked!');
            if (window.aiAssistant) {
                window.aiAssistant.toggle();
            }
        });
        console.log('AI Assistant initialized successfully!');
    } else {
        console.error('Chat toggle button not found!');
    }
});

// Add CSS for typing indicator and suggested prompts
const aiAssistantStyles = `
    .typing-dots {
        display: flex;
        gap: 4px;
        align-items: center;
        padding: 8px 0;
    }

    .typing-dots span {
        width: 8px;
        height: 8px;
        background: var(--accent-purple);
        border-radius: 50%;
        opacity: 0.4;
        animation: typing 1.4s infinite ease-in-out;
    }

    .typing-dots span:nth-child(1) {
        animation-delay: 0s;
    }

    .typing-dots span:nth-child(2) {
        animation-delay: 0.2s;
    }

    .typing-dots span:nth-child(3) {
        animation-delay: 0.4s;
    }

    @keyframes typing {
        0%, 60%, 100% {
            opacity: 0.4;
            transform: scale(1);
        }
        30% {
            opacity: 1;
            transform: scale(1.2);
        }
    }

    .suggested-prompts {
        margin: 1rem 0;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .prompts-title {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-bottom: 0.75rem;
        font-weight: 600;
    }

    .prompt-button {
        display: block;
        width: 100%;
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        color: var(--accent-purple);
        padding: 0.5rem 0.75rem;
        border-radius: 6px;
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
        cursor: pointer;
        transition: var(--transition-fast);
        text-align: left;
    }

    .prompt-button:hover {
        background: rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.5);
        transform: translateX(2px);
    }

    .prompt-button:last-child {
        margin-bottom: 0;
    }

    .chat-input-container input:focus + button {
        background: var(--secondary-gradient);
    }

    .message-content {
        word-wrap: break-word;
        overflow-wrap: break-word;
        line-height: 1.4;
    }

    .ai-message .message-content {
        position: relative;
    }

    .ai-message .message-content::before {
        content: '🤖';
        position: absolute;
        left: -25px;
        top: 0;
        font-size: 0.8rem;
        opacity: 0.7;
    }

    .user-message .message-content {
        position: relative;
    }

    .user-message .message-content::after {
        content: '👤';
        position: absolute;
        right: -25px;
        top: 0;
        font-size: 0.8rem;
        opacity: 0.7;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .chat-container {
            width: calc(100vw - 40px);
            right: 20px;
            left: 20px;
            bottom: 80px;
        }

        .chat-toggle {
            width: 50px;
            height: 50px;
        }

        .chat-toggle i {
            font-size: 1.2rem;
        }
    }

    /* High contrast mode */
    @media (prefers-contrast: high) {
        .typing-dots span {
            background: var(--text-primary);
        }

        .prompt-button {
            border-color: var(--text-primary);
            color: var(--text-primary);
        }
    }

    /* Suggested prompts styling */
    .suggested-prompts {
        margin: 1rem 0;
        padding: 1rem;
        background: linear-gradient(135deg, #f8f9ff 0%, #f0f3ff 100%);
        border-radius: 12px;
        border-left: 4px solid #007bff;
    }

    .prompts-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #495057;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .prompts-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 0.5rem;
    }

    @media (min-width: 576px) {
        .prompts-grid {
            grid-template-columns: 1fr 1fr;
        }
    }

    .prompt-button {
        background: white;
        border: 1px solid #e1e8f0;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-size: 0.85rem;
        color: #495057;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: left;
        line-height: 1.4;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    .prompt-button:hover {
        background: #007bff;
        color: white;
        border-color: #007bff;
        transform: translateY(-1px);
        box-shadow: 0 2px 6px rgba(0,123,255,0.15);
    }

    .prompt-button:active {
        transform: translateY(0);
    }

    /* Reduced motion */
    @media (prefers-reduced-motion: reduce) {
        .typing-dots span {
            animation: none;
            opacity: 1;
        }

        .chat-container {
            transition: none;
        }

        .prompt-button {
            transition: none;
        }

        .prompt-button:hover {
            transform: none;
        }
    }
`;

// Inject AI assistant styles
const aiStyleSheet = document.createElement('style');
aiStyleSheet.textContent = aiAssistantStyles;
document.head.appendChild(aiStyleSheet);
