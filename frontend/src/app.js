// frontend/src/app.js - Complete Timely Frontend Application

console.log('🚀 Timely Frontend Loading...');

class TimelyApp {
    constructor() {
        this.API_BASE_URL = 'http://127.0.0.1:8000/api/v1';
        this.currentTasks = [];
        this.chatHistory = [];
        this.totalTokens = 0;
        this.isConnected = false;

        this.init();
    }

    async init() {
        console.log('🎯 Initializing Timely App...');

        await this.checkConnection();
        this.initializeDOM();
        this.setupEventListeners();
        this.loadSampleData();
        this.showWelcomeMessage();
        this.updateDisplays();

        console.log('✅ App initialization complete!');
    }

    async checkConnection() {
        const statusElement = document.getElementById('connectionStatus');

        try {
            console.log('Testing connection to backend...');
            const response = await fetch('http://127.0.0.1:8000/health');

            if (response.ok) {
                console.log('✅ Backend connected successfully!');
                this.isConnected = true;

                if (statusElement) {
                    statusElement.className = 'w-2 h-2 bg-green-500 rounded-full animate-pulse';
                }

                this.showToast('Connected to Timely AI!', 'success');
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            console.error('❌ Connection failed:', error);
            this.isConnected = false;

            if (statusElement) {
                statusElement.className = 'w-2 h-2 bg-red-500 rounded-full';
            }

            this.showToast('Backend connection failed', 'error');
        }
    }

    initializeDOM() {
        this.elements = {
            // Settings
            energySelect: document.getElementById('energySelect'),
            personalitySelect: document.getElementById('personalitySelect'),
            energyDisplay: document.getElementById('energyDisplay'),
            personalityDisplay: document.getElementById('personalityDisplay'),
            connectionStatus: document.getElementById('connectionStatus'),

            // Chat
            chatMessages: document.getElementById('chatMessages'),
            chatForm: document.getElementById('chatForm'),
            messageInput: document.getElementById('messageInput'),
            sendBtn: document.getElementById('sendBtn'),

            // Quick actions
            morningBtn: document.getElementById('morningBtn'),
            planDayBtn: document.getElementById('planDayBtn'),
            clearChatBtn: document.getElementById('clearChatBtn'),

            // Tasks
            taskForm: document.getElementById('taskForm'),
            taskTitle: document.getElementById('taskTitle'),
            taskPriority: document.getElementById('taskPriority'),
            taskDuration: document.getElementById('taskDuration'),
            tasksList: document.getElementById('tasksList'),
            taskCount: document.getElementById('taskCount'),

            // Metrics
            tokensUsed: document.getElementById('tokensUsed'),
            toastContainer: document.getElementById('toastContainer')
        };
    }

    setupEventListeners() {
        // Chat form
        if (this.elements.chatForm) {
            this.elements.chatForm.addEventListener('submit', (e) => this.handleChatSubmit(e));
        }

        // Settings
        if (this.elements.energySelect) {
            this.elements.energySelect.addEventListener('change', () => this.updateDisplays());
        }
        if (this.elements.personalitySelect) {
            this.elements.personalitySelect.addEventListener('change', () => this.updateDisplays());
        }

        // Quick actions
        if (this.elements.morningBtn) {
            this.elements.morningBtn.addEventListener('click', () => this.handleMorningCheckin());
        }
        if (this.elements.planDayBtn) {
            this.elements.planDayBtn.addEventListener('click', () => this.handlePlanDay());
        }
        if (this.elements.clearChatBtn) {
            this.elements.clearChatBtn.addEventListener('click', () => this.clearChat());
        }

        // Tasks
        if (this.elements.taskForm) {
            this.elements.taskForm.addEventListener('submit', (e) => this.handleAddTask(e));
        }

        // Quick suggestions
        document.querySelectorAll('.quick-suggestion').forEach(btn => {
            btn.addEventListener('click', () => {
                if (this.elements.messageInput) {
                    this.elements.messageInput.value = btn.textContent.trim();
                    if (this.elements.chatForm) {
                        this.elements.chatForm.dispatchEvent(new Event('submit'));
                    }
                }
            });
        });

        // Enter key for chat input
        if (this.elements.messageInput) {
            this.elements.messageInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    if (this.elements.chatForm) {
                        this.elements.chatForm.dispatchEvent(new Event('submit'));
                    }
                }
            });
        }
    }

    loadSampleData() {
        this.currentTasks = [
            {
                id: 1,
                title: "Review project proposal",
                priority: "high",
                estimated_duration: 45,
                category: "work"
            },
            {
                id: 2,
                title: "Check emails",
                priority: "medium",
                estimated_duration: 15,
                category: "admin"
            },
            {
                id: 3,
                title: "Team meeting prep",
                priority: "high",
                estimated_duration: 30,
                category: "work"
            }
        ];

        this.updateTasksList();
    }

    updateDisplays() {
        const energy = this.elements.energySelect?.value || 'medium';
        const personality = this.elements.personalitySelect?.value || 'coach';

        if (this.elements.energyDisplay) {
            this.elements.energyDisplay.textContent = `${energy.charAt(0).toUpperCase() + energy.slice(1)} Energy`;
        }
        if (this.elements.personalityDisplay) {
            this.elements.personalityDisplay.textContent = `${personality.charAt(0).toUpperCase() + personality.slice(1)} Mode`;
        }
    }

    async handleChatSubmit(e) {
        e.preventDefault();

        const message = this.elements.messageInput?.value.trim();
        if (!message) return;

        // Clear input and disable button
        if (this.elements.messageInput) this.elements.messageInput.value = '';
        if (this.elements.sendBtn) this.elements.sendBtn.disabled = true;

        // Add user message
        this.addMessage('user', message);

        // Show typing indicator
        const typingId = this.addTypingIndicator();

        try {
            let endpoint = '/chat/next-task';
            if (message.toLowerCase().includes('plan') || message.toLowerCase().includes('schedule')) {
                endpoint = '/chat/plan-day';
            }

            const requestData = {
                message: message,
                energy_level: this.elements.energySelect?.value || 'medium',
                personality_mode: this.elements.personalitySelect?.value || 'coach',
                tasks: this.currentTasks
            };

            const response = await fetch(`${this.API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const result = await response.json();

            this.removeTypingIndicator(typingId);

            this.addMessage('assistant', result.response, {
                tokens: result.tokens_used,
                fallback: result.fallback,
                timestamp: result.timestamp
            });

            if (result.tokens_used) {
                this.totalTokens += result.tokens_used;
                this.updateTokenCounter();
            }

        } catch (error) {
            console.error('API Error:', error);
            this.removeTypingIndicator(typingId);

            this.addMessage('assistant', 'Sorry, I\'m having trouble connecting right now. Please make sure the backend is running and try again.', {
                error: true
            });

            this.showToast('Connection error. Check if backend is running.', 'error');
        }

        if (this.elements.sendBtn) this.elements.sendBtn.disabled = false;
        if (this.elements.messageInput) this.elements.messageInput.focus();
    }

    async handleMorningCheckin() {
        if (this.elements.morningBtn) this.elements.morningBtn.disabled = true;

        const requestData = {
            message: "Good morning!",
            energy_level: this.elements.energySelect?.value || 'medium',
            personality_mode: this.elements.personalitySelect?.value || 'coach',
            tasks: this.currentTasks
        };

        try {
            const response = await fetch(`${this.API_BASE_URL}/chat/morning-checkin`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestData)
            });

            const result = await response.json();

            this.addMessage('assistant', result.response, {
                tokens: result.tokens_used,
                type: 'morning-checkin'
            });

            if (result.tokens_used) {
                this.totalTokens += result.tokens_used;
                this.updateTokenCounter();
            }

        } catch (error) {
            console.error('Morning checkin error:', error);
            this.showToast('Could not complete morning check-in', 'error');
        }

        if (this.elements.morningBtn) this.elements.morningBtn.disabled = false;
    }

    async handlePlanDay() {
        if (this.elements.planDayBtn) this.elements.planDayBtn.disabled = true;

        const requestData = {
            message: "Plan my day",
            energy_level: this.elements.energySelect?.value || 'medium',
            personality_mode: this.elements.personalitySelect?.value || 'coach',
            tasks: this.currentTasks
        };

        try {
            const response = await fetch(`${this.API_BASE_URL}/chat/plan-day`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestData)
            });

            const result = await response.json();

            this.addMessage('user', 'Plan my day');
            this.addMessage('assistant', result.response, {
                tokens: result.tokens_used,
                type: 'day-plan'
            });

            if (result.tokens_used) {
                this.totalTokens += result.tokens_used;
                this.updateTokenCounter();
            }

        } catch (error) {
            console.error('Day planning error:', error);
            this.showToast('Could not create day plan', 'error');
        }

        if (this.elements.planDayBtn) this.elements.planDayBtn.disabled = false;
    }

    handleAddTask(e) {
        e.preventDefault();

        const title = this.elements.taskTitle?.value.trim();
        const priority = this.elements.taskPriority?.value || 'medium';
        const duration = parseInt(this.elements.taskDuration?.value) || 30;

        if (!title) return;

        const newTask = {
            id: Date.now(),
            title: title,
            priority: priority,
            estimated_duration: duration,
            category: 'general'
        };

        this.currentTasks.push(newTask);
        this.updateTasksList();

        if (this.elements.taskForm) this.elements.taskForm.reset();
        if (this.elements.taskDuration) this.elements.taskDuration.value = 30;

        this.showToast(`Added task: ${title}`, 'success');
    }

    removeTask(taskId) {
        this.currentTasks = this.currentTasks.filter(task => task.id !== taskId);
        this.updateTasksList();
        this.showToast('Task completed!', 'success');
    }

    updateTasksList() {
        if (!this.elements.tasksList || !this.elements.taskCount) return;

        this.elements.taskCount.textContent = this.currentTasks.length;

        if (this.currentTasks.length === 0) {
            this.elements.tasksList.innerHTML = '<p class="text-gray-500 text-sm">No tasks yet. Add one above!</p>';
            return;
        }

        this.elements.tasksList.innerHTML = this.currentTasks.map(task => {
            const priorityColors = {
                low: 'bg-blue-100 text-blue-800',
                medium: 'bg-yellow-100 text-yellow-800',
                high: 'bg-orange-100 text-orange-800',
                urgent: 'bg-red-100 text-red-800'
            };

            return `
                <div class="task-item">
                    <div class="flex items-center justify-between">
                        <div class="flex-1">
                            <div class="font-medium text-gray-900">${task.title}</div>
                            <div class="flex items-center space-x-2 mt-1">
                                <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${priorityColors[task.priority]}">
                                    <i class="fas fa-circle mr-1"></i>${task.priority}
                                </span>
                                <span class="text-sm text-gray-500">
                                    <i class="fas fa-clock mr-1"></i>${task.estimated_duration} min
                                </span>
                            </div>
                        </div>
                        <button 
                            onclick="app.removeTask(${task.id})"
                            class="text-green-600 hover:text-green-700 p-2 rounded-lg hover:bg-green-50 transition-colors"
                            title="Mark complete"
                        >
                            <i class="fas fa-check"></i>
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }

    addMessage(role, content, metadata = {}) {
        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        if (!this.elements.chatMessages) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = 'animate-fade-in';

        if (role === 'user') {
            messageDiv.innerHTML = `
                <div class="flex items-start space-x-3 justify-end mb-4">
                    <div class="flex-1 max-w-xs lg:max-w-md">
                        <div class="bg-blue-600 text-white rounded-lg px-4 py-3">
                            <div class="flex items-center space-x-2 mb-2 justify-end">
                                <span class="text-xs text-blue-100">${timestamp}</span>
                                <span class="font-semibold text-white">You</span>
                            </div>
                            <div class="text-white">${content}</div>
                        </div>
                    </div>
                    <div class="flex-shrink-0">
                        <div class="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
                            <i class="fas fa-user text-gray-600 text-sm"></i>
                        </div>
                    </div>
                </div>
            `;
        } else {
            const badges = [];
            if (metadata.tokens) badges.push(`<span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded"><i class="fas fa-brain mr-1"></i>${metadata.tokens} tokens</span>`);
            if (metadata.fallback) badges.push(`<span class="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded"><i class="fas fa-cog mr-1"></i>Offline</span>`);
            if (metadata.error) badges.push(`<span class="text-xs bg-red-100 text-red-800 px-2 py-1 rounded"><i class="fas fa-exclamation-triangle mr-1"></i>Error</span>`);

            messageDiv.innerHTML = `
                <div class="flex items-start space-x-3 mb-4">
                    <div class="flex-shrink-0">
                        <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                            <i class="fas fa-robot text-white text-sm"></i>
                        </div>
                    </div>
                    <div class="flex-1">
                        <div class="bg-gray-100 rounded-lg px-4 py-3">
                            <div class="flex items-center space-x-2 mb-2">
                                <span class="font-semibold text-gray-900">Timely</span>
                                <span class="text-xs text-gray-500">${timestamp}</span>
                                ${badges.join(' ')}
                            </div>
                            <div class="text-gray-800">${this.formatResponse(content)}</div>
                        </div>
                    </div>
                </div>
            `;
        }

        this.elements.chatMessages.appendChild(messageDiv);
        this.elements.chatMessages.scrollTop = this.elements.chatMessages.scrollHeight;
    }

    formatResponse(content) {
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>')
            .replace(/^• /gm, '<br>• ');
    }

    addTypingIndicator() {
        if (!this.elements.chatMessages) return null;

        const typingDiv = document.createElement('div');
        typingDiv.className = 'flex items-start space-x-3 typing-indicator mb-4';
        typingDiv.innerHTML = `
            <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                    <i class="fas fa-robot text-white text-sm"></i>
                </div>
            </div>
            <div class="flex-1">
                <div class="bg-gray-100 rounded-lg px-4 py-3">
                    <div class="flex items-center space-x-2">
                        <span class="font-semibold text-gray-900">Timely</span>
                        <span class="text-xs text-gray-500">typing...</span>
                    </div>
                    <div class="flex space-x-1 mt-2">
                        <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                        <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                    </div>
                </div>
            </div>
        `;

        this.elements.chatMessages.appendChild(typingDiv);
        this.elements.chatMessages.scrollTop = this.elements.chatMessages.scrollHeight;
        return typingDiv;
    }

    removeTypingIndicator(typingElement) {
        if (typingElement && typingElement.parentNode) {
            typingElement.parentNode.removeChild(typingElement);
        }
    }

    updateTokenCounter() {
        if (this.elements.tokensUsed) {
            this.elements.tokensUsed.innerHTML = `<i class="fas fa-brain mr-1"></i>${this.totalTokens} tokens`;
        }
    }

    clearChat() {
        if (this.elements.chatMessages) {
            this.elements.chatMessages.innerHTML = '';
        }
        this.chatHistory = [];
        this.showWelcomeMessage();
        this.showToast('Chat cleared', 'info');
    }

    showWelcomeMessage() {
        this.addMessage('assistant', `
            <strong>Welcome to Timely!</strong> I'm your AI productivity coach.
            <br><br>
            I'm here to help you:
            <br>• <strong>Decide what to do next</strong> when you're feeling overwhelmed
            <br>• <strong>Plan your day</strong> with realistic time blocks
            <br>• <strong>Stay motivated</strong> with personalized coaching
            <br><br>
            Try asking me "What should I do next?" or "Plan my day"
        `);
    }

    showToast(message, type = 'info') {
        // Create toast container if it doesn't exist
        let toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toastContainer';
            toastContainer.className = 'fixed top-4 right-4 space-y-2 z-50';
            document.body.appendChild(toastContainer);
            console.log('✅ Created toast container');
        }

        const toast = document.createElement('div');
        const colors = {
            success: 'bg-green-500',
            error: 'bg-red-500',
            info: 'bg-blue-500',
            warning: 'bg-yellow-500'
        };

        toast.className = `${colors[type]} text-white px-4 py-2 rounded-lg shadow-lg mb-2 animate-slide-up`;
        toast.textContent = message;

        toastContainer.appendChild(toast);

        // Auto-remove after 4 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 4000);
    }
}

// Initialize app when DOM loads
document.addEventListener('DOMContentLoaded', function () {
    console.log('🚀 Initializing Complete Timely App...');
    window.app = new TimelyApp();
});