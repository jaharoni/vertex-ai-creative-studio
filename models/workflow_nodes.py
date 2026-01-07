# Copyright 2025 Google LLC
# Node-based Visual Workflow System

from typing import Dict, List, Optional, Any, Union
from enum import Enum
from pydantic import BaseModel, Field
import uuid

class NodeType(str, Enum):
    """Types of workflow nodes."""
    # Input nodes
    TEXT_INPUT = "text_input"
    IMAGE_INPUT = "image_input"
    VIDEO_INPUT = "video_input"
    AUDIO_INPUT = "audio_input"
    MULTIBLOCK = "multiblock"
    
    # AI Generator nodes
    GEMINI_TEXT = "gemini_text"  # Gemini 2.0 Flash
    IMAGEN_GENERATE = "imagen_generate"  # Imagen 3
    VEO_GENERATE = "veo_generate"  # Veo 2
    KLING_GENERATE = "kling_generate"  # Kling 2.6 Pro
    WAN_GENERATE = "wan_generate"  # Wan 2.6
    AUDIO_GENERATE = "audio_generate"  # Chirp/TTS
    
    # Tool nodes
    TEXT_COMBINER = "text_combiner"
    JSON_EXTRACTOR = "json_extractor"
    CONDITION = "condition"
    LOOP = "loop"
    PARALLEL = "parallel"
    
    # Output nodes
    OUTPUT = "output"

class NodeConfig(BaseModel):
    """Configuration for a workflow node."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: NodeType
    label: str
    config: Dict[str, Any] = {}
    position: Dict[str, int] = {"x": 0, "y": 0}

class Connection(BaseModel):
    """Connection between nodes."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_node: str
    source_output: str = "output"
    target_node: str
    target_input: str = "input"

