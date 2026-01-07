"""Firestore storage layer for workflows."""

from datetime import datetime
from typing import List, Optional
from google.cloud import firestore
from workflows.models.workflow import Workflow, WorkflowExecution, WorkflowStatus


class WorkflowStorage:
    """Firestore storage for workflows."""
    
    def __init__(self, db: firestore.Client):
        self.db = db
        self.workflows_collection = "workflows"
        self.executions_collection = "workflow_executions"
    
    def save_workflow(self, workflow: Workflow) -> None:
        """Save workflow to Firestore."""
        workflow.updated_at = datetime.utcnow()
        doc_ref = self.db.collection(self.workflows_collection).document(workflow.id)
        doc_ref.set(workflow.dict())
    
    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """Get workflow by ID."""
        doc_ref = self.db.collection(self.workflows_collection).document(workflow_id)
        doc = doc_ref.get()
        if doc.exists:
            return Workflow(**doc.to_dict())
        return None
    
    def list_workflows(self, user_id: str, limit: int = 50) -> List[Workflow]:
        """List workflows for a user."""
        query = (self.db.collection(self.workflows_collection)
                .where("user_id", "==", user_id)
                .order_by("updated_at", direction=firestore.Query.DESCENDING)
                .limit(limit))
        return [Workflow(**doc.to_dict()) for doc in query.stream()]
    
    def save_execution(self, execution: WorkflowExecution) -> None:
        """Save workflow execution."""
        doc_ref = self.db.collection(self.executions_collection).document(execution.id)
        doc_ref.set(execution.dict())
    
    def get_execution(self, execution_id: str) -> Optional[WorkflowExecution]:
        """Get execution by ID."""
        doc_ref = self.db.collection(self.executions_collection).document(execution_id)
        doc = doc_ref.get()
        if doc.exists:
            return WorkflowExecution(**doc.to_dict())
        return None
