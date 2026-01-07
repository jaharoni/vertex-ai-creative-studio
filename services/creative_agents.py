# Copyright 2025 Google LLC

import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass
from vertexai.generative_models import GenerativeModel
import logging

logger = logging.getLogger(__name__)

@dataclass
class AgentConfig:
    """Configuration for a creative agent."""
    name: str
    description: str
    avatar_style: str
    system_prompt: str
    capabilities: List[str]
    quick_actions: List[str]

class CreativeAgent:
    """A specialized creative AI agent."""
    
    def __init__(self, config: AgentConfig, project_id: str):
        self.config = config
        self.project_id = project_id
        # Use Gemini 2.0 Flash Thinking for advanced reasoning
        self.gemini = GenerativeModel("gemini-2.0-flash-thinking-exp-01-21")
        self.conversation_history = []
        
    async def chat(self, user_message: str, context: Optional[Dict] = None) -> Dict:
        """Chat with the agent."""
        
        # Build conversation context
        messages = [{
            "role": "system",
            "content": self.config.system_prompt
        }]
        
        # Add conversation history
        messages.extend(self.conversation_history)
        
        # Add user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Generate response
        full_prompt = f"{self.config.system_prompt}\n\nUser: {user_message}"
        response = await asyncio.to_thread(
            self.gemini.generate_content,
            full_prompt
        )
        
        # Store in conversation history
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": response.text})
        
        return {
            "response": response.text,
            "agent": self.config.name,
            "capabilities_used": self.config.capabilities
        }

class AgentRegistry:
    """Registry of specialized creative agents."""
    
    AGENTS = {
        "director": AgentConfig(
            name="Creative Director Agent",
            description="Expert at transforming ideas into cinematic visions with Gemini Director AI",
            avatar_style="director",
            system_prompt="""
You are a professional creative director and cinematographer.
Transform user concepts into detailed cinematic visions.
Provide:
- Enhanced visual descriptions with cinematography details
- Shot composition and camera movements
- Lighting and color palette
- Pacing and emotional beats
- Audio/music direction
Be creative, bold, and cinematic in your vision.
""",
            capabilities=["concept_enhancement", "cinematography", "storyboarding"],
            quick_actions=[
                "Create a cinematic trailer concept",
                "Design an epic product reveal",
                "Build a dramatic story arc"
            ]
        ),
        
        "video_producer": AgentConfig(
            name="Video Production Agent",
            description="Generates short-form videos using Veo 2, Kling 2.6, and Wan models",
            avatar_style="producer",
            system_prompt="""
You are an expert video producer specializing in AI-generated content.
Help users create stunning videos using:
- Veo 2 for Google's latest video generation
- Kling 2.6 Pro for motion control and native audio
- Wan 2.6 for multi-shot narrative videos

Guide users on:
- Best prompts for each model
- Aspect ratios and duration
- Style and motion control
- When to use image-to-video vs text-to-video
""",
            capabilities=["veo_generation", "kling_generation", "wan_generation"],
            quick_actions=[
                "Generate a 5-second product demo",
                "Create a smooth transition video",
                "Make a cinematic reveal animation"
            ]
        ),
        
        "image_artist": AgentConfig(
            name="Visual Artist Agent",
            description="Creates stunning images and key frames with Imagen 3",
            avatar_style="artist",
            system_prompt="""
You are a master visual artist and concept designer.
Create compelling image prompts for Imagen 3 that result in:
- Stunning, high-quality visuals
- Consistent style and aesthetics  
- Perfect composition and lighting
- Cinematic framing

Provide detailed prompts that specify:
- Subject and composition
- Lighting and atmosphere
- Color palette and mood
- Camera angle and framing
- Style references
""",
            capabilities=["imagen_generation", "style_design", "composition"],
            quick_actions=[
                "Design a hero image for my brand",
                "Create concept art for a scene",
                "Generate a mood board"
            ]
        ),
        
        "audio_engineer": AgentConfig(
            name="Audio Engineer Agent",
            description="Crafts perfect soundscapes with Gemini TTS, Chirp, and audio mixing",
            avatar_style="audio",
            system_prompt="""
You are a professional audio engineer and sound designer.
Help users create perfect audio for their videos:
- Voiceovers using Gemini TTS
- Background music selection and generation
- Sound effects and foley
- Audio mixing and mastering
- Lip-sync and timing

Provide guidance on:
- Voice tone and delivery
- Music genre and mood
- Sound effect placement
- Audio levels and balance
""",
            capabilities=["tts_generation", "music_selection", "audio_mixing"],
            quick_actions=[
                "Create a dramatic voiceover",
                "Find the perfect background music",
                "Add cinematic sound effects"
            ]
        ),
        
        "workflow_architect": AgentConfig(
            name="Workflow Architect Agent",
            description="Designs and orchestrates complex multi-step creative workflows",
            avatar_style="architect",
            system_prompt="""
You are a workflow architect specializing in creative automation.
Help users design end-to-end workflows that combine:
- Multiple AI models (Gemini, Imagen, Veo, Kling, Wan)
- Sequential and parallel processing
- Conditional logic and branching
- Error handling and retries
- Quality control and validation

Break down complex creative projects into:
- Clear workflow steps
- Model selection rationale
- Dependencies and timing
- Resource optimization
""",
            capabilities=["workflow_design", "orchestration", "optimization"],
            quick_actions=[
                "Design a complete video production pipeline",
                "Create a multi-variant content generator",
                "Build an automated campaign system"
            ]
        )
    }
    
    @classmethod
    def get_agent(cls, agent_type: str, project_id: str) -> CreativeAgent:
        """Get an agent by type."""
        config = cls.AGENTS.get(agent_type)
        if not config:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return CreativeAgent(config, project_id)
    
    @classmethod
    def list_agents(cls) -> List[Dict]:
        """List all available agents."""
        return [
            {
                "id": agent_id,
                "name": config.name,
                "description": config.description,
                "capabilities": config.capabilities,
                "quick_actions": config.quick_actions
            }
            for agent_id, config in cls.AGENTS.items()
        ]
