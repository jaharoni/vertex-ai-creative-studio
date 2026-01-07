# 🎬 Creative Workflow Automation - MVP Phase 1

## What We Built Today

A **text-to-video AI orchestration system** that transforms natural language prompts into structured creative workflows.

## System Architecture

```
┌─────────────────────────────────────────────────┐
│  USER TYPES PROMPT                              │
│  "30sec Nike ad, Brooklyn, golden hour..."      │
└──────────────┬──────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────┐
│  WORKFLOW ORCHESTRATOR (Gemini 2.0)              │
│  - Analyzes creative vision                      │
│  - Generates structured plan:                    │
│    • Shot list (6 scenes with timing)            │
│    • Camera movements & framing                  │
│    • Audio (voiceover script + music)            │
│    • Style keywords                              │
└──────────────┬───────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────┐
│  FIRESTORE (Workflow Storage)                    │
│  workflows/{id}                                  │
│    - original_prompt                             │
│    - plan (JSON structure)                       │
│    - status: "planning" → "executing" → "done"   │
│    - outputs: {video_uri, metadata}              │
└──────────────────────────────────────────────────┘
```

## Files Created

### 1. `services/workflows/orchestrator.py`
**The Big Brain** - AI-powered workflow planning service

- **`WorkflowOrchestrator` class**
  - `create_workflow_from_prompt()` - Entry point
  - `_generate_workflow_plan()` - Gemini JSON generation
- **Gemini Integration**
  - Uses `response_mime_type="application/json"`
  - Temperature: 0.7 (creative but structured)
- **Firestore Integration**
  - Stores workflows in `workflows/` collection
  - UUID-based workflow IDs

### 2. `pages/workflow_create.py`
**The UI** - User interface for creative prompts

- **Mesop Components**
  - Large textarea for creative vision input
  - "Generate Workflow" button
  - Example prompts (Patagonia, Coca-Cola, UGC)
  - Status messages & error handling
- **State Management**
  - `WorkflowPageState` dataclass
  - Real-time loading states
- **Navigation**
  - After workflow creation → `/workflow/status?id={workflow_id}`

### 3. `services/workflows/__init__.py`
Python package initialization

## What Happens When User Clicks "Generate"

1. **User types**: "30sec Nike ad, Brooklyn basketball, golden hour"
2. **Orchestrator receives** prompt + user_email
3. **Gemini analyzes** and returns JSON:
   ```json
   {
     "duration": 30,
     "shots": [
       {"time_range": "0-5s", "scene": "Wide: Brooklyn court at sunset", "camera": "drone pullback"},
       {"time_range": "5-12s", "scene": "Close: Ball bouncing, chalk dust", "camera": "slow-mo 120fps"},
       ...
     ],
     "audio": {
       "voiceover": "Every legend starts on the blacktop...",
       "music": "Hip-hop beat, 90bpm, gritty bass"
     },
     "style_keywords": ["cinematic", "golden hour", "street", "authentic"]
   }
   ```
4. **Firestore stores** workflow document with UUID
5. **UI navigates** to status page (to be built in Phase 2)

## Current Branch

```bash
git branch
* feature/creative-workflows
```

## Commit

```
feat: Add workflow orchestration system - MVP Phase 1

- Created WorkflowOrchestrator service for AI-powered workflow planning
- Created /workflow/create UI page with Mesop
- Gemini analyzes creative prompts and generates structured workflows
- Stores workflow plans in Firestore
- Ready for Phase 2: Executor implementation
```

## Next Steps (Phase 2)

### Immediate Next Files to Create:

1. **`services/workflows/executor.py`**
   - Execute the generated workflow plan
   - Generate key frames with Imagen 3
   - Generate video clips with Veo 2
   - Generate audio with TTS
   - Stitch everything with FFmpeg

2. **`pages/workflow_status.py`**
   - Real-time progress tracking
   - Show which step is executing
   - Progress bar
   - Preview thumbnails

3. **`services/workflows/ffmpeg_service.py`**
   - Video composition
   - Transitions & effects
   - Audio mixing
   - Multi-format export

## Testing Locally

```bash
# In Cloud Shell
cd ~/vertex-ai-creative-studio
python main.py

# Visit:
https://[CLOUD_SHELL_URL]/workflow/create
```

## Deploy to Cloud Run

```bash
# Build & deploy
gcloud builds submit --config cloudbuild.yaml

# New URL will include /workflow/create route
```

## Cost Estimate Per Workflow

- **Gemini planning**: $0.01
- **Imagen keyframes (6)**: $1.20
- **Veo videos (6 × 5sec)**: $4.80
- **TTS voiceover**: $0.05
- **FFmpeg (free)**

**Total: ~$6-8 per 30sec commercial**

## The Vision

User types one sentence → AI creates a full commercial in 5 minutes.

That's what we're building. 🚀

