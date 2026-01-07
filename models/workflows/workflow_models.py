from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import uuid

@dataclass
class WorkflowStep:
    step_id: str
    step_type: str
    parameters: Dict[str, Any]
    order: int
    output_name: str = "output"
    use_previous_output: bool = False
    previous_output_key: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'step_id': self.step_id,
            'step_type': self.step_type,
            'parameters': self.parameters,
            'order': self.order,
            'output_name': self.output_name,
            'use_previous_output': self.use_previous_output,
            'previous_output_key': self.previous_output_key
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)

@dataclass
class Workflow:
    workflow_id: str
    name: str
    description: str
    steps: List[WorkflowStep]
    created_at: str
    updated_at: str
    created_by: str = "user"
    tags: List[str] = field(default_factory=list)
    is_public: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'workflow_id': self.workflow_id,
            'name': self.name,
            'description': self.description,
            'steps': [step.to_dict() for step in self.steps],
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'created_by': self.created_by,
            'tags': self.tags,
            'is_public': self.is_public
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        steps = [WorkflowStep.from_dict(step) for step in data.get('steps', [])]
        return cls(
            workflow_id=data.get('workflow_id', str(uuid.uuid4())),
            name=data['name'],
            description=data['description'],
            steps=steps,
            created_at=data.get('created_at', datetime.utcnow().isoformat()),
            updated_at=data.get('updated_at', datetime.utcnow().isoformat()),
            created_by=data.get('created_by', 'user'),
            tags=data.get('tags', []),
            is_public=data.get('is_public', False)
        )

@dataclass
class WorkflowExecution:
    execution_id: str
    workflow_id: str
    status: str
    current_step: int
    results: Dict[str, Any]
    started_at: str
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    step_outputs: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'execution_id': self.execution_id,
            'workflow_id': self.workflow_id,
            'status': self.status,
            'current_step': self.current_step,
            'results': self.results,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'error_message': self.error_message,
            'step_outputs': self.step_outputs
        }
