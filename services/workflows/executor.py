"""Workflow Executor - Runs the AI commercial generation pipeline.

Executes each step: keyframes → videos → audio → composition
"""
import asyncio
import logging
from typing import Dict, Any, List, Optional
import os
from datetime import datetime

from google.cloud import storage
from services import imagen, veo, gemini_tts
from services.workflows.ffmpeg_service import FFmpegComposer

logger = logging.getLogger(__name__)


class WorkflowExecutor:
    """Executes AI commercial generation workflows."""
    
    def __init__(self, project_id: str, bucket_name: str):
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(bucket_name)
        self.ffmpeg = FFmpegComposer()
        
    async def execute_workflow(self, workflow: Dict[str, Any], callback=None) -> Dict[str, Any]:
        """Execute complete workflow pipeline.
        
        Args:
            workflow: Workflow specification from orchestrator
            callback: Optional callback for progress updates
            
        Returns:
            Updated workflow with output URLs
        """
        workflow_id = workflow['workflow_id']
        logger.info(f"Executing workflow {workflow_id}")
        
        try:
            # Step 1: Generate keyframes for each shot
            workflow = await self._generate_keyframes(workflow, callback)
            
            # Step 2: Generate videos from keyframes
            workflow = await self._generate_videos(workflow, callback)
            
            # Step 3: Generate audio (voiceover + music)
            workflow = await self._generate_audio(workflow, callback)
            
            # Step 4: Compose final video
            workflow = await self._compose_final_video(workflow, callback)
            
            # Step 5: Export multiple formats
            workflow = await self._export_formats(workflow, callback)
            
            workflow['status'] = 'completed'
            workflow['completed_at'] = datetime.utcnow().isoformat()
            
            logger.info(f"Workflow {workflow_id} completed successfully")
            return workflow
            
        except Exception as e:
            logger.error(f"Workflow {workflow_id} failed: {e}")
            workflow['status'] = 'failed'
            workflow['error'] = str(e)
            raise
    
    async def _generate_keyframes(self, workflow: Dict[str, Any], callback=None) -> Dict[str, Any]:
        """Generate Imagen keyframes for each shot."""
        workflow_id = workflow['workflow_id']
        shots = workflow['spec']['shots']
        style = workflow['spec']['style']
        
        logger.info(f"Generating {len(shots)} keyframes for workflow {workflow_id}")
        
        if callback:
            callback('keyframes', 'started', 0)
        
        keyframe_tasks = []
        for i, shot in enumerate(shots):
            # Build Imagen prompt from shot spec
            prompt = self._build_imagen_prompt(shot, style)
            
            # Generate keyframe
            task = imagen.generate_image(
                prompt=prompt,
                aspect_ratio=style.get('aspect_ratio', '16:9'),
                model="imagen-004"
            )
            keyframe_tasks.append((i, task))
        
        # Execute keyframe generation in parallel
        results = await asyncio.gather(*[t for _, t in keyframe_tasks])
        
        # Upload keyframes and update workflow
        for i, result in enumerate(results):
            keyframe_path = f"workflows/{workflow_id}/keyframes/shot_{i+1}.png"
            blob = self.bucket.blob(keyframe_path)
            blob.upload_from_string(result['image_bytes'], content_type='image/png')
            
            shots[i]['keyframe_uri'] = f"gs://{self.bucket_name}/{keyframe_path}"
            
            if callback:
                progress = int((i + 1) / len(shots) * 100)
                callback('keyframes', 'progress', progress)
        
        workflow['progress']['keyframes'] = 'complete'
        if callback:
            callback('keyframes', 'complete', 100)
        
        logger.info(f"Keyframes generated for workflow {workflow_id}")
        return workflow
    
    async def _generate_videos(self, workflow: Dict[str, Any], callback=None) -> Dict[str, Any]:
        """Generate Veo videos from keyframes."""
        workflow_id = workflow['workflow_id']
        shots = workflow['spec']['shots']
        
        logger.info(f"Generating {len(shots)} videos for workflow {workflow_id}")
        
        if callback:
            callback('videos', 'started', 0)
        
        # Generate videos sequentially (Veo has rate limits)
        for i, shot in enumerate(shots):
            # Build Veo prompt
            prompt = f"{shot['scene_description']}. {shot['camera_movement']}. {shot['lighting']}."
            
            # Generate video from keyframe
            result = await veo.generate_video(
                prompt=prompt,
                image_uri=shot['keyframe_uri'],
                duration=shot['duration'],
                model="veo-003"
            )
            
            # Upload video
            video_path = f"workflows/{workflow_id}/videos/shot_{i+1}.mp4"
            blob = self.bucket.blob(video_path)
            blob.upload_from_string(result['video_bytes'], content_type='video/mp4')
            
            shots[i]['video_uri'] = f"gs://{self.bucket_name}/{video_path}"
            
            if callback:
                progress = int((i + 1) / len(shots) * 100)
                callback('videos', 'progress', progress)
            
            # Veo rate limiting - wait between shots
            await asyncio.sleep(2)
        
        workflow['progress']['videos'] = 'complete'
        if callback:
            callback('videos', 'complete', 100)
        
        logger.info(f"Videos generated for workflow {workflow_id}")
        return workflow
    
    async def _generate_audio(self, workflow: Dict[str, Any], callback=None) -> Dict[str, Any]:
        """Generate voiceover and music."""
        workflow_id = workflow['workflow_id']
        audio_spec = workflow['spec']['audio']
        
        logger.info(f"Generating audio for workflow {workflow_id}")
        
        if callback:
            callback('audio', 'started', 0)
        
        # Generate voiceover using Gemini TTS
        if 'voiceover' in audio_spec:
            voiceover_script = audio_spec['voiceover']['script']
            voiceover_style = audio_spec['voiceover'].get('style', 'neutral')
            
            voiceover_result = await gemini_tts.generate_speech(
                text=voiceover_script,
                voice_style=voiceover_style
            )
            
            voiceover_path = f"workflows/{workflow_id}/audio/voiceover.mp3"
            blob = self.bucket.blob(voiceover_path)
            blob.upload_from_string(voiceover_result['audio_bytes'], content_type='audio/mpeg')
            
            audio_spec['voiceover']['audio_uri'] = f"gs://{self.bucket_name}/{voiceover_path}"
        
        if callback:
            callback('audio', 'progress', 50)
        
        # TODO: Generate background music using Lyria (when available)
        # For now, use placeholder or stock music
        if 'music' in audio_spec:
            # Placeholder music generation
            music_path = f"workflows/{workflow_id}/audio/music.mp3"
            audio_spec['music']['audio_uri'] = f"gs://{self.bucket_name}/{music_path}"
        
        workflow['progress']['audio'] = 'complete'
        if callback:
            callback('audio', 'complete', 100)
        
        logger.info(f"Audio generated for workflow {workflow_id}")
        return workflow
    
    async def _compose_final_video(self, workflow: Dict[str, Any], callback=None) -> Dict[str, Any]:
        """Compose final video using FFmpeg."""
        workflow_id = workflow['workflow_id']
        
        logger.info(f"Composing final video for workflow {workflow_id}")
        
        if callback:
            callback('composition', 'started', 0)
        
        # Download all assets
        shots = workflow['spec']['shots']
        audio_spec = workflow['spec']['audio']
        
        video_clips = [shot['video_uri'] for shot in shots]
        audio_tracks = []
        
        if 'voiceover' in audio_spec and 'audio_uri' in audio_spec['voiceover']:
            audio_tracks.append(audio_spec['voiceover']['audio_uri'])
        if 'music' in audio_spec and 'audio_uri' in audio_spec['music']:
            audio_tracks.append(audio_spec['music']['audio_uri'])
        
        # Compose using FFmpeg
        composed_video = await self.ffmpeg.compose(
            video_clips=video_clips,
            audio_tracks=audio_tracks,
            transitions=workflow['spec'].get('transitions', []),
            style=workflow['spec']['style']
        )
        
        # Upload composed video
        final_path = f"workflows/{workflow_id}/final/commercial.mp4"
        blob = self.bucket.blob(final_path)
        blob.upload_from_filename(composed_video)
        
        workflow['outputs'] = {
            'final_video_uri': f"gs://{self.bucket_name}/{final_path}",
            'final_video_url': blob.public_url
        }
        
        workflow['progress']['composition'] = 'complete'
        if callback:
            callback('composition', 'complete', 100)
        
        logger.info(f"Final video composed for workflow {workflow_id}")
        return workflow
    
    async def _export_formats(self, workflow: Dict[str, Any], callback=None) -> Dict[str, Any]:
        """Export to multiple formats (16:9, 9:16, 1:1)."""
        workflow_id = workflow['workflow_id']
        final_video_path = workflow['outputs']['final_video_uri']
        
        logger.info(f"Exporting formats for workflow {workflow_id}")
        
        formats = [
            {'name': 'youtube', 'aspect': '16:9', 'resolution': '1920x1080'},
            {'name': 'tiktok', 'aspect': '9:16', 'resolution': '1080x1920'},
            {'name': 'instagram', 'aspect': '1:1', 'resolution': '1080x1080'}
        ]
        
        format_outputs = {}
        for fmt in formats:
            output_path = await self.ffmpeg.transcode(
                input_video=final_video_path,
                aspect_ratio=fmt['aspect'],
                resolution=fmt['resolution']
            )
            
            export_path = f"workflows/{workflow_id}/exports/{fmt['name']}.mp4"
            blob = self.bucket.blob(export_path)
            blob.upload_from_filename(output_path)
            
            format_outputs[fmt['name']] = {
                'uri': f"gs://{self.bucket_name}/{export_path}",
                'url': blob.public_url
            }
        
        workflow['outputs']['formats'] = format_outputs
        
        logger.info(f"Formats exported for workflow {workflow_id}")
        return workflow
    
    def _build_imagen_prompt(self, shot: Dict[str, Any], style: Dict[str, Any]) -> str:
        """Build Imagen prompt from shot specification."""
        prompt_parts = [
            shot['scene_description'],
            f"Framing: {shot['framing']}",
            f"Lighting: {shot['lighting']}",
            f"Mood: {shot['mood']}",
        ]
        
        # Add style keywords
        if 'visual_keywords' in style:
            prompt_parts.append(f"Style: {', '.join(style['visual_keywords'])}")
        
        # Add color palette
        if 'color_palette' in style:
            prompt_parts.append(f"Colors: {', '.join(style['color_palette'])}")
        
        prompt = ". ".join(prompt_parts)
        prompt += ". Cinematic still frame, high quality, professional cinematography."
        
        return prompt
