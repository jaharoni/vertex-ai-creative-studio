# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");

"""Workflow Creation Page - Text-to-Video Magic."""

import mesop as me
from state.state import AppState
from components.header import header
from components.page_scaffold import page_scaffold, page_frame


@me.stateclass
class WorkflowPageState:
    prompt: str = ""
    is_generating: bool = False
    workflow_id: str = ""
    error_message: str = ""


@me.page(
    path="/workflow/create",
    title="GenMedia Creative Studio - Workflow",
)
def page():
    with page_scaffold(page_name="workflow"):
        workflow_content()


def workflow_content():
    state = me.state(WorkflowPageState)
    
    with page_frame():
        header("Create Something Amazing", "auto_awesome")
        
        # Hero section
        with me.box(
            style=me.Style(
                margin=me.Margin(bottom=32),
                padding=me.Padding.all(24),
                background="#f8f9fa",
                border_radius=8,
            )
        ):
            me.text(
                "Describe your vision in natural language. AI will plan and execute the entire creative workflow.",
                style=me.Style(font_size=18, color="#5f6368"),
            )
        
        # Main prompt input
        with me.box(
            style=me.Style(
                margin=me.Margin(bottom=24),
            )
        ):
            me.textarea(
                value=state.prompt,
                label="Your Creative Vision",
                placeholder="""Example: "30-second Nike ad. Street basketball in Brooklyn, golden hour. Kids playing pickup game. Spike Jonze vibes. Hip-hop beat. Voiceover: inspirational quote about dreams.""",
                on_blur=on_prompt_change,
                rows=6,
                style=me.Style(width="100%"),
            )
        
        # Action buttons
        with me.box(
            style=me.Style(
                display="flex",
                gap=16,
                margin=me.Margin(bottom=24),
            )
        ):
            me.button(
                "Generate Workflow",
                on_click=on_generate_click,
                disabled=state.is_generating or not state.prompt,
                type="raised",
                style=me.Style(
                    background="#1976d2" if not state.is_generating else "#ccc",
                    color="white",
                )
            )
            
            me.button(
                "Use Template",
                on_click=on_template_click,
                type="stroked",
            )
        
        # Status messages
        if state.is_generating:
            with me.box(
                style=me.Style(
                    padding=me.Padding.all(16),
                    background="#e3f2fd",
                    border_radius=8,
                )
            ):
                me.text("🎬 Planning your creative workflow...")
        
        if state.error_message:
            with me.box(
                style=me.Style(
                    padding=me.Padding.all(16),
                    background="#ffebee",
                    border_radius=8,
                )
            ):
                me.text(f"❌ {state.error_message}", style=me.Style(color="#c62828"))
        
        # Example workflows
        render_examples()


def render_examples():
    with me.box(
        style=me.Style(
            margin=me.Margin(top=48),
        )
    ):
        me.text("Quick Examples", type="headline-6")
        
        examples = [
            "30sec Patagonia ad. Sunrise hike in Yosemite. Lone climber summits Half Dome. Wes Anderson symmetry meets Planet Earth cinematography.",
            "60sec Coca-Cola commercial. 4th of July backyard pool party in the Hamptons, late afternoon. Michael Bay energy meets A24 aesthetics.",
            "15sec Instagram Reel. UGC-style product unboxing. Hiking boots. Authentic, handheld camera.",
        ]
        
        with me.box(
            style=me.Style(
                display="grid",
                grid_template_columns="repeat(auto-fit, minmax(300px, 1fr))",
                gap=16,
                margin=me.Margin(top=16),
            )
        ):
            for example in examples:
                with me.box(
                    style=me.Style(
                        padding=me.Padding.all(16),
                        border=me.Border.all(me.BorderSide(color="#e0e0e0")),
                        border_radius=8,
                        cursor="pointer",
                    ),
                    on_click=lambda e, text=example: use_example(text),
                ):
                    me.text(example, style=me.Style(font_size=14))


def on_prompt_change(e: me.InputBlurEvent):
    state = me.state(WorkflowPageState)
    state.prompt = e.value


def on_generate_click(e: me.ClickEvent):
    state = me.state(WorkflowPageState)
    app_state = me.state(AppState)
    
    state.is_generating = True
    state.error_message = ""
    
    try:
        # Import here to avoid circular dependency
        from services.workflows.orchestrator import WorkflowOrchestrator
        
        orchestrator = WorkflowOrchestrator()
        result = orchestrator.create_workflow_from_prompt(
            prompt=state.prompt,
            user_email=app_state.user_email
        )
        
        state.workflow_id = result["workflow_id"]
        
        # Navigate to workflow status page
        me.navigate(f"/workflow/status?id={state.workflow_id}")
        
    except Exception as error:
        state.error_message = f"Failed to create workflow: {str(error)}"
        state.is_generating = False
    
    yield


def on_template_click(e: me.ClickEvent):
    # Future: Navigate to template selection page
    me.navigate("/templates")


def use_example(text: str):
    state = me.state(WorkflowPageState)
    state.prompt = text
    yield

