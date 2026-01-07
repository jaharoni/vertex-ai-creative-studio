# 🎬 Creative Automation Machine - AI Commercial Generator

## Overview
Full-stack AI video generation system that transforms text prompts into complete commercials.

## Architecture

### Core Services
1. **Workflow Orchestrator** (`services/workflows/orchestrator.py`)
   - Uses Gemini 2.5 Pro for intelligent planning
   - Transforms text → structured workflow JSON
   - Shot-by-shot breakdown with cinematography details

2. **Model Selector** (`services/workflows/model_selector.py`)
   - Intelligently chooses optimal models per shot
   - Supports: Veo 3, Kling 2.6, Wan 2.2, Imagen 4
   - Budget modes: economy/balanced/premium

3. **Workflow Executor** (`services/workflows/executor.py`)
   - Async pipeline execution
   - Steps: keyframes → videos → audio → composition
   - Progress callbacks for real-time updates

4. **FFmpeg Composer** (`services/workflows/ffmpeg_service.py`)
   - Video stitching with transitions
   - Color grading and effects
   - Multi-format export (16:9, 9:16, 1:1)

### Models Integrated

**Planning:**
- Gemini 2.5 Pro (thinking mode, most intelligent)

**Image Generation:**
- Imagen 4 Standard (highest quality)
- Imagen 4 Fast ($0.02/image)

**Video Generation:**
- Veo 3: Premium quality, native audio, up to 60s
- Kling 2.6: Best value (~$1.10/min), action scenes, 2min max
- Wan 2.2: Cinematic quality, "film language", 720p

**Audio:**
- Gemini TTS for voiceover
- Lyria 2 for music (upcoming)

## Usage

### 1. Create Workflow from Text Prompt

```python
from services.workflows.orchestrator import WorkflowOrchestrator

orchestrator = WorkflowOrchestrator(
    project_id="your-project",
    location="us-central1"
)

prompt = """
30sec Patagonia ad. Sunrise hike in Yosemite. Lone climber summits Half Dome.
Wes Anderson symmetry meets Planet Earth cinematography. 
Voiceover: whispered poem about solitude.
"""

workflow = orchestrator.create_workflow_from_prompt(prompt)
```

### 2. Get Cost Estimates

```python
from services.workflows.model_selector import ModelSelector

selector = ModelSelector()
recommendations = selector.get_recommendations(workflow)

# Output:
# {
#   'economy': {'cost': {'total': 2.45}, 'description': '...'},
#   'balanced': {'cost': {'total': 4.20}, 'description': '...'},
#   'premium': {'cost': {'total': 7.80}, 'description': '...'}
# }
```

### 3. Execute Workflow

```python
from services.workflows.executor import WorkflowExecutor

executor = WorkflowExecutor(
    project_id="your-project",
    bucket_name="your-bucket"
)

# With progress callback
def progress_callback(stage, status, progress):
    print(f"{stage}: {status} ({progress}%)")

result = await executor.execute_workflow(
    workflow, 
    callback=progress_callback
)

# Result includes:
# - outputs.final_video_url
# - outputs.formats (youtube, tiktok, instagram)
```

## Cost Optimization

### Budget Mode Comparison (30sec, 6 shots)

| Mode | Models Used | Est. Cost | Best For |
|------|------------|-----------|----------|
| Economy | Kling 2.6 + Wan 2.2 | $1-2 | High volume, testing |
| Balanced | Smart selection | $4-5 | Production quality |
| Premium | Veo 3 + Imagen 4 | $6-8 | Client work, audio sync |

### Model Selection Logic

**Veo 3 chosen when:**
- Native audio/dialogue required
- Premium quality requested
- Budget mode = premium

**Kling 2.6 chosen when:**
- Action scenes with movement
- Character consistency needed
- Duration > 60 seconds
- Budget optimization

**Wan 2.2 chosen when:**
- Short cinematic shots (≤5s)
- Aesthetic/"film language" focus
- Economy mode for cinematic content

## Workflow JSON Structure

```json
{
  "workflow_id": "uuid",
  "status": "planned|executing|completed|failed",
  "spec": {
    "duration": 30,
    "shots": [
      {
        "shot_number": 1,
        "time_start": 0,
        "time_end": 5,
        "duration": 5,
        "scene_description": "Wide shot of Yosemite...",
        "camera_movement": "Slow drone pull back",
        "framing": "Wide landscape, rule of thirds",
        "lighting": "Golden hour, rim lighting",
        "mood": "Serene, anticipatory"
      }
    ],
    "audio": {
      "voiceover": {
        "script": "In the quiet before the world wakes...",
        "style": "Whispered, intimate"
      },
      "music": {
        "style": "Ambient minimal piano"
      }
    },
    "style": {
      "visual_keywords": ["symmetrical framing", "muted earth tones"],
      "color_palette": ["warm golds", "deep shadows"],
      "aspect_ratio": "16:9"
    }
  },
  "outputs": {
    "final_video_url": "https://...",
    "formats": {
      "youtube": {"url": "..."},
      "tiktok": {"url": "..."},
      "instagram": {"url": "..."}
    }
  }
}
```

## Next Steps

- [ ] Add functional UI with text prompt interface
- [ ] Implement real-time progress tracking
- [ ] Add job queue for async processing
- [ ] Deploy to Cloud Run
- [ ] Add workflow templates
- [ ] Implement iteration/refinement
- [ ] Add Lyria 2 music generation
- [ ] Build visual node editor

## Testing

See `test_workflow.py` for end-to-end examples.
