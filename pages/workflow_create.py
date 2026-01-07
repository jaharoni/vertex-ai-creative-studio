"""
Workflow Creator UI - Text-to-Video Interface
"""
import streamlit as st
import asyncio
import uuid
from services.workflows.workflow_orchestrator import WorkflowOrchestrator
from services.workflows.job_queue import get_job_queue, JobStatus

def show():
    st.title("🎬 Creative Automation Machine")
    st.markdown("### Transform your ideas into video with AI")
    
    # Text prompt input
    st.markdown("#### 📝 Describe your video")
    prompt = st.text_area(
        "Enter your video concept",
        placeholder="Example: A 30-second commercial for eco-friendly shoes. Opens with sunrise over a forest, shows athletes running on trails, close-ups of sustainable materials, ends with brand logo.",
        height=150
    )
    
    # Advanced settings (collapsible)
    with st.expander("⚙️ Advanced Settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            duration = st.slider("Duration (seconds)", 5, 60, 30)
            style = st.selectbox(
                "Visual Style",
                ["Cinematic", "Documentary", "Abstract", "Minimalist", "Vibrant"]
            )
            
        with col2:
            aspect_ratio = st.selectbox(
                "Aspect Ratio",
                ["16:9 (Landscape)", "9:16 (Vertical)", "1:1 (Square)"]
            )
            video_model = st.selectbox(
                "Video Model",
                ["Veo 2", "Kling 1.6", "Wan Show"]
            )
    
    # Generate button
    if st.button("🎥 Generate Video", type="primary", use_container_width=True):
        if not prompt:
            st.error("Please enter a video concept")
            return
            
        with st.spinner("Submitting job..."):
            try:
                # Create workflow JSON from prompt
                orchestrator = WorkflowOrchestrator()
                workflow_json = asyncio.run(orchestrator.create_workflow_from_prompt(
                    prompt=prompt,
                    duration=duration,
                    style=style.lower()
                ))
                
                # Submit to job queue
                job_queue = get_job_queue()
                job_id = str(uuid.uuid4())
                asyncio.run(job_queue.submit_job(job_id, workflow_json))
                
                st.success(f"✅ Job submitted! Job ID: {job_id}")
                st.info("Your video is being generated. Check the Status page for progress.")
                
                # Show workflow preview
                with st.expander("📋 View Generated Workflow"):
                    st.json(workflow_json)
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Divider
    st.markdown("---")
    
    # Recent jobs
    st.markdown("### 📊 Recent Jobs")
    
    job_queue = get_job_queue()
    jobs = job_queue.list_jobs()
    
    if not jobs:
        st.info("No jobs yet. Create your first video above!")
    else:
        # Show last 5 jobs
        for job in sorted(jobs, key=lambda j: j.created_at, reverse=True)[:5]:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.text(f"Job {job.id[:8]}...")
                    
                with col2:
                    if job.status == JobStatus.COMPLETED:
                        st.success("✅ Complete")
                    elif job.status == JobStatus.RUNNING:
                        st.info("⏳ Running")
                    elif job.status == JobStatus.FAILED:
                        st.error("❌ Failed")
                    elif job.status == JobStatus.QUEUED:
                        st.warning("⏸️ Queued")
                    else:
                        st.text(job.status.value)
                        
                with col3:
                    st.text(f"{int(job.progress * 100)}%")
    
    # Help section
    with st.expander("💡 Tips for Better Results"):
        st.markdown("""
        **Crafting Great Prompts:**
        - Be specific about visual elements, timing, and mood
        - Include scene descriptions: "Opens with...", "Transitions to..."
        - Mention key moments: "Close-up of...", "Wide shot of..."
        - Specify audio needs: "Upbeat music", "Voiceover explaining..."
        
        **Examples:**
        - "60-second tech product demo. Sleek minimalist style. Shows product rotating, UI features, customer testimonials."
        - "15-second social media ad. Vibrant colors. Fast cuts between people using the app, ending with logo reveal."
        - "30-second brand story. Cinematic documentary style. Time-lapse of company growth, founder interviews, team collaboration."
        """)

if __name__ == "__main__":
    show()
