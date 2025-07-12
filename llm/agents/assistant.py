from openai import OpenAI
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from backend.core.config import settings

class TimelyAssistant:
    """Main AI assistant for Timely productivity coaching"""
    
    def __init__(self):
        # Initialize OpenAI client with error handling
        try:
            print(f"Initializing OpenAI client...")
            print(f"API key from settings: {settings.openai_api_key[:10]}...{settings.openai_api_key[-4:] if settings.openai_api_key else 'None'}")
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.model = "gpt-3.5-turbo"  # Use the more stable model
            self.client_ready = bool(settings.openai_api_key)
            print(f"OpenAI client initialized: API key configured={self.client_ready}")
        except Exception as e:
            print(f"Warning: OpenAI client initialization failed: {e}")
            self.client_ready = False
            self.client = None
        
    async def what_should_i_do_next(
        self, 
        user_input: str = "What should I do next?",
        available_tasks: List[Dict] = None,
        energy_level: str = "medium",
        personality_mode: str = "coach"
    ) -> Dict[str, Any]:
        """
        Core functionality: Suggest the next task based on context
        """
        
        # If OpenAI isn't available, use intelligent fallback
        if not self.client_ready:
            print("OpenAI client not ready, using fallback")
            return self._get_smart_fallback(user_input, available_tasks, energy_level, personality_mode)
        
        try:
            current_time = datetime.now()
            
            # Build the prompt
            prompt = self._build_next_task_prompt(
                user_input, available_tasks, energy_level, personality_mode, current_time
            )
            
            print(f"Attempting OpenAI API call with model: {self.model}")
            # Call OpenAI using the modern client
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are Timely, an AI productivity coach focused on helping users decide what to do next with minimal decision fatigue."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            print(f"OpenAI API call successful, tokens used: {response.usage.total_tokens}")
            
            assistant_response = response.choices[0].message.content
            
            return {
                "response": assistant_response,
                "tokens_used": response.usage.total_tokens,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "context_used": {
                    "energy_level": energy_level,
                    "personality_mode": personality_mode,
                    "tasks_count": len(available_tasks or [])
                }
            }
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            print(f"Error type: {type(e)}")
            import traceback
            traceback.print_exc()
            # Use intelligent fallback
            return self._get_smart_fallback(user_input, available_tasks, energy_level, personality_mode)
    
    async def plan_my_day(
        self,
        user_input: str = "Plan my day",
        available_tasks: List[Dict] = None,
        personality_mode: str = "coach"
    ) -> Dict[str, Any]:
        """
        Generate a daily schedule based on tasks
        """
        
        if not self.client_ready:
            return self._get_day_plan_fallback(available_tasks, personality_mode)
        
        try:
            current_time = datetime.now()
            
            prompt = self._build_day_plan_prompt(user_input, available_tasks, current_time)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are Timely, an AI productivity coach helping users plan their day effectively."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.6
            )
            
            plan_response = response.choices[0].message.content
            
            return {
                "response": plan_response,
                "tokens_used": response.usage.total_tokens,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            print(f"OpenAI API error in day planning: {e}")
            return self._get_day_plan_fallback(available_tasks, personality_mode)
    
    async def morning_checkin(self, energy_level: str = "medium") -> Dict[str, Any]:
        """
        Friendly morning check-in
        """
        
        if not self.client_ready:
            return self._get_morning_fallback(energy_level)
        
        try:
            current_time = datetime.now()
            
            prompt = f"""
Give a warm, energizing morning greeting for someone with {energy_level} energy level.
It's {current_time.strftime('%A morning, %B %d at %I:%M %p')}.

Be encouraging, ask what they'd like to focus on today, and keep it brief but inspiring.
Match their energy level appropriately.
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.8
            )
            
            return {
                "response": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
                "timestamp": current_time.isoformat()
            }
            
        except Exception as e:
            print(f"OpenAI API error in morning check-in: {e}")
            return self._get_morning_fallback(energy_level)
    
    def _build_next_task_prompt(self, user_input, available_tasks, energy_level, personality_mode, current_time):
        """Build prompt for next task suggestion"""
        
        personalities = {
            "coach": "Be encouraging and supportive, like a professional productivity coach",
            "friend": "Be casual and friendly, like a helpful friend", 
            "strict": "Be direct and focused, like an efficient executive assistant",
            "zen": "Be calm and mindful, like a mindfulness teacher"
        }
        
        style = personalities.get(personality_mode, personalities["coach"])
        task_context = self._format_tasks(available_tasks or [])
        
        return f"""
{style}.

USER REQUEST: "{user_input}"

CURRENT CONTEXT:
- Time: {current_time.strftime('%A, %B %d at %I:%M %p')}
- Energy Level: {energy_level}
- Available Tasks: {len(available_tasks or [])}

TASKS:
{task_context}

Suggest ONE specific task they should do next. Consider their energy level and time of day.

FORMAT:
**Next Task:** [Clear task name]
**Why Now:** [Brief reasoning]
**Duration:** [Estimated time]

{self._get_personality_closer(personality_mode)}
"""
    
    def _build_day_plan_prompt(self, user_input, available_tasks, current_time):
        """Build prompt for day planning"""
        
        task_list = self._format_tasks_for_planning(available_tasks or [])
        
        return f"""
Help plan the user's day. It's {current_time.strftime('%A, %B %d at %I:%M %p')}.

AVAILABLE TASKS:
{task_list}

Create a realistic schedule with 4-6 time blocks, considering:
- Current time and remaining day
- Energy levels throughout the day  
- Task complexity and duration
- Natural breaks

FORMAT:
🗓️ **Your Day Plan:**
• [Time] → [Task] ([Duration])
• [Continue pattern]

**Strategy:** [Brief explanation]
Ready to make this day productive! ✨
"""
    
    def _format_tasks(self, tasks: List[Dict]) -> str:
        """Format tasks for display"""
        if not tasks:
            return "No pending tasks available."
        
        formatted = []
        for i, task in enumerate(tasks[:8], 1):
            priority_emoji = {"low": "🔵", "medium": "🟡", "high": "🟠", "urgent": "🔴"}
            emoji = priority_emoji.get(task.get('priority', 'medium'), '⚪')
            
            title = task.get('title', f'Task {i}')
            priority = task.get('priority', 'medium')
            duration = task.get('estimated_duration', 30)
            
            formatted.append(f"{emoji} {title} ({priority} priority, ~{duration}min)")
        
        return "\n".join(formatted)
    
    def _format_tasks_for_planning(self, tasks: List[Dict]) -> str:
        """Format tasks for day planning"""
        if not tasks:
            return "No tasks to schedule."
        
        formatted = []
        for task in tasks[:10]:
            title = task.get('title', 'Untitled Task')
            duration = task.get('estimated_duration', 30)
            priority = task.get('priority', 'medium')
            
            formatted.append(f"• {title} (~{duration}min, {priority} priority)")
        
        return "\n".join(formatted)
    
    def _get_personality_closer(self, personality_mode: str) -> str:
        """Get personality-appropriate closing"""
        closers = {
            "coach": "You've got this! 💪",
            "friend": "Hope this helps! 😊",
            "strict": "Execute immediately.",
            "zen": "Focus on this moment. 🧘"
        }
        return closers.get(personality_mode, "Let's get started! ✨")
    
    def _get_smart_fallback(self, user_input, available_tasks, energy_level, personality_mode):
        """Intelligent fallback when API is unavailable"""
        
        if available_tasks:
            # Find highest priority task
            high_priority_tasks = [t for t in available_tasks if t.get('priority') in ['high', 'urgent']]
            if high_priority_tasks:
                task = high_priority_tasks[0]
                return {
                    "response": f"**Next Task:** {task['title']}\n**Why Now:** This is marked as {task['priority']} priority\n**Duration:** ~{task.get('estimated_duration', 30)} minutes\n\n{self._get_personality_closer(personality_mode)}",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "fallback": True
                }
            
            # Otherwise suggest first task
            task = available_tasks[0]
            return {
                "response": f"**Next Task:** {task['title']}\n**Why Now:** Good starting point for your current energy level\n**Duration:** ~{task.get('estimated_duration', 30)} minutes\n\n{self._get_personality_closer(personality_mode)}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "fallback": True
            }
        
        # No tasks - suggest based on energy
        energy_suggestions = {
            "low": "**Next Task:** Take a 5-10 minute break\n**Why Now:** Recharge before tackling new work\n**Duration:** 10 minutes",
            "medium": "**Next Task:** Review your priorities for today\n**Why Now:** Planning helps focus your energy\n**Duration:** 5 minutes", 
            "high": "**Next Task:** Start your most important project\n**Why Now:** Channel that energy into meaningful work\n**Duration:** 30 minutes"
        }
        
        suggestion = energy_suggestions.get(energy_level, energy_suggestions["medium"])
        return {
            "response": f"{suggestion}\n\n{self._get_personality_closer(personality_mode)}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "fallback": True
        }
    
    def _get_day_plan_fallback(self, available_tasks, personality_mode):
        """Fallback day plan"""
        current_time = datetime.now()
        
        if available_tasks:
            high_priority = [t for t in available_tasks if t.get('priority') in ['high', 'urgent']]
            medium_priority = [t for t in available_tasks if t.get('priority') == 'medium']
            
            plan = "🗓️ **Your Day Plan:**\n"
            
            if high_priority:
                plan += f"• Now → {high_priority[0]['title']} (High priority first)\n"
            
            if medium_priority:
                plan += f"• Mid-morning → {medium_priority[0]['title']} (Good follow-up)\n"
            
            plan += "• After lunch → Quick tasks and admin\n"
            plan += "• Afternoon → Deep work or project time\n"
            
            plan += f"\n**Strategy:** Tackle high-priority items when your energy is fresh.\n{self._get_personality_closer(personality_mode)}"
        else:
            plan = f"""🗓️ **Your Day Plan:**
• Now → Set 3 main priorities for today
• Mid-morning → Focus work block (90 minutes)
• Late morning → Break and quick tasks
• After lunch → Secondary projects
• Afternoon → Wrap up and plan tomorrow

**Strategy:** Structure creates momentum even without a task list.
{self._get_personality_closer(personality_mode)}"""
        
        return {
            "response": plan,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "fallback": True
        }
    
    def _get_morning_fallback(self, energy_level):
        """Fallback morning greeting"""
        energy_greetings = {
            "low": "Good morning! 🌅 Take it gentle today - even small steps count. What would you like to focus on?",
            "medium": "Good morning! ✨ Ready to make today productive? What's your main priority today?",
            "high": "Good morning! 🚀 You seem energized - let's channel that into something great! What exciting project can we tackle?"
        }
        
        greeting = energy_greetings.get(energy_level, "Good morning! 🌅 How can I help you make today great?")
        
        return {
            "response": greeting,
            "timestamp": datetime.now().isoformat(),
            "fallback": True
        }