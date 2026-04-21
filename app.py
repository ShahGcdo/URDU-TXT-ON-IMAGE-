import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import arabic_reshaper
from bidi.algorithm import get_display
import os

st.set_page_config(page_title="Image Text Editor PRO", layout="wide")

# -----------------------------
# SESSION STATE
# -----------------------------
if "final_img" not in st.session_state:
    st.session_state.final_img = None

# -----------------------------
# SAFE FONT LOADER (NO CRASH)
# -----------------------------
def load_font(size):
    font_path = os.path.join("fonts", "NotoNastaliqUrdu-Regular.ttf")

    if not os.path.exists(font_path):
        st.warning("⚠️ Font file missing. Using default font.")
        return ImageFont.load_default()

    try:
        return ImageFont.truetype(font_path, size)
    except Exception as e:
        st.error(f"❌ Font load failed: {e}")
        return ImageFont.load_default()

# -----------------------------
# TEXT PROCESS (URDU FIX)
# -----------------------------
def process_text(text):
    try:
        reshaped = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped)
        return bidi_text
    except:
        return text

# -----------------------------
# UI
# -----------------------------
st.title("🖼️ Image Text Editor PRO (Urdu + English)")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    # ✅ SMALL PREVIEW
    st.image(image, caption="Original Image", width=350)

    text = st.text_area("Enter Text (Urdu / English)")

    col1, col2, col3 = st.columns(3)

    with col1:
        font_size = st.slider("Font Size", 20, 200, 60)

    with col2:
        x_pos = st.slider("Position X", 0, image.width, 50)

    with col3:
        y_pos = st.slider("Position Y", 0, image.height, 50)

    text_color = st.color_picker("Text Color", "#ffffff")

    # DEBUG (you can remove later)
    st.write("Font file exists:", os.path.exists("fonts/NotoNastaliqUrdu-Regular.ttf"))

    # -----------------------------
    # GENERATE
    # -----------------------------
    if st.button("✅ Generate Image"):
        img_copy = image.copy()
        draw = ImageDraw.Draw(img_copy)

        font = load_font(font_size)
        final_text = process_text(text)

        draw.text((x_pos, y_pos), final_text, fill=text_color, font=font)

        st.session_state.final_img = img_copy

    # -----------------------------
    # RESULT
    # -----------------------------
    if st.session_state.final_img:
        st.image(st.session_state.final_img, caption="Final Image", width=350)

        buf = io.BytesIO()
        st.session_state.final_img.save(buf, format="PNG")

        st.download_button(
            "⬇ Download Image",
            buf.getvalue(),
            file_name="edited_image.png",
            mime="image/png"
        )
