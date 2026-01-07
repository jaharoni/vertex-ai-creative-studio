import mesop as me
import mesop.labs as mel

@me.stateclass
class State:
    prompt: str = ""
    duration: int = 30
    style: str = "cinematic"
    video_model: str = "veo2"
    job_id: str = ""
    status: str = ""
    
@me.page(
    path="/workflow-create",
    title="Creative Automation Machine",
)
def page():
    state = me.state(State)
    
    with me.box(style=me.Style(
        display="flex",
        flex_direction="column",
        gap=24,
        padding=me.Padding.all(24),
        max_width=1200,
        margin=me.Margin.symmetric(horizontal="auto"),
    )):
        # Header
        me.text(
            "🎬 Creative Automation Machine",
            type="headline-3",
        )
        me.text(
            "Transform your ideas into video with AI - Powered by Gemini 2.5 Pro, Veo 2, Kling & Wan",
            type="body-1",
            style=me.Style(color="#888"),
        )
        
        # Main input area
        with me.box(style=me.Style(
            background="#1a1a2e",
            padding=me.Padding.all(24),
            border_radius=12,
            margin=me.Margin(top=24),
        )):
            me.text(
                "📝 Describe Your Video",
                type="headline-5",
            )
            
            me.textarea(
                label="Video Concept",
                value=state.prompt,
                on_blur=on_prompt_change,
                rows=6,
                placeholder="Example: A 30-second commercial for eco-friendly shoes. Opens with sunrise over a forest, shows athletes running on trails, close-ups of sustainable materials, ends with brand logo.",
                style=me.Style(
                    width="100%",
                    margin=me.Margin(top=12),
                ),
            )
            
            # Settings row
            with me.box(style=me.Style(
                display="flex",
                gap=16,
                margin=me.Margin(top=24),
                flex_wrap="wrap",
            )):
                with me.box(style=me.Style(flex="1 1 200px")):
                    me.select(
                        label="Duration",
                        options=[
                            me.SelectOption(label="15 seconds", value="15"),
                            me.SelectOption(label="30 seconds", value="30"),
                            me.SelectOption(label="45 seconds", value="45"),
                            me.SelectOption(label="60 seconds", value="60"),
                        ],
                        on_selection_change=on_duration_change,
                        value=str(state.duration),
                    )
                
                with me.box(style=me.Style(flex="1 1 200px")):
                    me.select(
                        label="Visual Style",
                        options=[
                            me.SelectOption(label="Cinematic", value="cinematic"),
                            me.SelectOption(label="Documentary", value="documentary"),
                            me.SelectOption(label="Abstract", value="abstract"),
                            me.SelectOption(label="Minimalist", value="minimalist"),
                            me.SelectOption(label="Vibrant", value="vibrant"),
                        ],
                        on_selection_change=on_style_change,
                        value=state.style,
                    )
                
                with me.box(style=me.Style(flex="1 1 200px")):
                    me.select(
                        label="Video Model",
                        options=[
                            me.SelectOption(label="Veo 2 (Google)", value="veo2"),
                            me.SelectOption(label="Kling 1.6", value="kling"),
                            me.SelectOption(label="Wan Show", value="wan"),
                        ],
                        on_selection_change=on_model_change,
                        value=state.video_model,
                    )
            
            # Generate button
            me.button(
                "🎥 Generate Video",
                on_click=on_generate_click,
                type="flat",
                style=me.Style(
                    margin=me.Margin(top=24),
                    width="100%",
                    background="#4CAF50",
                    color="white",
                    padding=me.Padding.symmetric(vertical=16),
                ),
            )
        
        # Status message
        if state.status:
            with me.box(style=me.Style(
                background="#2a2a3e" if "Success" in state.status else "#3a2a2e",
                padding=me.Padding.all(16),
                border_radius=8,
                margin=me.Margin(top=16),
            )):
                me.text(state.status, style=me.Style(color="#4CAF50" if "Success" in state.status else "#ff6b6b"))
                if state.job_id:
                    me.text(f"Job ID: {state.job_id}", type="body-2", style=me.Style(margin=me.Margin(top=8)))
        
        # Features section
        with me.box(style=me.Style(
            margin=me.Margin(top=32),
            padding=me.Padding.all(24),
            background="#1a1a2e",
            border_radius=12,
        )):
            me.text("✨ Powered By", type="headline-5")
            
            features = [
                "✅ Gemini 2.5 Pro - AI Director for intelligent shot planning",
                "✅ Veo 2, Kling 1.6, Wan Show - Multi-model video generation",
                "✅ Imagen 3 - High-quality keyframe generation",
                "✅ FFmpeg - Professional video stitching & audio mixing",
                "✅ Async Job Queue - Production-scale processing",
            ]
            
            for feature in features:
                me.text(
                    feature,
                    type="body-2",
                    style=me.Style(margin=me.Margin(top=8)),
                )

def on_prompt_change(e: me.InputBlurEvent):
    state = me.state(State)
    state.prompt = e.value

def on_duration_change(e: me.SelectSelectionChangeEvent):
    state = me.state(State)
    state.duration = int(e.value)

def on_style_change(e: me.SelectSelectionChangeEvent):
    state = me.state(State)
    state.style = e.value

def on_model_change(e: me.SelectSelectionChangeEvent):
    state = me.state(State)
    state.video_model = e.value

def on_generate_click(e: me.ClickEvent):
    state = me.state(State)
    
    if not state.prompt:
        state.status = "Error: Please enter a video concept"
        return
    
    # Submit job
    try:
        import uuid
        import asyncio
        from services.workflows.workflow_orchestrator import WorkflowOrchestrator
        from services.workflows.job_queue import get_job_queue
        
        job_id = str(uuid.uuid4())
        state.job_id = job_id
        
        # Create workflow
        orchestrator = WorkflowOrchestrator()
        workflow_json = asyncio.run(orchestrator.create_workflow_from_prompt(
            prompt=state.prompt,
            duration=state.duration,
            style=state.style
        ))
        
        # Submit to queue
        job_queue = get_job_queue()
        asyncio.run(job_queue.submit_job(job_id, workflow_json))
        
        state.status = f"✅ Success! Video generation started. Job ID: {job_id[:8]}..."
    except Exception as ex:
        state.status = f"❌ Error: {str(ex)}"
