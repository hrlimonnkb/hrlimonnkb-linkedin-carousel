# LinkedIn Carousel Maker with Streamlit, Azure OpenAI, and Pillow

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from openai import AzureOpenAI
import os

# --- Load secrets from .streamlit/secrets.toml ---
client = AzureOpenAI(
    api_key=st.secrets["AZURE_API_KEY"],
    api_version="2023-03-15-preview",
    azure_endpoint=st.secrets["AZURE_ENDPOINT"]
)

deployment_name = st.secrets["AZURE_DEPLOYMENT"]

# --- Paths ---
TEMPLATE_IMAGE_PATH = "template/template.png"
AI_ICON_PATH = "icons/ai.png"
SWIPE_ICON_PATH = "icons/swipe.png"
FONT_BOLD_PATH = "fonts/Roboto-Bold.ttf"
FONT_REGULAR_PATH = "fonts/Roboto-Regular.ttf"
SLIDES_DIR = "slides"

# --- Generate Carousel Content using Azure OpenAI ---
def generate_carousel_content(hint):
    prompt = f"""
    You are an expert at writing LinkedIn carousel slides.
    Based on the topic: '{hint}', generate 6 slides with:
    - A short, catchy title
    - 2–3 lines of professional, helpful content.
    Respond in JSON format:
    [{{"title": "...", "content": "..."}}, ...]
    """

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800
    )

    return eval(response.choices[0].message.content)

# --- Create a Single Slide ---
def create_slide(slide_data, slide_number):
    img = Image.open(TEMPLATE_IMAGE_PATH).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # Load fonts
    title_font = ImageFont.truetype(FONT_BOLD_PATH, 64)
    content_font = ImageFont.truetype(FONT_REGULAR_PATH, 42)

    # Draw text
    draw.text((80, 180), slide_data['title'], font=title_font, fill="black")
    draw.text((80, 300), slide_data['content'], font=content_font, fill="gray")

    # Paste AI icon
    ai_icon = Image.open(AI_ICON_PATH).resize((80, 80)).convert("RGBA")
    img.paste(ai_icon, (950, 40), ai_icon)

    # Last slide has swipe icon
    if slide_number == 6:
        swipe_icon = Image.open(SWIPE_ICON_PATH).resize((100, 100)).convert("RGBA")
        img.paste(swipe_icon, (900, 900), swipe_icon)

    # Save image
    os.makedirs(SLIDES_DIR, exist_ok=True)
    path = f"{SLIDES_DIR}/slide{slide_number}.png"
    img.save(path)
    return path

# --- Streamlit UI ---
st.set_page_config(page_title="LinkedIn Carousel Maker", layout="centered")
st.title("🖼️ LinkedIn Carousel Maker")
st.markdown("Generate beautiful carousels with AI, instantly!")

hint = st.text_input("🔤 Enter a content hint (e.g. '5 Tips for Productivity')")

if st.button("🚀 Generate Carousel") and hint:
    if not os.path.exists(SLIDES_DIR):
        os.makedirs(SLIDES_DIR)

    with st.spinner("Generating with AI..."):
        try:
            slides = generate_carousel_content(hint)
            paths = []
            for i, slide in enumerate(slides, 1):
                path = create_slide(slide, i)
                paths.append(path)
            st.success("✅ Slides generated successfully!")
            for p in paths:
                st.image(p, use_column_width=True)
        except Exception as e:
            st.error(f"❌ Error: {e}")
