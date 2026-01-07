import mesop as me
from components.page_scaffold import page_frame, page_scaffold

@me.page(
    path="/workflow-create",
    title="Workflow Creator - GenMedia Creative Studio",
)
def workflow_page():
    with page_frame():
        with page_scaffold(
            title="Visual Workflow Builder",
            subtitle="Build custom AI workflows by connecting nodes - Create complex pipelines from simple building blocks"
        ):
            # Main workflow canvas
            with me.box(
                style=me.Style(
                    background="#f5f5f5",
                    border_radius=8,
                    padding=me.Padding.all(32),
                    min_height=400,
                    display="flex",
                    flex_direction="column",
                    align_items="center",
                    justify_content="center",
                )
            ):
                me.text(
                    "Visual Workflow Canvas",
                    style=me.Style(
                        font_size=24,
                        font_weight=600,
                        color="#666",
                        margin=me.Margin(bottom=16),
                    ),
                )
                me.text(
                    "Drag and drop nodes to build your workflow",
                    style=me.Style(
                        font_size=16,
                        color="#999",
                        margin=me.Margin(bottom=8),
                    ),
                )
                me.text(
                    "Coming soon: Interactive node-based workflow builder with real-time preview",
                    style=me.Style(
                        font_size=14,
                        color="#aaa",
                        font_style="italic",
                    ),
                )
            
            # Key features section
            me.text(
                "Key Features",
                style=me.Style(
                    font_size=20,
                    font_weight=600,
                    margin=me.Margin(top=32, bottom=16),
                ),
            )
            
            with me.box(
                style=me.Style(
                    display="flex",
                    flex_direction="row",
                    gap=16,
                    flex_wrap="wrap",
                )
            ):
                features = [
                    ("Node-Based Design", "Connect AI models visually"),
                    ("Real-Time Preview", "See results as you build"),
                    ("Save & Share", "Export and collaborate"),
                    ("One-Click Deploy", "Launch workflows instantly"),
                ]
                
                for title, description in features:
                    with me.box(
                        style=me.Style(
                            background="white",
                            border_radius=8,
                            padding=me.Padding.all(20),
                            flex_basis="calc(25% - 12px)",
                            border=me.Border.all(me.BorderSide(width=1, color="#e0e0e0", style="solid")),
                        )
                    ):
                        me.text(
                            title,
                            style=me.Style(
                                font_weight=600,
                                margin=me.Margin(bottom=8),
                            ),
                        )
                        me.text(
                            description,
                            style=me.Style(
                                font_size=14,
                                color="#666",
                            ),
                        )
