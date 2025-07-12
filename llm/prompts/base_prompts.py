from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class UserContext:
    """Context container for personalizing assistant responses"""
    current_time: datetime
    energy_level: str = "medium"
    personality_mode: str = "coach"
    recent_tasks: list = None
    calendar_events: list = None
    habit_patterns: dict = None
    
    def __post_init__(self):
        if self.recent_tasks is None:
            self.recent_tasks = []
        if self.calendar_events is None:
            self.calendar_events = []
        if self.habit_patterns is None:
            self.habit_patterns = {}

class BasePromptTemplate:
    """Base class for all prompt templates"""
    
    PERSONALITY_MODES = {
        "coach": {
            "tone": "encouraging and supportive",
            "style": "like a professional productivity coach",
            "language": "motivational but not pushy"
        },
        "friend": {
            "tone": "casual and friendly",
            "style": "like a helpful friend",
            "language": "conversational and relaxed"
        },
        "strict": {
            "tone": "direct and focused",
            "style": "like an efficient executive assistant",
            "language": "clear and action-oriented"
        },
        "zen": {
            "tone": "calm and mindful",
            "style": "like a mindfulness teacher",
            "language": "peaceful and reflective"
        }
    }
    
    def __init__(self, context: UserContext):
        self.context = context
        self.personality = self.PERSONALITY_MODES.get(
            context.personality_mode, 
            self.PERSONALITY_MODES["coach"]
        )
    
    def get_base_instructions(self) -> str:
        """Common instructions for all prompts"""
        return f"""
You are Timely, an AI productivity coach. Your role is to help users manage their time effectively and reduce decision fatigue.

PERSONALITY: Act {self.personality['tone']} - {self.personality['style']}. Use {self.personality['language']} language.

CORE PRINCIPLES:
- Be decisive but not overwhelming
- Consider the user's energy level: {self.context.energy_level}
- Keep responses concise and actionable
- Always suggest ONE clear next action
- Time context: {self.context.current_time.strftime('%A, %B %d, %Y at %I:%M %p')}

RESPONSE FORMAT:
- Lead with the most important point
- Use clear, specific language
- Include brief reasoning when helpful
- End with a motivational touch (personality appropriate)
"""

class WhatToDoNextPrompt(BasePromptTemplate):
    """Prompt template for 'What should I do next?' queries"""
    
    def build_prompt(self, user_input: str, available_tasks: list) -> str:
        task_context = self._format_tasks(available_tasks)
        
        return f"""
{self.get_base_instructions()}

USER REQUEST: "{user_input}"

AVAILABLE TASKS:
{task_context}

CURRENT CONTEXT:
- Energy Level: {self.context.energy_level}
- Recent Activity: {self._format_recent_activity()}
- Calendar: {self._format_calendar()}

TASK: Suggest ONE specific task the user should do next. Consider:
1. Urgency and deadlines
2. Energy level match
3. Time available
4. Natural workflow

RESPONSE FORMAT:
**Next Task:** [Clear task name]
**Why Now:** [Brief reasoning]
**Duration:** [Estimated time]
{self._get_personality_closer()}
"""
    
    def _format_tasks(self, tasks: list) -> str:
        if not tasks:
            return "No pending tasks in the system."
        
        formatted = []
        for task in tasks[:10]:  # Limit to prevent prompt overflow
            priority_emoji = {"low": "🔵", "medium": "🟡", "high": "🟠", "urgent": "🔴"}
            emoji = priority_emoji.get(task.get('priority', 'medium'), '⚪')
            formatted.append(f"{emoji} {task['title']} (Priority: {task['priority']})")
        
        return "\n".join(formatted)
    
    def _format_recent_activity(self) -> str:
        if not self.context.recent_tasks:
            return "No recent activity"
        return f"Recently completed: {', '.join(self.context.recent_tasks[-3:])}"
    
    def _format_calendar(self) -> str:
        if not self.context.calendar_events:
            return "No upcoming events"
        return f"Next: {self.context.calendar_events[0]['title']} at {self.context.calendar_events[0]['time']}"
    
    def _get_personality_closer(self) -> str:
        closers = {
            "coach": "You've got this! 💪",
            "friend": "Hope this helps! 😊",
            "strict": "Execute immediately.",
            "zen": "Focus on this moment. 🧘"
        }
        return closers.get(self.context.personality_mode, "Let's get started! ✨")