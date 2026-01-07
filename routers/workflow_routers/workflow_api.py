from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from models.workflows.workflow_models import Workflow, WorkflowStep
from services.workflows.workflow_storage import storage
from services.workflows.workflow_executor import executor
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/workflows", tags=["workflows"])

@router.post("/create")
async def create_workflow(name: str, description: str, steps: List[Dict[str, Any]]):
    workflow_steps = []
    for i, step_data in enumerate(steps):
        step = WorkflowStep(
            step_id=str(uuid.uuid4()),
            step_type=step_data["type"],
            parameters=step_data.get("parameters", {}),
            order=i,
            output_name=step_data.get("output_name", f"step{i}_output")
        )
        workflow_steps.append(step)
    
    workflow = Workflow(
        workflow_id=str(uuid.uuid4()),
        name=name,
        description=description,
        steps=workflow_steps,
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat()
    )
    
    workflow_id = storage.save_workflow(workflow)
    return {"workflow_id": workflow_id, "status": "created"}

@router.get("/list")
async def list_workflows():
    workflows = storage.list_workflows()
    return [{"id": w.workflow_id, "name": w.name, "description": w.description} for w in workflows]

@router.post("/execute/{workflow_id}")
async def execute_workflow(workflow_id: str, inputs: Dict[str, Any] = {}):
    try:
        execution_id = await executor.execute_workflow(workflow_id, inputs)
        return {"execution_id": execution_id, "status": "started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/execution/{execution_id}")
async def get_execution(execution_id: str):
    execution = storage.get_execution(execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    return execution.to_dict()
