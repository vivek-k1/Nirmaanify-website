class FAQChat {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.isTyping = false;
        this.suggestionsVisible = true;
        this.suggestions = [
            "What services do you offer?",
            "How can I join the internship program?",
            "What technologies do you use?",
            "How much does training cost?",
            "Do you provide certificates?"
        ];
        
        this.init();
    }
    
    init() {
        this.createWidget();
        this.bindEvents();
        this.addWelcomeMessage();
    }
    
    createWidget() {
        const widgetHTML = `
            <div class="faq-widget">
                <div class="faq-dropdown" id="faq-dropdown">
                    <div class="faq-chat-window" id="faq-chat-window">
                        <div class="faq-chat-header">
                            <h3>Ask a Question</h3>
                            <button class="faq-close-btn" id="faq-close-btn">&times;</button>
                        </div>
                        <div class="faq-chat-body">
                            <div class="faq-messages" id="faq-messages"></div>
                            <div class="faq-typing-indicator" id="faq-typing-indicator">
                                Nirmaanify is typing...
                            </div>
                            <div class="faq-suggestions" id="faq-suggestions">
                                <div class="faq-suggestions-header">
                                    <span class="faq-suggestions-title">Quick Questions</span>
                                    <button class="faq-suggestions-toggle" id="faq-suggestions-toggle">
                                        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                                            <path d="M7 10l5 5 5-5z"/>
                                        </svg>
                                    </button>
                                </div>
                                <div class="faq-suggestion-chips" id="faq-suggestion-chips"></div>
                            </div>
                            <div class="faq-input-area">
                                <div class="faq-input-container">
                                    <input type="text" class="faq-input" id="faq-input" placeholder="Type your question...">
                                    <button class="faq-send-btn" id="faq-send-btn">
                                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <button class="faq-toggle-btn" id="faq-toggle-btn" aria-label="Open FAQ">
                    <img src="./svg/faq.svg" alt="FAQ" class="faq-toggle-icon" />
                </button>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', widgetHTML);
    }
    
    bindEvents() {
        const toggleBtn = document.getElementById('faq-toggle-btn');
        const closeBtn = document.getElementById('faq-close-btn');
        const sendBtn = document.getElementById('faq-send-btn');
        const input = document.getElementById('faq-input');
        const dropdown = document.getElementById('faq-dropdown');
        const suggestionsToggle = document.getElementById('faq-suggestions-toggle');
        
        toggleBtn.addEventListener('click', () => this.toggleChat());
        closeBtn.addEventListener('click', () => this.closeChat());
        sendBtn.addEventListener('click', () => this.sendMessage());
        suggestionsToggle.addEventListener('click', () => this.toggleSuggestions());
        
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        input.addEventListener('input', () => {
            sendBtn.disabled = !input.value.trim();
        });
        
        document.addEventListener('click', (e) => {
            if (this.isOpen && !e.target.closest('.faq-widget')) {
                this.closeChat();
            }
        });
        
        this.addSuggestions();
    }
    
    toggleChat() {
        const dropdown = document.getElementById('faq-dropdown');
        const toggleBtn = document.getElementById('faq-toggle-btn');
        
        if (this.isOpen) {
            this.closeChat();
        } else {
            this.openChat();
        }
    }
    
    openChat() {
        const dropdown = document.getElementById('faq-dropdown');
        const toggleBtn = document.getElementById('faq-toggle-btn');
        
        dropdown.classList.add('active');
        toggleBtn.style.transform = 'rotate(45deg)';
        this.isOpen = true;
        
        setTimeout(() => {
            document.getElementById('faq-input').focus();
        }, 300);
    }
    
    closeChat() {
        const dropdown = document.getElementById('faq-dropdown');
        const toggleBtn = document.getElementById('faq-toggle-btn');
        
        dropdown.classList.remove('active');
        toggleBtn.style.transform = 'rotate(0deg)';
        this.isOpen = false;
    }
    
    addWelcomeMessage() {
        const welcomeHTML = `
            <div class="faq-welcome-message">
                <h4>Hi there!</h4>
                <p>I'm here to help answer your questions about Nirmaanify. What would you like to know?</p>
            </div>
        `;
        
        this.addMessage('bot', welcomeHTML);
    }
    
    toggleSuggestions() {
        const suggestionsContainer = document.getElementById('faq-suggestion-chips');
        const toggleBtn = document.getElementById('faq-suggestions-toggle');
        
        this.suggestionsVisible = !this.suggestionsVisible;
        
        if (this.suggestionsVisible) {
            suggestionsContainer.style.display = 'flex';
            toggleBtn.style.transform = 'rotate(0deg)';
        } else {
            suggestionsContainer.style.display = 'none';
            toggleBtn.style.transform = 'rotate(180deg)';
        }
    }
    
    addSuggestions() {
        const suggestionsContainer = document.getElementById('faq-suggestion-chips');
        
        this.suggestions.forEach(suggestion => {
            const chip = document.createElement('div');
            chip.className = 'faq-suggestion-chip';
            chip.textContent = suggestion;
            chip.addEventListener('click', () => {
                document.getElementById('faq-input').value = suggestion;
                this.sendMessage();
            });
            suggestionsContainer.appendChild(chip);
        });
    }
    
    async sendMessage() {
        const input = document.getElementById('faq-input');
        const message = input.value.trim();
        
        if (!message || this.isTyping) return;
        
        this.addMessage('user', message);
        input.value = '';
        document.getElementById('faq-send-btn').disabled = true;
        
        this.showTyping();
        
        try {
            const response = await fetch('/api/faq/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: message })
            });
            
            const data = await response.json();
            
            this.hideTyping();
            
            if (data.success && data.results.length > 0) {
                const bestMatch = data.results[0];
                this.addMessage('bot', bestMatch.answer);
                
                if (data.results.length > 1) {
                    const additionalHTML = `
                        <div class="faq-additional-options">
                            <p><strong>Related questions:</strong></p>
                            ${data.results.slice(1, 3).map(faq => 
                                `<div class="faq-option" onclick="faqChat.askQuestion('${faq.question}')">
                                    ${faq.question}
                                </div>`
                            ).join('')}
                        </div>
                    `;
                    this.addMessage('bot', additionalHTML);
                }
            } else {
                this.addMessage('bot', "I couldn't find a specific answer to your question. Please try rephrasing it or contact us directly at contact@nirmaanify.com for personalized assistance.");
            }
            
        } catch (error) {
            this.hideTyping();
            this.addMessage('bot', "Sorry, I'm having trouble connecting right now. Please try again later or contact us directly.");
            console.error('FAQ search error:', error);
        }
    }
    
    askQuestion(question) {
        document.getElementById('faq-input').value = question;
        this.sendMessage();
    }
    
    showTyping() {
        this.isTyping = true;
        document.getElementById('faq-typing-indicator').classList.add('active');
        this.scrollToBottom();
    }
    
    hideTyping() {
        this.isTyping = false;
        document.getElementById('faq-typing-indicator').classList.remove('active');
    }
    
    addMessage(sender, content) {
        const messagesContainer = document.getElementById('faq-messages');
        const messageId = `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        
        const avatar = sender === 'bot' ? 'N' : 'U';
        const messageClass = sender === 'bot' ? 'bot' : 'user';
        
        const messageHTML = `
            <div class="faq-message ${messageClass}" id="${messageId}">
                <div class="faq-message-avatar">${avatar}</div>
                <div class="faq-message-bubble">${content}</div>
            </div>
        `;
        
        messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
        
        setTimeout(() => {
            const messageElement = document.getElementById(messageId);
            if (messageElement) {
                messageElement.style.opacity = '0';
                messageElement.style.transform = 'translateY(20px)';
                messageElement.style.transition = 'all 0.3s ease';
                
                setTimeout(() => {
                    messageElement.style.opacity = '1';
                    messageElement.style.transform = 'translateY(0)';
                    this.scrollToBottom();
                }, 50);
            }
            this.scrollToBottom();
        }, 10);
    }
    
    scrollToBottom() {
        const messagesContainer = document.getElementById('faq-messages');
        if (messagesContainer) {
            setTimeout(() => {
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }, 100);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    try {
        window.faqChat = new FAQChat();
    } catch (error) {
        console.error('Failed to initialize FAQ chat:', error);
    }
});

const additionalCSS = `
    .faq-additional-options {
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid #e1e5e9;
    }
    
    .faq-option {
        padding: 8px 12px;
        margin: 5px 0;
        background: #f8f9fa;
        border: 1px solid #e1e5e9;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    
    .faq-option:hover {
        background: #e9ecef;
        border-color: #6A3EE8;
    }
`;

const style = document.createElement('style');
style.textContent = additionalCSS;
document.head.appendChild(style);
