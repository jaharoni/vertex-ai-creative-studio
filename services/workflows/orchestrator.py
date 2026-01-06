# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

"""Workflow Orchestrator - The Big Brain that plans creative workflows."""

import json
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional

from vertexai.generative_models import GenerativeModel
from config.default import Default as cfg
from config.firebase_config import FirebaseClient
from common.analytics import get_logger

logger = get_logger(__name__)
db = FirebaseClient().get_client()


class WorkflowOrchestrator:
    """Orchestrates AI-powered creative workflow generation."""
    
    def __init__(self):
        self.config = cfg()
        self.model = GenerativeModel(self.config.MODEL_ID)
    
    async def create_workflow_from_prompt(self, prompt: str, user_email: str) -> Dict:
        """
        Takes a natural language prompt and generates a structured workflow.
        
        Args:
            prompt: User's creative vision (e.g., "30sec Nike ad, Brooklyn, golden hour")
            user_email: User identifier
            
        Returns:
            Dict containing workflow_id and initial workflow structure
        """
        logger.info(f"Creating workflow from prompt: {prompt[:100]}...")
        
        # Generate workflow plan using Gemini
        workflow_plan = await self._generate_workflow_plan(prompt)
        
        # Create workflow document in Firestore
        workflow_id = str(uuid.uuid4())
        workflow_doc = {
            "id": workflow_id,
            "user_email": user_email,
            "original_prompt": prompt,
            "status": "planning",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "plan": workflow_plan,
            "execution_log": [],
            "outputs": {}
        }
        
        # Save to Firestore
        db.collection("workflows").document(workflow_id).set(workflow_doc)
        
        logger.info(f"Workflow created: {workflow_id}")
        return {
            "workflow_id": workflow_id,
            "plan": workflow_plan,
            "status": "planning"
        }
    
    async def _generate_workflow_plan(self, prompt: str) -> Dict:
        """
        Uses Gemini to analyze the prompt and create a structured plan.
        """
        system_prompt = """
You are a creative director AI. Analyze the user's vision and create a detailed workflow.

Output a JSON structure with:
- duration: total seconds
- shots: array of {time_range, scene_description, camera_movement, style_notes}
- audio: {voiceover_script, music_description, sound_effects}
- style_keywords: array of visual style descriptors
- brand_voice: tone and messaging guidelines

Be specific and cinematic. Think like a director.
"""
        
        full_prompt = f"{system_prompt}\n\nUser Vision: {prompt}"
        
        response = self.model.generate_content(
            full_prompt,
            generation_config={
                "temperature": 0.7,
                "response_mime_type": "application/json"
            }
        )
        
        plan = json.loads(response.text)
        return plan

