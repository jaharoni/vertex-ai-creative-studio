"""FFmpeg Composer - Video composition and editing service."""
import asyncio
import logging
import subprocess
import tempfile
import os
from typing import Dict, Any, List
from pathlib import Path

logger = logging.getLogger(__name__)


class FFmpegComposer:
    """Composes final videos using FFmpeg."""
    
    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir()) / 'workflow_composer'
        self.temp_dir.mkdir(exist_ok=True)
    
    async def compose(
        self, 
        video_clips: List[str],
        audio_tracks: List[str],
        transitions: List[Dict[str, Any]],
        style: Dict[str, Any]
    ) -> str:
        """Compose final video from clips and audio.
        
        Args:
            video_clips: List of GCS URIs for video clips
            audio_tracks: List of GCS URIs for audio tracks
            transitions: List of transition specs
            style: Style configuration (color grading, effects)
            
        Returns:
            Path to composed video file
        """
        logger.info(f"Composing video from {len(video_clips)} clips")
        
        # Download all assets
        local_videos = await self._download_assets(video_clips)
        local_audio = await self._download_assets(audio_tracks) if audio_tracks else []
        
        # Build FFmpeg filter chain
        filter_complex = self._build_filter_chain(
            len(local_videos),
            transitions,
            style
        )
        
        # Output file
        output_path = self.temp_dir / f"composed_{os.urandom(8).hex()}.mp4"
        
        # Build FFmpeg command
        cmd = ['ffmpeg', '-y']
        
        # Add video inputs
        for video in local_videos:
            cmd.extend(['-i', video])
        
        # Add audio inputs
        for audio in local_audio:
            cmd.extend(['-i', audio])
        
        # Apply filter complex
        cmd.extend(['-filter_complex', filter_complex])
        
        # Output settings
        cmd.extend([
            '-map', '[outv]',  # Use processed video
            '-c:v', 'libx264',  # H.264 codec
            '-preset', 'medium',
            '-crf', '23',  # Quality
            '-pix_fmt', 'yuv420p',  # Compatibility
        ])
        
        # Add audio mix if present
        if local_audio:
            cmd.extend([
                '-map', '[outa]',  # Use mixed audio
                '-c:a', 'aac',
                '-b:a', '192k'
            ])
        
        cmd.append(str(output_path))
        
        # Execute FFmpeg
        logger.info(f"Running FFmpeg: {' '.join(cmd[:10])}...")
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            logger.error(f"FFmpeg failed: {stderr.decode()}")
            raise RuntimeError(f"Video composition failed: {stderr.decode()[:500]}")
        
        logger.info(f"Video composed successfully: {output_path}")
        return str(output_path)
    
    async def transcode(
        self,
        input_video: str,
        aspect_ratio: str,
        resolution: str
    ) -> str:
        """Transcode video to different format/resolution.
        
        Args:
            input_video: GCS URI or local path
            aspect_ratio: Target aspect ratio (e.g., '16:9', '9:16', '1:1')
            resolution: Target resolution (e.g., '1920x1080')
            
        Returns:
            Path to transcoded video
        """
        logger.info(f"Transcoding to {aspect_ratio} @ {resolution}")
        
        # Download if GCS URI
        if input_video.startswith('gs://'):
            local_input = (await self._download_assets([input_video]))[0]
        else:
            local_input = input_video
        
        output_path = self.temp_dir / f"transcoded_{aspect_ratio.replace(':', 'x')}_{os.urandom(4).hex()}.mp4"
        
        # Parse resolution
        width, height = map(int, resolution.split('x'))
        
        # Build crop/scale filter based on aspect ratio
        if aspect_ratio == '1:1':
            # Square - crop to center square
            scale_filter = f"scale={width}:{width}:force_original_aspect_ratio=increase,crop={width}:{height}"
        elif aspect_ratio == '9:16':
            # Portrait
            scale_filter = f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height}"
        else:  # 16:9 or other
            scale_filter = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2"
        
        cmd = [
            'ffmpeg', '-y',
            '-i', local_input,
            '-vf', scale_filter,
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'copy',  # Copy audio
            str(output_path)
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        await process.communicate()
        
        if process.returncode != 0:
            raise RuntimeError("Video transcoding failed")
        
        return str(output_path)
    
    def _build_filter_chain(
        self,
        num_clips: int,
        transitions: List[Dict[str, Any]],
        style: Dict[str, Any]
    ) -> str:
        """Build FFmpeg filter_complex string."""
        filters = []
        
        # Apply style to each clip
        for i in range(num_clips):
            clip_filter = f"[{i}:v]"
            
            # Apply color grading if specified
            if 'color_palette' in style:
                # Simple color adjustment
                clip_filter += "eq=contrast=1.1:brightness=0.05:saturation=1.2,"
            
            # Apply film grain if specified
            if 'film_grain' in style.get('visual_keywords', []):
                clip_filter += "noise=alls=10:allf=t,"
            
            # Finish clip processing
            clip_filter += f"format=yuv420p[v{i}]"
            filters.append(clip_filter)
        
        # Concatenate clips with transitions
        if len(transitions) > 0 and num_clips > 1:
            # Use xfade for crossfades
            concat_str = "[v0]"
            for i, trans in enumerate(transitions):
                if i < num_clips - 1:
                    trans_type = trans.get('type', 'fade')
                    duration = trans.get('duration', 0.5)
                    concat_str += f"[v{i+1}]xfade=transition={trans_type}:duration={duration}:offset=0"
            concat_str += "[outv]"
            filters.append(concat_str)
        else:
            # Simple concatenation
            concat_inputs = "".join([f"[v{i}]" for i in range(num_clips)])
            filters.append(f"{concat_inputs}concat=n={num_clips}:v=1:a=0[outv]")
        
        # Mix audio if present
        if num_clips > 0:
            # Assuming audio starts after video inputs
            audio_inputs = "".join([f"[{num_clips + i}:a]" for i in range(2)])  # voiceover + music
            if audio_inputs:
                filters.append(f"{audio_inputs}amix=inputs=2:duration=longest[outa]")
        
        return ";".join(filters)
    
    async def _download_assets(self, uris: List[str]) -> List[str]:
        """Download assets from GCS to local temp."""
        local_paths = []
        
        for uri in uris:
            if uri.startswith('gs://'):
                # Extract bucket and path
                parts = uri.replace('gs://', '').split('/', 1)
                bucket_name = parts[0]
                blob_path = parts[1]
                
                # Local path
                local_path = self.temp_dir / Path(blob_path).name
                
                # Download using gsutil
                cmd = ['gsutil', 'cp', uri, str(local_path)]
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                await process.communicate()
                
                local_paths.append(str(local_path))
            else:
                local_paths.append(uri)
        
        return local_paths
