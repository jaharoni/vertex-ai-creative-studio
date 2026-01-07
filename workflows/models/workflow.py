"""Workflow data models for Hollywood Hercules.

Defines the schema for workflows, workflow nodes, and execution state.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class NodeType(str, Enum):
    """Types of workflow nodes."""
    # Input nodes
    TEXT_INPUT = "text_input"
    IMAGE_UPLOAD = "image_upload"
    PARAMETER_INPUT = "parameter_input"
    
    # Generation nodes
    IMAGEN_GENERATE = "imagen_generate"
    VEO_GENERATE = "veo_generate"
    GEMINI_GENERATE = "gemini_generate"
    GEMINI_TTS = "gemini_tts"
    
    # Segmentation nodes  
    SAM_SEGMENT = "sam_segment"
    
    # Transform nodes
    RESIZE = "resize"
    CROP = "crop"
    STYLE_TRANSFER = "style_transfer"
    
    # Composition nodes
    LAYER = "layer"
    BLEND = "blend"
    COMPOSITE = "composite"
    
    # Output nodes
    OUTPUT = "output"


class NodeStatus(str, Enum):
    """Execution status of a node."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowNode(BaseModel):
    """A single node in a workflow."""
    id: str = Field(..., description="Unique node identifier")
    type: NodeType = Field(..., description="Type of node")
    name: str = Field(..., description="Display name")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Node parameters")
    dependencies: List[str] = Field(default_factory=list, description="IDs of nodes this depends on")
    position: Dict[str, float] = Field(default_factory=dict, description="Canvas position (x, y)")
    status: NodeStatus = Field(default=NodeStatus.PENDING, description="Execution status")
    output: Optional[Dict[str, Any]] = Field(default=None, description="Node output data")
    error: Optional[str] = Field(default=None, description="Error message if failed")


class WorkflowStatus(str, Enum):
    """Overall workflow execution status."""
    DRAFT = "draft"
    RUNNING = "running" 
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Workflow(BaseModel):
    """A complete workflow definition."""
    id: str = Field(..., description="Unique workflow identifier")
    name: str = Field(..., description="Workflow name")
    description: Optional[str] = Field(default=None, description="Workflow description")
    user_id: str = Field(..., description="Owner user ID")
    nodes: List[WorkflowNode] = Field(default_factory=list, description="Workflow nodes")
    connections: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Node connections: [{from: node_id, to: node_id}]"
    )
    status: WorkflowStatus = Field(default=WorkflowStatus.DRAFT, description="Workflow status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    is_public: bool = Field(default=False, description="Whether workflow is publicly visible")
    tags: List[str] = Field(default_factory=list, description="Workflow tags")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class WorkflowExecution(BaseModel):
    """Tracks a single workflow execution."""
    id: str = Field(..., description="Unique execution identifier")
    workflow_id: str = Field(..., description="ID of workflow being executed")
    user_id: str = Field(..., description="User who triggered execution")
    status: WorkflowStatus = Field(default=WorkflowStatus.RUNNING, description="Execution status")
    node_states: Dict[str, NodeStatus] = Field(
        default_factory=dict,
        description="Status of each node: {node_id: status}"
    )
    node_outputs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Outputs from each node: {node_id: output_data}"
    )
    started_at: datetime = Field(default_factory=datetime.utcnow, description="Execution start time")
    completed_at: Optional[datetime] = Field(default=None, description="Execution completion time")
    error: Optional[str] = Field(default=None, description="Error message if failed")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
