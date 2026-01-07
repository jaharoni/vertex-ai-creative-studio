import mesop as me
import mesop.labs as mel

@me.page(
    path="/workflow-builder",
    title="AI Workflow Builder",
)
def workflow_builder_page():
    with me.box(style=me.Style(height="100%", display="flex", flex_direction="column", background="#1a1a1a")):
        # Header
        with me.box(style=me.Style(padding=me.Padding.all(20), background="#2d2d2d", border_bottom=me.Border.all(me.BorderSide(width=1, color="#444", style="solid")))):
            me.text("AI Workflow Builder", style=me.Style(font_size=24, font_weight="bold", color="#ffffff"))
            me.text("Drag and drop AI model nodes to create custom workflows", style=me.Style(font_size=14, color="#aaaaaa", margin=me.Margin(top=8)))
        
        with me.box(style=me.Style(display="flex", flex=1, overflow="auto")):
            # Sidebar with available nodes
            with me.box(style=me.Style(width="250px", background="#2d2d2d", padding=me.Padding.all(16), border_right=me.Border.all(me.BorderSide(width=1, color="#444", style="solid")), overflow_y="auto")):
                me.text("Available Models", style=me.Style(font_size=16, font_weight="bold", color="#ffffff", margin=me.Margin(bottom=16)))
                
                # Node types
                create_node_button("Imagen", "Image Generation", "#4285f4")
                create_node_button("Veo", "Video Generation", "#ea4335")
                create_node_button("Gemini", "Text/Chat", "#fbbc04")
                create_node_button("Gemini Image", "Image Understanding", "#34a853")
                create_node_button("Gemini TTS", "Text-to-Speech", "#ff6d00")
                create_node_button("Chirp 3 HD", "Audio Generation", "#9c27b0")
                create_node_button("Lyria", "Music Generation", "#00bcd4")
                
                me.divider(style=me.Style(margin=me.Margin(top=24, bottom=24)))
                
                me.text("Utility Nodes", style=me.Style(font_size=16, font_weight="bold", color="#ffffff", margin=me.Margin(bottom=16)))
                create_node_button("Input", "User Input", "#607d8b")
                create_node_button("Output", "Final Output", "#607d8b")
                create_node_button("Transform", "Data Transform", "#795548")
            
            # Canvas area
            with me.box(style=me.Style(flex=1, background="#1a1a1a", position="relative", padding=me.Padding.all(32))):
                me.text("Canvas", style=me.Style(font_size=18, color="#666", text_align="center", margin=me.Margin(top=100)))
                me.text("Drag nodes from the sidebar to start building your workflow", style=me.Style(font_size=14, color="#444", text_align="center", margin=me.Margin(top=8)))
                
                # Instructions
                with me.box(style=me.Style(position="absolute", bottom=20, right=20, background="#2d2d2d", padding=me.Padding.all(16), border_radius=8)):
                    me.text("Quick Start:", style=me.Style(font_size=14, font_weight="bold", color="#ffffff", margin=me.Margin(bottom=8)))
                    me.text("• Drag model nodes onto the canvas", style=me.Style(font_size=12, color="#aaaaaa"))
                    me.text("• Connect nodes by clicking outputs to inputs", style=me.Style(font_size=12, color="#aaaaaa"))
                    me.text("• Configure each node's parameters", style=me.Style(font_size=12, color="#aaaaaa"))
                    me.text("• Click 'Execute' to run your workflow", style=me.Style(font_size=12, color="#aaaaaa"))
        
        # Bottom toolbar
        with me.box(style=me.Style(padding=me.Padding.all(16), background="#2d2d2d", border_top=me.Border.all(me.BorderSide(width=1, color="#444", style="solid")), display="flex", gap=12, justify_content="flex-end")):
            me.button("Clear Canvas", on_click=lambda e: None, style=me.Style(padding=me.Padding(top=8, bottom=8, left=16, right=16), background="#444", color="#ffffff", border_radius=4))
            me.button("Save Workflow", on_click=lambda e: None, style=me.Style(padding=me.Padding(top=8, bottom=8, left=16, right=16), background="#4285f4", color="#ffffff", border_radius=4))
            me.button("Execute Workflow", on_click=lambda e: None, style=me.Style(padding=me.Padding(top=8, bottom=8, left=16, right=16), background="#34a853", color="#ffffff", border_radius=4))

def create_node_button(name: str, description: str, color: str):
    """Create a draggable node button"""
    with me.box(
        style=me.Style(
            background=color,
            padding=me.Padding.all(12),
            border_radius=8,
            margin=me.Margin(bottom=8),
            cursor="grab",
        )
    ):
        me.text(name, style=me.Style(font_size=14, font_weight="bold", color="#ffffff"))
        me.text(description, style=me.Style(font_size=11, color="#ffffffdd", margin=me.Margin(top=4)))
