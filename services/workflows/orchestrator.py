"""Workflow Orchestrator - Gemini 2.0 as AI Director.

Transforms text prompts into structured video workflows.
"""
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

from vertexai.generative_models import GenerativeModel, GenerationConfig

logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    """Orchestrates AI commercial generation using Gemini 2.0."""
    
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        self.model = GenerativeModel("gemini-2.5-pro")
        
    def create_workflow_from_prompt(self, prompt: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Transform text prompt into structured workflow.
        
        Args:
            prompt: User's creative vision (e.g., "30sec Patagonia ad...")
            user_id: Optional user identifier
            
        Returns:
            Complete workflow specification with shots, audio, style
        """
        logger.info(f"Creating workflow from prompt: {prompt[:100]}...")
        
        # Generate workflow ID
        workflow_id = str(uuid.uuid4())
        
        # Build Gemini prompt for workflow planning
        planning_prompt = self._build_planning_prompt(prompt)
        
        try:
            # Call Gemini 2.0 for intelligent planning
            response = self.model.generate_content(
                planning_prompt,
                generation_config=GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=4096,
                    response_mime_type="application/json"
                )
            )
            
            # Parse Gemini's workflow plan
            workflow_spec = json.loads(response.text)
            
            # Add metadata
            workflow = {
                "workflow_id": workflow_id,
                "user_id": user_id,
                "original_prompt": prompt,
                "created_at": datetime.utcnow().isoformat(),
                "status": "planned",
                "spec": workflow_spec,
                "progress": {
                    "planning": "complete",
                    "keyframes": "pending",
                    "videos": "pending",
                    "audio": "pending",
                    "composition": "pending"
                }
            }
            
            logger.info(f"Workflow {workflow_id} created successfully")
            return workflow
            
        except Exception as e:
            logger.error(f"Failed to create workflow: {e}")
            raise
    
    def _build_planning_prompt(self, user_prompt: str) -> str:
        """Build detailed prompt for Gemini 2.0 workflow planning."""
        return f"""You are an expert AI commercial director. Transform this creative brief into a detailed video production workflow.

CREATIVE BRIEF:
{user_prompt}

Generate a complete workflow specification in JSON format with this structure:

{{
  "duration": <total_seconds>,
  "shots": [
    {{
      "shot_number": 1,
      "time_start": 0,
      "time_end": 5,
      "duration": 5,
      "scene_description": "Wide shot of Yosemite valley at dawn with rising mist",
      "camera_movement": "Slow drone pull back revealing scale",
      "framing": "Wide landscape, rule of thirds",
      "lighting": "Golden hour, rim lighting on peaks",
      "mood": "Serene, anticipatory"
    }}
  ],
  "audio": {{
    "voiceover": {{
      "script": "In the quiet before the world wakes...",
      "style": "Whispered, intimate, contemplative",
      "timing": [
        {{"text": "In the quiet before the world wakes", "start": 2, "end": 6}}
      ]
    }},
    "music": {{
      "style": "Ambient minimal piano with swelling strings",
      "intensity_curve": [[0, 0.3], [15, 0.5], [20, 0.8], [30, 0.4]],
      "key_moments": ["Build at 20s for summit reveal"]
    }}
  }},
  "style": {{
    "visual_keywords": ["symmetrical framing", "muted earth tones", "16mm film grain"],
    "color_palette": ["warm golds", "deep shadows", "muted greens"],
    "references": ["Wes Anderson symmetry", "Planet Earth cinematography"],
    "aspect_ratio": "16:9"
  }},
  "transitions": [
    {{"from_shot": 1, "to_shot": 2, "type": "crossfade", "duration": 0.5}}
  ],
  "brand": {{
    "name": "Patagonia",
    "logo_timing": {{"start": 26, "end": 30}},
    "brand_colors": ["#FF6B35", "#004E89"]
  }}
}}

IMPORTANT GUIDELINES:
- Break down into 5-8 distinct shots
- Each shot should be 3-7 seconds
- Vary camera angles and movements
- Match visual style to brand identity
- Create emotional arc across shots
- Ensure audio complements visuals
- Be specific with cinematography details

Respond ONLY with the JSON object, no additional text.
"""
    
    def refine_shot(self, workflow: Dict[str, Any], shot_number: int, refinement: str) -> Dict[str, Any]:
        """Refine a specific shot based on user feedback.
        
        Args:
            workflow: Existing workflow specification
            shot_number: Which shot to refine (1-indexed)
            refinement: User's feedback (e.g., "make it more cinematic")
            
        Returns:
            Updated workflow with refined shot
        """
        logger.info(f"Refining shot {shot_number}: {refinement}")
        
        original_shot = workflow['spec']['shots'][shot_number - 1]
        
        refinement_prompt = f"""Refine this shot based on director's note.

ORIGINAL SHOT:
{json.dumps(original_shot, indent=2)}

DIRECTOR'S NOTE:
"{refinement}"

Generate an improved version of this shot. Maintain the same duration and general scene, but enhance based on the feedback. Return ONLY the updated shot JSON object.
"""
        
        try:
            response = self.model.generate_content(
                refinement_prompt,
                generation_config=GenerationConfig(
                    temperature=0.8,
                    response_mime_type="application/json"
                )
            )
            
            refined_shot = json.loads(response.text)
            workflow['spec']['shots'][shot_number - 1] = refined_shot
            workflow['updated_at'] = datetime.utcnow().isoformat()
            
            logger.info(f"Shot {shot_number} refined successfully")
            return workflow
            
        except Exception as e:
            logger.error(f"Failed to refine shot: {e}")
            raise
