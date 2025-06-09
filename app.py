import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("SceneDetect: Narrating Your World")

# Function to analyze an image by sending it to the FastAPI backend
def analyze_image(image_file):
    # Display the uploaded image
    st.image(image_file, caption="Uploaded Image", use_container_width=True)
    st.write("Analyzing the image...")

    # Convert image file to bytes
    image_bytes = image_file.read()
    files = {"file": ("image.jpg", image_bytes, "image/jpeg")}

    # API endpoint
    api_url = "http://127.0.0.1:8000/analyze"

    try:
        # Send POST request to the FastAPI backend
        response = requests.post(api_url, files=files)
        response.raise_for_status()  # Raise an error if the request fails
        data = response.json()

        # Display the results
        if data["success"]:
            st.write("### **Description:**")
            st.write(data["analysis"]["description"])

            st.write("### **Objects Detected:**")
            st.write(", ".join(data["analysis"]["objects"]) if data["analysis"]["objects"] else "None detected.")

            st.write("### **Tags:**")
            st.write(", ".join(data["analysis"]["tags"]) if data["analysis"]["tags"] else "None detected.")

            # Play the audio if generated
            if "audio_url" in data:
                st.audio(data["audio_url"], format="audio/wav", start_time=0)
        else:
            st.error("Error in analysis. Please try again.")

    except requests.exceptions.RequestException as e:
        st.error(f"success")

# Upload file section
st.subheader("Upload an image to analyze:")
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    analyze_image(uploaded_file)
