from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

from llm.agents.assistant import TimelyAssistant

router = APIRouter(prefix="/chat", tags=["chat"])

# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    energy_level: Optional[str] = "medium"
    personality_mode: Optional[str] = "coach"
    tasks: Optional[List[Dict[str, Any]]] = []

class ChatResponse(BaseModel):
    response: str
    tokens_used: Optional[int] = None
    timestamp: str
    context_used: Optional[Dict[str, Any]] = None
    fallback: Optional[bool] = False

class QuickTask(BaseModel):
    title: str
    priority: Optional[str] = "medium"
    estimated_duration: Optional[int] = 30
    category: Optional[str] = "general"

# Note: Using fresh assistant instances for each request to ensure latest configuration

@router.post("/next-task", response_model=ChatResponse)
async def get_next_task(request: ChatRequest):
    """
    Get AI suggestion for what to do next
    """
    try:
        # Create fresh assistant instance for latest configuration
        assistant = TimelyAssistant()
        
        result = await assistant.what_should_i_do_next(
            user_input=request.message,
            available_tasks=request.tasks,
            energy_level=request.energy_level,
            personality_mode=request.personality_mode
        )
        
        return ChatResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting task suggestion: {str(e)}"
        )

@router.post("/plan-day", response_model=ChatResponse)
async def plan_day(request: ChatRequest):
    """
    Generate a day plan based on available tasks
    """
    try:
        # Create fresh assistant instance for latest configuration
        assistant = TimelyAssistant()
        
        result = await assistant.plan_my_day(
            user_input=request.message,
            available_tasks=request.tasks,
            personality_mode=request.personality_mode
        )
        
        return ChatResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating day plan: {str(e)}"
        )

@router.post("/morning-checkin", response_model=ChatResponse)
async def morning_checkin(request: ChatRequest):
    """
    Morning greeting and check-in
    """
    try:
        # Create fresh assistant instance for latest configuration
        assistant = TimelyAssistant()
        
        result = await assistant.morning_checkin(
            energy_level=request.energy_level
        )
        
        return ChatResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error with morning check-in: {str(e)}"
        )

@router.get("/test")
async def test_ai():
    """
    Simple test endpoint to verify AI integration
    """
    try:
        # Test with a simple task list
        test_tasks = [
            {"title": "Review emails", "priority": "medium", "estimated_duration": 15},
            {"title": "Write project proposal", "priority": "high", "estimated_duration": 60},
            {"title": "Team meeting", "priority": "high", "estimated_duration": 30}
        ]
        
        # Create fresh assistant instance for latest configuration
        assistant = TimelyAssistant()
        
        result = await assistant.what_should_i_do_next(
            user_input="What should I focus on right now?",
            available_tasks=test_tasks,
            energy_level="medium",
            personality_mode="coach"
        )
        
        return {
            "message": "✅ AI integration working!",
            "test_result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI test failed: {str(e)}"
        )

@router.get("/test-fresh")
async def test_fresh_ai():
    """
    Test endpoint that creates a fresh assistant instance
    """
    try:
        # Create a fresh assistant
        fresh_assistant = TimelyAssistant()
        
        # Simple test message
        from openai import OpenAI
        from backend.core.config import settings
        
        # Test direct OpenAI call
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say hello!"}],
            max_tokens=10
        )
        
        return {
            "message": "✅ Direct OpenAI test working!",
            "response": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens,
            "assistant_ready": fresh_assistant.client_ready,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fresh AI test failed: {str(e)}"
        )

# Add a simple tasks endpoint for testing
@router.post("/quick-task")
async def add_quick_task(task: QuickTask):
    """
    Quick endpoint to add a task (for testing)
    """
    return {
        "message": f"Task '{task.title}' noted!",
        "task": task.dict(),
        "timestamp": datetime.now().isoformat()
    }