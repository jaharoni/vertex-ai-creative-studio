# Add this to main.py startup
import asyncio
from services.workflows.job_queue import get_job_queue

# In app startup (add to __main__ or setup function):
job_queue = get_job_queue()
asyncio.create_task(job_queue.start())
