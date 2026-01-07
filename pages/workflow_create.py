import mesop as me

@me.page(path="/workflow-create", title="Creative Automation Machine")
def workflow_create_page():
    state = me.state(State)
    
    with me.box(style=me.Style(
        background="#1a1a2e",
        min_height="100vh",
        padding=me.Padding.all(24)
    )):
        # Header
        me.text(
            "🎬 Creative Automation Machine",
            style=me.Style(font_size=32, font_weight=700, color="#ffffff", margin=me.Margin(bottom=8))
        )
        me.text(
            "Transform ideas into video with AI - Veo 2, Kling, Wan",
            style=me.Style(font_size=14, color="#a0a0a0", margin=me.Margin(bottom=32))
        )
        
        # Video Concept Card
        with me.box(style=me.Style(background="#262640", border_radius=12, padding=me.Padding.all(24), margin=me.Margin(bottom=24))):
            me.text("📄 Video Concept", style=me.Style(font_size=16, font_weight=600, color="#ffffff", margin=me.Margin(bottom=16)))
            me.textarea(
                value=state.prompt,
                on_blur=on_prompt_change,
                rows=6,
                style=me.Style(width="100%", background="#1a1a2e", color="#ffffff", border="1px solid #3a3a5a", border_radius=8, padding=me.Padding.all(12))
            )
        
        # Config Row
        with me.box(style=me.Style(display="flex", gap=16, margin=me.Margin(bottom=24))):
            # Duration
            with me.box(style=me.Style(flex=1, background="#262640", border_radius=12, padding=me.Padding.all(20))):
                me.text("⏱️ Duration", style=me.Style(font_size=14, font_weight=600, color="#ffffff", margin=me.Margin(bottom=12)))
                me.select(
                    options=[me.SelectOption(label="5 sec", value="5"), me.SelectOption(label="10 sec", value="10"), me.SelectOption(label="15 sec", value="15")],
                    on_selection_change=on_duration_change,
                    style=me.Style(width="100%")
                )
            
            # Visual Style
            with me.box(style=me.Style(flex=1, background="#262640", border_radius=12, padding=me.Padding.all(20))):
                me.text("🎨 Visual Style", style=me.Style(font_size=14, font_weight=600, color="#ffffff", margin=me.Margin(bottom=12)))
                me.select(
                    options=[me.SelectOption(label="Cinematic", value="cinematic"), me.SelectOption(label="Realistic", value="realistic")],
                    on_selection_change=on_style_change,
                    style=me.Style(width="100%")
                )
            
            # Video Model
            with me.box(style=me.Style(flex=1, background="#262640", border_radius=12, padding=me.Padding.all(20))):
                me.text("🎥 Model", style=me.Style(font_size=14, font_weight=600, color="#ffffff", margin=me.Margin(bottom=12)))
                me.select(
                    options=[me.SelectOption(label="Veo 2", value="veo2"), me.SelectOption(label="Kling 1.6", value="kling"), me.SelectOption(label="Wan", value="wan")],
                    on_selection_change=on_model_change,
                    style=me.Style(width="100%")
                )
        
        # Generate Button
        me.button(
            "🎬 Generate Video",
            on_click=on_generate_click,
            style=me.Style(
                width="100%",
                background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                color="#ffffff",
                font_size=16,
                font_weight=600,
                padding=me.Padding(top=16, bottom=16, left=24, right=24),
                border_radius=8,
                margin=me.Margin(bottom=24)
            )
        )
        
        # Status
        if state.status:
            with me.box(style=me.Style(background="#262640", border_radius=8, padding=me.Padding.all(16), margin=me.Margin(bottom=24))):
                me.text(state.status, style=me.Style(color="#4ade80" if "Success" in state.status else "#f87171"))
        
        # Workflow Preview
        with me.box(style=me.Style(background="#262640", border_radius=12, padding=me.Padding.all(24))):
            me.text("✨ Workflow Pipeline", style=me.Style(font_size=16, font_weight=600, color="#ffffff", margin=me.Margin(bottom=16)))
            
            nodes = [
                {"icon": "💬", "name": "Gemini Director", "desc": "Script & planning"},
                {"icon": "🎬", "name": "Scene Breakdown", "desc": "Shot composition"},
                {"icon": "🖼️", "name": "Imagen 3", "desc": "Frame generation"},
                {"icon": "🎥", "name": f"{state.model}", "desc": "Video synthesis"},
                {"icon": "🎵", "name": "Audio Mix", "desc": "Sound design"},
                {"icon": "✂️", "name": "FFmpeg", "desc": "Final render"}
            ]
            
            for node in nodes:
                with me.box(style=me.Style(display="flex", align_items="center", gap=12, padding=me.Padding.all(12), margin=me.Margin(bottom=8), background="#1a1a2e", border_radius=8)):
                    me.text(node["icon"], style=me.Style(font_size=20))
                    with me.box():
                        me.text(node["name"], style=me.Style(font_size=14, font_weight=600, color="#ffffff"))
                        me.text(node["desc"], style=me.Style(font_size=12, color="#a0a0a0"))


@me.stateclass
class State:
    prompt: str = '''{
  "camera": "ORBIT: 360° rotation",
  "style": "clay-to-realistic"
}'''
    duration: str = "15"
    style: str = "cinematic"
    model: str = "Veo 2"
    status: str = ""


def on_prompt_change(e: me.InputBlurEvent):
    state = me.state(State)
    state.prompt = e.value


def on_duration_change(e: me.SelectSelectionChangeEvent):
    state = me.state(State)
    state.duration = e.value


def on_style_change(e: me.SelectSelectionChangeEvent):
    state = me.state(State)
    state.style = e.value


def on_model_change(e: me.SelectSelectionChangeEvent):
    state = me.state(State)
    state.model = e.value


def on_generate_click(e: me.ClickEvent):
    import uuid
    state = me.state(State)
    
    if not state.prompt:
        state.status = "❌ Error: Enter a video concept"
        return
    
    try:
        job_id = str(uuid.uuid4())[:8]
        state.status = f"✅ Success! Video generation started. Job: {job_id}"
    except Exception as ex:
        state.status = f"❌ Error: {str(ex)}"
