# 🖼️ LinkedIn Carousel Maker with AI (Streamlit + Azure OpenAI)

Generate professional, eye-catching LinkedIn carousel posts with just a **content hint**. This Streamlit-powered tool uses **Azure OpenAI** to generate engaging slides and renders them with custom design, AI icons, and swipe indicators.

---

## 🚀 Features

✅ Input a single idea or topic  
✅ Generate 6-slide carousel content using Azure OpenAI  
✅ Beautiful slide designs using Pillow  
✅ Auto-embedded AI and Swipe icons  
✅ Instant preview inside the browser  
✅ Save slides as PNG (Ready for LinkedIn)

---

## 🛠️ Tech Stack

- Python 🐍
- Streamlit 🌐
- Azure OpenAI 💡
- Pillow (PIL) 🖼️
- GitHub + Streamlit Cloud 🌥️

---

## 📸 Preview

![Carousel Demo](https://linkedin-carousels.streamlit.app/)

---

## 🧠 How It Works

1. Enter a topic (e.g. `"7 Tips for Building a Personal Brand"`)
2. The AI generates 6 slides with catchy titles & engaging text
3. Each slide is styled using a custom template with icons
4. Download and upload to LinkedIn as a carousel post

---

## 🧪 Local Setup

```bash
git clone https://github.com/hrlimonnkb/linkedin-carousel-streamlit.git
cd linkedin-carousel-streamlit
pip install -r requirements.txt
streamlit run carousel_maker.py
🔐 Azure OpenAI Setup
Set your credentials in carousel_maker.py:


openai.api_type = "azure"
openai.api_base = "https://YOUR_RESOURCE_NAME.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = "YOUR_API_KEY"
deployment_name = "YOUR_DEPLOYMENT_NAME"


☁️ Deploy to Streamlit Cloud
    Go to Streamlit Cloud
    Click New App
    Connect this repo
    Set main file to: carousel_maker.py
    Deploy & enjoy 🎉

👨‍💻 Author
Habibur Rahman
🔗 hrlimon.com
🐦 @habibsoft
