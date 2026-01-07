import mesop as me

@me.page(
    path="/workflow-create",
    title="Creative Automation Machine",
)
def page():
    with me.box(
        style=me.Style(
            display="flex",
            flex_direction="column",
            gap=24,
            padding=me.Padding.all(24),
        )
    ):
        me.text(
            "🎬 Creative Automation Machine",
            type="headline-3",
        )
        me.text(
            "Transform your ideas into video with AI",
            type="headline-5",
        )
        
        # Coming soon message
        with me.box(
            style=me.Style(
                background="#1a1a2e",
                padding=me.Padding.all(24),
                border_radius=12,
                margin=me.Margin(top=24),
            )
        ):
            me.text(
                "🚀 Workflow Automation System",
                type="headline-5",
            )
            me.text(
                "The Creative Automation Machine has been successfully deployed with:",
                style=me.Style(margin=me.Margin(top=12, bottom=12)),
            )
            
            features = [
                "✅ Gemini 2.5 Pro as AI Director",
                "✅ Workflow Orchestrator for shot planning",
                "✅ Workflow Executor with Imagen 3 & Veo 2",
                "✅ Multi-model support (Veo 2, Kling 1.6, Wan Show)",
                "✅ FFmpeg Service for video stitching",
                "✅ Job Queue System (async processing)",
                "✅ Text-to-workflow JSON generation",
            ]
            
            for feature in features:
                me.text(
                    feature,
                    style=me.Style(margin=me.Margin(top=8)),
                )
            
            me.text(
                "\n📝 Backend services are ready. UI integration in progress.",
                type="body-1",
                style=me.Style(
                    margin=me.Margin(top=24),
                    color="#4CAF50",
                    font_weight=500,
                ),
            )
