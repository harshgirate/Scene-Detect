# Scene-Detect
Scene Detect is a tool where you upload an image, and it provides an audio description of that image. This helps users understand the content of the image through spoken words, making it useful for accessibility and quick image summaries.

Scene Detect is an easy-to-use application that allows users to upload an image and receive an audio description of the image content. This project aims to enhance accessibility by providing spoken descriptions, making images more understandable for visually impaired users or anyone who prefers audio summaries.

# Features
Upload any image and get an instant audio description.

Helps with accessibility by converting visual information into speech.

Simple and intuitive interface for quick image analysis.

# How It Works
The app uses Microsoft Azure cognitive services and text to speech to understand the image and give an audio description to user.

# Initialization
*install dependencies*
pip install -r requirements.txt

*add keys and endpoints to .env file*
AZURE_COMPUTER_VISION_KEY=

AZURE_COMPUTER_VISION_ENDPOINT=

AZURE_SPEECH_KEY=

AZURE_SPEECH_REGION=

# Future updates
*Future Updates: The project will be expanded to support both images and videos, providing audio descriptions for video content as well as images to enhance usability and accessibility.*
