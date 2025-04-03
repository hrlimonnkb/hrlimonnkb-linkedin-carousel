# LinkedIn Carousel Maker with Streamlit, Azure OpenAI, and PDF Export

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from openai import AzureOpenAI
from fpdf import FPDF
import os
import json
import textwrap

# --- Load secrets from .streamlit/secrets.toml ---
client = AzureOpenAI(
    api_key=st.secrets["AZURE_API_KEY"],
    api_version="2023-03-15-preview",
    azure_endpoint=st.secrets["AZURE_ENDPOINT"]
)

deployment_name = st.secrets["AZURE_DEPLOYMENT"]

# --- Paths ---
AI_ICON_PATH = "icons/ai.png"
SWIPE_ICON_PATH = "icons/swipe.png"
FONT_BOLD_PATH = "fonts/Roboto-Bold.ttf"
FONT_REGULAR_PATH = "fonts/Roboto-Regular.ttf"
OUTPUT_PDF = "slides/carousel_output.pdf"

# --- Generate Carousel Content using Azure OpenAI ---
def generate_carousel_content(hint):
    prompt = f"""
    You are an expert at writing LinkedIn carousel slides.
    Based on the topic: '{hint}', generate exactly 6 slides with:
    - A short, catchy title
    - 2–3 lines of helpful, friendly content.

    Additionally:
    - Write a relevant, punchy title for the whole carousel (max 8 words)
    - Write a subtitle for the cover slide (1 line only)
    - Write a short CTA message to be used in the last slide (1–2 lines)

    Respond ONLY in valid JSON format like this:
    {{
      "cover_title": "Main Big Title",
      "cover_subtitle": "One line subtitle",
      "slides": [
        {{"title": "Slide 1 title", "content": "Line 1. Line 2."}},
        ...
      ],
      "cta": "Final call to action text."
    }}
    """

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )

    return json.loads(response.choices[0].message.content)

# --- Create PDF Slide ---
def draw_gradient_background(draw, width, height):
    for y in range(height):
        gradient = int(20 + (y / height) * 80)
        draw.line([(0, y), (width, y)], fill=(gradient, gradient, gradient))

# --- Generate PDF ---
def generate_pdf(data):
    pdf = FPDF(format=(1080, 1080), unit="pt")
    os.makedirs("slides", exist_ok=True)

    cover_title = data["cover_title"]
    cover_subtitle = data.get("cover_subtitle", "")
    slides = data["slides"]
    cta_text = data["cta"]

    # --- Add Cover Slide ---
    pdf.add_page()
    cover = Image.new("RGB", (1080, 1080), color="#141414")
    draw = ImageDraw.Draw(cover)
    draw_gradient_background(draw, 1080, 1080)

    cover_font = ImageFont.truetype(FONT_BOLD_PATH, 80)
    sub_font = ImageFont.truetype(FONT_REGULAR_PATH, 46)
    wrapped = textwrap.wrap(cover_title, width=20)
    for i, line in enumerate(wrapped):
        draw.text((100, 300 + i * 90), line, font=cover_font, fill="white")
    draw.text((100, 550 + len(wrapped) * 40), cover_subtitle, font=sub_font, fill="lightgray")

    try:
        swipe_icon = Image.open(SWIPE_ICON_PATH).resize((80, 80)).convert("RGBA")
        cover.paste(swipe_icon, (500, 950), swipe_icon)
    except:
        pass

    cover.save("slides/cover.jpg")
    pdf.image("slides/cover.jpg", x=0, y=0, w=1080, h=1080)

    # --- Add Content Slides ---
    for i, slide in enumerate(slides, start=1):
        pdf.add_page()
        canvas = Image.new("RGB", (1080, 1080), color="#141414")
        draw = ImageDraw.Draw(canvas)
        draw_gradient_background(draw, 1080, 1080)

        title_font = ImageFont.truetype(FONT_BOLD_PATH, 72)
        content_font = ImageFont.truetype(FONT_REGULAR_PATH, 42)
        number_font = ImageFont.truetype(FONT_BOLD_PATH, 130)

        draw.text((80, 60), str(i), font=number_font, fill="gray")

        text_x = 100
        title_y = 300
        content_y = 440
        max_width = 880

        wrapped_title = textwrap.wrap(slide['title'], width=26)
        for j, line in enumerate(wrapped_title):
            draw.text((text_x, title_y + j * 75), line, font=title_font, fill="white")
        content_y += len(wrapped_title) * 75

        wrapped_content = textwrap.wrap(slide['content'], width=48)
        for j, line in enumerate(wrapped_content):
            draw.text((text_x, content_y + j * 55), line, font=content_font, fill="lightgray")

        try:
            ai_icon = Image.open(AI_ICON_PATH).resize((70, 70)).convert("RGBA")
            canvas.paste(ai_icon, (970, 40), ai_icon)
        except:
            pass

        temp_path = f"slides/temp_slide_{i}.jpg"
        canvas.save(temp_path)
        pdf.image(temp_path, x=0, y=0, w=1080, h=1080)

    # --- Add CTA Slide ---
    pdf.add_page()
    cta = Image.new("RGB", (1080, 1080), color="#141414")
    draw = ImageDraw.Draw(cta)
    draw_gradient_background(draw, 1080, 1080)

    cta_title = ImageFont.truetype(FONT_BOLD_PATH, 72)
    cta_sub = ImageFont.truetype(FONT_REGULAR_PATH, 44)

    wrapped_cta = textwrap.wrap(cta_text, width=30)
    for i, line in enumerate(wrapped_cta):
        draw.text((120, 420 + i * 70), line, font=cta_title, fill="white")

    draw.text((120, 650), "💬 Like, Comment & Share if useful!", font=cta_sub, fill="lightgray")

    cta.save("slides/cta.jpg")
    pdf.image("slides/cta.jpg", x=0, y=0, w=1080, h=1080)

    pdf.output(OUTPUT_PDF)
    return OUTPUT_PDF

# --- Streamlit UI ---
st.set_page_config(page_title="LinkedIn Carousel Maker", layout="centered")
st.title("🖼️ LinkedIn Carousel Maker by Habib")
st.markdown("Generate beautiful carousels with AI, instantly!")

hint = st.text_input("🔤 Enter a content hint (e.g. '5 Tips for Productivity')")

if st.button("🚀 Generate Carousel") and hint:
    with st.spinner("Generating with AI..."):
        try:
            data = generate_carousel_content(hint)
            pdf_path = generate_pdf(data)
            st.success("✅ Slides generated and combined into a single PDF!")
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download Carousel PDF", f, file_name="LinkedIn_Carousel.pdf")
        except Exception as e:
            st.error(f"❌ Error: {e}")