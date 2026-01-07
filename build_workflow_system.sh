#!/bin/bash
echo "=== Building Complete Workflow System ==="

# 1. Storage Service
cat > services/workflows/workflow_storage.py << 'EOF'
import json
import os
from typing import List, Dict, Optional
from models.workflows.workflow_models import Workflow, WorkflowExecution
import uuid
from datetime import datetime

class WorkflowStorage:
    def __init__(self, data_dir="data/workflows"):
        self.data_dir = data_dir
        self.workflows_file = os.path.join(data_dir, "workflows.json")
        self.executions_file = os.path.join(data_dir, "executions.json")
        os.makedirs(data_dir, exist_ok=True)
        self._init_files()
    
    def _init_files(self):
        if not os.path.exists(self.workflows_file):
            with open(self.workflows_file, 'w') as f:
                json.dump({}, f)
        if not os.path.exists(self.executions_file):
            with open(self.executions_file, 'w') as f:
                json.dump({}, f)
    
    def save_workflow(self, workflow: Workflow) -> str:
        workflows = self._load_workflows()
        workflows[workflow.workflow_id] = workflow.to_dict()
        self._save_workflows(workflows)
        return workflow.workflow_id
    
    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        workflows = self._load_workflows()
        if workflow_id in workflows:
            return Workflow.from_dict(workflows[workflow_id])
        return None
    
    def list_workflows(self) -> List[Workflow]:
        workflows = self._load_workflows()
        return [Workflow.from_dict(w) for w in workflows.values()]
    
    def delete_workflow(self, workflow_id: str) -> bool:
        workflows = self._load_workflows()
        if workflow_id in workflows:
            del workflows[workflow_id]
            self._save_workflows(workflows)
            return True
        return False
    
    def save_execution(self, execution: WorkflowExecution) -> str:
        executions = self._load_executions()
        executions[execution.execution_id] = execution.to_dict()
        self._save_executions(executions)
        return execution.execution_id
    
    def get_execution(self, execution_id: str) -> Optional[WorkflowExecution]:
        executions = self._load_executions()
        if execution_id in executions:
            data = executions[execution_id]
            return WorkflowExecution(**data)
        return None
    
    def _load_workflows(self) -> Dict:
        try:
            with open(self.workflows_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_workflows(self, workflows: Dict):
        with open(self.workflows_file, 'w') as f:
            json.dump(workflows, f, indent=2)
    
    def _load_executions(self) -> Dict:
        try:
            with open(self.executions_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_executions(self, executions: Dict):
        with open(self.executions_file, 'w') as f:
            json.dump(executions, f, indent=2)

storage = WorkflowStorage()
EOF

echo "✓ Created workflow_storage.py"
