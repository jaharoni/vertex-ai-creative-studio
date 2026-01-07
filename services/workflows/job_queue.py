"""
Job Queue System for Creative Automation Machine
Manages async job execution for video generation workflows
"""
import asyncio
import logging
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import json

logger = logging.getLogger(__name__)

class JobStatus(Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Job:
    id: str
    workflow_json: Dict[str, Any]
    status: JobStatus = JobStatus.QUEUED
    progress: float = 0.0
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
class JobQueue:
    """Async job queue for workflow execution"""
    
    def __init__(self, max_concurrent=3):
        self.jobs: Dict[str, Job] = {}
        self.max_concurrent = max_concurrent
        self._running_tasks: Dict[str, asyncio.Task] = {}
        self._queue = asyncio.Queue()
        self._worker_task = None
        
    async def start(self):
        """Start the job queue worker"""
        if self._worker_task is None:
            self._worker_task = asyncio.create_task(self._worker())
            logger.info(f"Job queue started with max_concurrent={self.max_concurrent}")
            
    async def stop(self):
        """Stop the job queue worker"""
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
            self._worker_task = None
            logger.info("Job queue stopped")
            
    async def submit_job(self, job_id: str, workflow_json: Dict[str, Any]) -> str:
        """Submit a new job to the queue"""
        job = Job(id=job_id, workflow_json=workflow_json)
        self.jobs[job_id] = job
        await self._queue.put(job_id)
        logger.info(f"Job {job_id} submitted to queue")
        return job_id
        
    def get_job(self, job_id: str) -> Optional[Job]:
        """Get job by ID"""
        return self.jobs.get(job_id)
        
    def list_jobs(self, status: Optional[JobStatus] = None) -> List[Job]:
        """List all jobs, optionally filtered by status"""
        if status:
            return [job for job in self.jobs.values() if job.status == status]
        return list(self.jobs.values())
        
    async def cancel_job(self, job_id: str) -> bool:
        """Cancel a job"""
        job = self.jobs.get(job_id)
        if not job:
            return False
            
        if job.status == JobStatus.RUNNING:
            task = self._running_tasks.get(job_id)
            if task:
                task.cancel()
        elif job.status == JobStatus.QUEUED:
            job.status = JobStatus.CANCELLED
            
        logger.info(f"Job {job_id} cancelled")
        return True
        
    async def _worker(self):
        """Main worker loop - processes jobs from queue"""
        from .workflow_executor import WorkflowExecutor
        
        executor = WorkflowExecutor()
        
        while True:
            try:
                # Wait for a job
                job_id = await self._queue.get()
                job = self.jobs.get(job_id)
                
                if not job:
                    continue
                    
                # Wait if we're at max concurrent jobs
                while len(self._running_tasks) >= self.max_concurrent:
                    await asyncio.sleep(0.5)
                    
                # Start the job
                task = asyncio.create_task(self._execute_job(job, executor))
                self._running_tasks[job_id] = task
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker error: {e}")
                
    async def _execute_job(self, job: Job, executor):
        """Execute a single job"""
        try:
            job.status = JobStatus.RUNNING
            job.started_at = datetime.utcnow()
            logger.info(f"Starting job {job.id}")
            
            # Execute the workflow
            result = await executor.execute_workflow(job.workflow_json)
            
            # Update job
            job.status = JobStatus.COMPLETED
            job.progress = 1.0
            job.result = result
            job.completed_at = datetime.utcnow()
            logger.info(f"Job {job.id} completed successfully")
            
        except asyncio.CancelledError:
            job.status = JobStatus.CANCELLED
            job.completed_at = datetime.utcnow()
            logger.info(f"Job {job.id} was cancelled")
            
        except Exception as e:
            job.status = JobStatus.FAILED
            job.error = str(e)
            job.completed_at = datetime.utcnow()
            logger.error(f"Job {job.id} failed: {e}")
            
        finally:
            # Clean up
            if job.id in self._running_tasks:
                del self._running_tasks[job.id]

# Global job queue instance
_job_queue: Optional[JobQueue] = None

def get_job_queue() -> JobQueue:
    """Get the global job queue instance"""
    global _job_queue
    if _job_queue is None:
        _job_queue = JobQueue()
    return _job_queue
