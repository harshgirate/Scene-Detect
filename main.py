from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from dotenv import load_dotenv
import io
import os

# Load environment variables
load_dotenv()

# Azure Cognitive Services setup
computervision_client = ComputerVisionClient(
    endpoint=os.getenv("AZURE_COMPUTER_VISION_ENDPOINT"),
    credentials=CognitiveServicesCredentials(os.getenv("AZURE_COMPUTER_VISION_KEY"))
)

speech_config = SpeechConfig(
    subscription=os.getenv("AZURE_SPEECH_KEY"),
    region=os.getenv("AZURE_SPEECH_REGION")
)

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_scene(file: UploadFile = File(...)):
    try:
        # Read and analyze image
        image_bytes = await file.read()
        image_stream = io.BytesIO(image_bytes)
        features = [VisualFeatureTypes.description, VisualFeatureTypes.objects, VisualFeatureTypes.tags]
        analysis = computervision_client.analyze_image_in_stream(image_stream, visual_features=features)

        # Extract results
        description = analysis.description.captions[0].text if analysis.description.captions else "No description available."
        objects = [obj.object_property for obj in analysis.objects] if analysis.objects else []
        tags = [tag.name for tag in analysis.tags[:5]] if analysis.tags else []

        # Generate audio
        audio_file_path = "output.wav"
        audio_config = AudioConfig(filename=audio_file_path)
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        synthesis_result = synthesizer.speak_text_async(description).get()

        if synthesis_result.reason != synthesis_result.Reason.SynthesizingAudioCompleted:
            raise HTTPException(status_code=500, detail="Audio generation failed.")

        return {
            "success": True,
            "analysis": {"description": description, "objects": objects, "tags": tags},
            "audio_url": f"http://127.0.0.1:8000/static/{audio_file_path}",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
async def test_endpoint():
    return {"message": "Server is running"}

