import mesop as me
from components.page import page_scaffold

@me.page(
    path="/workflow-create",
    title="Workflow Creator - GenMedia Creative Studio",
)
def page():
    with page_scaffold(page_name="Workflow Creator"):
        workflow_content()

def workflow_content():
    with me.box(style=me.Style(
        padding=me.Padding.all(32),
        display="flex",
        flex_direction="column",
        gap=24,
    )):
        me.text(
            "Visual Workflow Builder",
            style=me.Style(
                font_size=36,
                font_weight=700,
                margin=me.Margin(bottom=8),
            ),
        )
        
        me.text(
            "Build custom AI workflows by connecting nodes - Create complex pipelines from simple building blocks",
            style=me.Style(
                font_size=18,
                color="#666",
                margin=me.Margin(bottom=32),
            ),
        )
        
        with me.box(style=me.Style(
            border=me.Border.all(
                me.BorderSide(width=2, color="#e0e0e0", style="solid")
            ),
            border_radius=12,
            min_height=600,
            background="#f5f5f5",
            padding=me.Padding.all(24),
            display="flex",
            flex_direction="column",
            align_items="center",
            justify_content="center",
        )):
            me.text(
                "Visual Workflow Canvas",
                style=me.Style(
                    font_size=24,
                    font_weight=600,
                    color="#999",
                    margin=me.Margin(bottom=16),
                ),
            )
            
            me.text(
                "Drag and drop nodes to build your workflow",
                style=me.Style(
                    font_size=16,
                    color="#aaa",
                    margin=me.Margin(bottom=8),
                ),
            )
            
            me.text(
                "Coming soon: Interactive node-based workflow builder with real-time preview",
                style=me.Style(
                    font_size=14,
                    color="#bbb",
                    font_style="italic",
                ),
            )
        
        me.text(
            "Key Features",
            style=me.Style(
                font_size=24,
                font_weight=600,
                margin=me.Margin(top=32, bottom=16),
            ),
        )
        
        with me.box(style=me.Style(
            display="grid",
            grid_template_columns="repeat(auto-fit, minmax(250px, 1fr))",
            gap=16,
        )):
            feature_card("Node-Based Design", "Connect AI models visually")
            feature_card("Real-Time Preview", "See results as you build")
            feature_card("Save & Share", "Export and collaborate")
            feature_card("One-Click Deploy", "Launch workflows instantly")

def feature_card(title: str, description: str):
    with me.box(style=me.Style(
        background="#fff",
        padding=me.Padding.all(20),
        border_radius=8,
        border=me.Border.all(
            me.BorderSide(width=1, color="#e0e0e0", style="solid")
        ),
    )):
        me.text(
            title,
            style=me.Style(
                font_size=18,
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
