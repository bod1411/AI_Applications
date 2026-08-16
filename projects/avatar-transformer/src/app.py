import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import base64
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

def analyze_face(image_bytes, mime_type):
    # Use GPT-4o vision to analyze facial features
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:{mime_type};base64,{base64_image}"
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe the facial features in this selfie for a cartoon transformation."},
                {"type": "image_url", "image_url": {"url": data_url}}
            ]
        }
    ]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=200
    )
    return response.choices[0].message.content

def generate_avatar(image_bytes, style="anime"):
    # Use DALL-E to generate a cartoon/anime avatar
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    prompt = f"Create a high-quality {style} cartoon avatar based on this selfie. Keep the main facial features and pose."
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="512x512",
        response_format="url",
        image={"data": base64_image}
    )
    return response.data[0].url

st.title("Avatar Transformer")
st.write("Upload a selfie to generate a cartoon/anime avatar!")

uploaded_file = st.file_uploader("Upload a selfie (jpg/png)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image_bytes = uploaded_file.read()
    mime_type = uploaded_file.type  # e.g., "image/jpeg"
    image = Image.open(io.BytesIO(image_bytes))
    st.image(image, caption="Original Selfie", use_column_width=True)

    if st.button("Analyze & Transform"):
        with st.spinner("Analyzing facial features..."):
            features = analyze_face(image_bytes, mime_type)
            st.subheader("Facial Feature Analysis")
            st.write(features)

        with st.spinner("Generating cartoon/anime avatar..."):
            avatar_url = generate_avatar(image_bytes, style="anime")
            st.subheader("Cartoon/Anime Avatar")
            st.image(avatar_url, caption="Your Avatar", use_column_width=True)