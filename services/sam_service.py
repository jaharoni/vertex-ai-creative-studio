"""SAM segmentation service stub."""

class SAMService:
    """Segment Anything Model service."""
    
    async def segment_image(self, image_url: str, prompt: str = None):
        """Segment image using SAM."""
        # TODO: Implement SAM integration
        return {"masks": [], "segments": []}