class WorkflowGraph(BaseModel):
    """Complete workflow graph."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str = ""
    nodes: List[NodeConfig] = []
    connections: List[Connection] = []
    metadata: Dict[str, Any] = {}

# Node Templates for easy workflow creation
NODE_TEMPLATES = {
    NodeType.TEXT_INPUT: {
        "label": "Text Input",
        "description": "Enter text or prompt",
        "inputs": [],
        "outputs": [{"name": "text", "type": "string"}],
        "config_schema": {
            "placeholder": "string",
            "multiline": "boolean",
            "default_value": "string"
        }
    },
    
    NodeType.GEMINI_TEXT: {
        "label": "Gemini 2.0 Flash",
        "description": "Generate text with Gemini 2.0 (latest)",
        "inputs": [{"name": "prompt", "type": "string"}],
        "outputs": [{"name": "text", "type": "string"}],
        "config_schema": {
            "model": {"type": "select", "options": ["gemini-2.0-flash-exp", "gemini-2.0-flash-thinking-exp"]},
            "temperature": {"type": "number", "min": 0, "max": 2, "default": 0.7},
            "max_tokens": {"type": "number", "default": 2048},
            "system_prompt": {"type": "text", "multiline": True}
        }
    },
    
    NodeType.IMAGEN_GENERATE: {
        "label": "Imagen 3",
        "description": "Generate images with Imagen 3",
        "inputs": [{"name": "prompt", "type": "string"}],
        "outputs": [{"name": "image", "type": "image"}],
        "config_schema": {
            "aspect_ratio": {"type": "select", "options": ["1:1", "16:9", "9:16", "4:3"]},
            "num_images": {"type": "number", "min": 1, "max": 4, "default": 1},
            "safety_filter": {"type": "select", "options": ["block_some", "block_few", "block_most"]},
            "person_generation": {"type": "select", "options": ["allow_all", "allow_adult", "dont_allow"]}
        }
    },
    
    NodeType.VEO_GENERATE: {
        "label": "Veo 2 (Google)",
        "description": "Generate videos with Veo 2",
        "inputs": [
            {"name": "prompt", "type": "string"},
            {"name": "image", "type": "image", "optional": True}
        ],
        "outputs": [{"name": "video", "type": "video"}],
        "config_schema": {
            "duration": {"type": "select", "options": ["5s", "8s"]},
            "aspect_ratio": {"type": "select", "options": ["16:9", "9:16", "1:1"]},
            "mode": {"type": "select", "options": ["text-to-video", "image-to-video"]}
        }
    },
    
    NodeType.KLING_GENERATE: {
        "label": "Kling 2.6 Pro",
        "description": "Generate videos with Kling 2.6 (motion control + native audio)",
        "inputs": [
            {"name": "prompt", "type": "string"},
            {"name": "image", "type": "image", "optional": True}
        ],
        "outputs": [{"name": "video", "type": "video"}],
        "config_schema": {
            "duration": {"type": "select", "options": ["5", "10", "15"]},
            "mode": {"type": "select", "options": ["std", "pro"]},
            "aspect_ratio": {"type": "select", "options": ["16:9", "9:16", "1:1"]},
            "native_audio": {"type": "boolean", "default": True},
            "motion_intensity": {"type": "number", "min": 0, "max": 1, "default": 0.5}
        }
    },
    
    NodeType.WAN_GENERATE: {
        "label": "Wan 2.6 (Alibaba)",
        "description": "Generate multi-shot narrative videos with Wan 2.6",
        "inputs": [
            {"name": "prompt", "type": "string"},
            {"name": "reference_video", "type": "video", "optional": True}
        ],
        "outputs": [{"name": "video", "type": "video"}],
        "config_schema": {
            "duration": {"type": "select", "options": ["3", "5", "10", "15"]},
            "resolution": {"type": "select", "options": ["480p", "720p", "1080p"]},
            "mode": {"type": "select", "options": ["text-to-video", "image-to-video", "reference-to-video"]},
            "character_consistency": {"type": "boolean", "default": True}
        }
    },
    
    NodeType.TEXT_COMBINER: {
        "label": "Text Combiner",
        "description": "Combine multiple text inputs",
        "inputs": [
            {"name": "input1", "type": "string"},
            {"name": "input2", "type": "string"},
            {"name": "input3", "type": "string", "optional": True}
        ],
        "outputs": [{"name": "text", "type": "string"}],
        "config_schema": {
            "separator": {"type": "string", "default": "\n"},
            "template": {"type": "text", "multiline": True}
        }
    },
    
    NodeType.CONDITION: {
        "label": "Condition",
        "description": "Branch based on condition",
        "inputs": [{"name": "input", "type": "any"}],
        "outputs": [
            {"name": "true", "type": "any"},
            {"name": "false", "type": "any"}
        ],
        "config_schema": {
            "condition": {"type": "text"},
            "operator": {"type": "select", "options": ["equals", "contains", "greater", "less"]}
        }
    },
    
    NodeType.PARALLEL: {
        "label": "Parallel Execution",
        "description": "Execute multiple branches in parallel",
        "inputs": [{"name": "input", "type": "any"}],
        "outputs": [
            {"name": "output1", "type": "any"},
            {"name": "output2", "type": "any"},
            {"name": "output3", "type": "any"}
        ],
        "config_schema": {}
    }
}

# Workflow Templates
WORKFLOW_TEMPLATES = {
    "cinematic_video": {
        "name": "Cinematic Video Production",
        "description": "Complete pipeline: Concept → Storyboard → Images → Video → Audio",
        "nodes": [
            {"type": NodeType.TEXT_INPUT, "label": "Video Concept", "position": {"x": 100, "y": 100}},
            {"type": NodeType.GEMINI_TEXT, "label": "Enhance with Gemini", "position": {"x": 300, "y": 100}},
            {"type": NodeType.IMAGEN_GENERATE, "label": "Generate Key Frame", "position": {"x": 500, "y": 100}},
            {"type": NodeType.VEO_GENERATE, "label": "Generate Video", "position": {"x": 700, "y": 100}},
            {"type": NodeType.AUDIO_GENERATE, "label": "Add Audio", "position": {"x": 900, "y": 100}},
            {"type": NodeType.OUTPUT, "label": "Final Video", "position": {"x": 1100, "y": 100}}
        ]
    },
    
    "multi_model_comparison": {
        "name": "Multi-Model Video Comparison",
        "description": "Generate same video with Veo, Kling, and Wan for comparison",
        "nodes": [
            {"type": NodeType.TEXT_INPUT, "label": "Prompt", "position": {"x": 100, "y": 300}},
            {"type": NodeType.PARALLEL, "label": "Split to 3 Models", "position": {"x": 300, "y": 300}},
            {"type": NodeType.VEO_GENERATE, "label": "Veo 2", "position": {"x": 500, "y": 100}},
            {"type": NodeType.KLING_GENERATE, "label": "Kling 2.6", "position": {"x": 500, "y": 300}},
            {"type": NodeType.WAN_GENERATE, "label": "Wan 2.6", "position": {"x": 500, "y": 500}}
        ]
    },
    
    "story_to_video": {
        "name": "Story to Multi-Scene Video",
        "description": "Break story into scenes, generate images, animate with video model",
        "nodes": [
            {"type": NodeType.TEXT_INPUT, "label": "Story", "position": {"x": 100, "y": 200}},
            {"type": NodeType.GEMINI_TEXT, "label": "Scene Breakdown", "position": {"x": 300, "y": 200}},
            {"type": NodeType.LOOP, "label": "For Each Scene", "position": {"x": 500, "y": 200}},
            {"type": NodeType.IMAGEN_GENERATE, "label": "Generate Scene Image", "position": {"x": 700, "y": 200}},
            {"type": NodeType.KLING_GENERATE, "label": "Animate Scene", "position": {"x": 900, "y": 200}}
        ]
    }
}
