"""Workflow API endpoints."""
from flask import Blueprint, request, jsonify
from workflows.storage import WorkflowStorage
from workflows.executor import WorkflowExecutor

workflows_bp = Blueprint('workflows', __name__)

@workflows_bp.route('/workflows', methods=['POST'])
def create_workflow():
    """Create new workflow."""
    return jsonify({"id": "workflow-123"}), 201

@workflows_bp.route('/workflows/<workflow_id>', methods=['GET'])
def get_workflow(workflow_id):
    """Get workflow by ID."""
    return jsonify({"id": workflow_id})

@workflows_bp.route('/workflows/<workflow_id>/execute', methods=['POST'])
def execute_workflow(workflow_id):
    """Execute workflow."""
    return jsonify({"execution_id": "exec-123"})
