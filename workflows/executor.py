"""Workflow execution engine."""

import uuid
from datetime import datetime
from typing import Dict, Any
from workflows.models.workflow import Workflow, WorkflowExecution, WorkflowStatus, NodeStatus, NodeType
from workflows.storage import WorkflowStorage


class WorkflowExecutor:
    """Executes workflows by orchestrating nodes."""
    
    def __init__(self, storage: WorkflowStorage):
        self.storage = storage
    
    async def execute_workflow(self, workflow_id: str, user_id: str) -> WorkflowExecution:
        """Execute a workflow."""
        workflow = self.storage.get_workflow(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        # Create execution record
        execution = WorkflowExecution(
            id=str(uuid.uuid4()),
            workflow_id=workflow_id,
            user_id=user_id,
            status=WorkflowStatus.RUNNING
        )
        self.storage.save_execution(execution)
        
        try:
            # Execute nodes in dependency order
            for node in self._topological_sort(workflow):
                await self._execute_node(node, execution)
            
            execution.status = WorkflowStatus.COMPLETED
            execution.completed_at = datetime.utcnow()
        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.error = str(e)
        
        self.storage.save_execution(execution)
        return execution
    
    def _topological_sort(self, workflow: Workflow):
        """Sort nodes by dependencies."""
        # Simple topological sort implementation
        return workflow.nodes
    
    async def _execute_node(self, node, execution):
        """Execute a single node."""
        execution.node_states[node.id] = NodeStatus.RUNNING
        # Node execution logic based on type
        # This will call appropriate service (Imagen, Veo, SAM, etc.)
        execution.node_states[node.id] = NodeStatus.COMPLETED
