import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import arabic_reshaper
from bidi.algorithm import get_display
import os

st.set_page_config(page_title="Image Text Editor PRO", layout="wide")

if "final_img" not in st.session_state:
    st.session_state.final_img = None

# -----------------------------
# LOAD FONT
# -----------------------------
def load_font(size):
    font_path = "fonts/NotoNastaliqUrdu-Regular.ttf"

    if os.path.exists(font_path):
        return ImageFont.truetype(font_path, size)
    else:
        st.warning("⚠️ Urdu font not found! Upload font in /fonts folder")
        return ImageFont.load_default()

# -----------------------------
# TITLE
# -----------------------------
st.title("🖼️ Image Text Editor PRO (Urdu + English)")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    # SMALL PREVIEW
    st.image(image, caption="Original Image", width=400)

    text = st.text_area("Enter Text (Urdu / English)")

    col1, col2, col3 = st.columns(3)

    with col1:
        font_size = st.slider("Font Size", 20, 200, 60)

    with col2:
        x_pos = st.slider("Position X", 0, image.width, 50)

    with col3:
        y_pos = st.slider("Position Y", 0, image.height, 50)

    text_color = st.color_picker("Text Color", "#ffffff")

    if st.button("✅ Generate Image"):
        img_copy = image.copy()
        draw = ImageDraw.Draw(img_copy)

        font = load_font(font_size)

        # ✅ Proper Urdu handling
        if text.strip() != "":
            try:
                reshaped = arabic_reshaper.reshape(text)
                bidi_text = get_display(reshaped)
            except:
                bidi_text = text
        else:
            bidi_text = ""

        draw.text((x_pos, y_pos), bidi_text, fill=text_color, font=font)

        st.session_state.final_img = img_copy

    if st.session_state.final_img:
        st.image(st.session_state.final_img, caption="Final Image", width=400)

        buf = io.BytesIO()
        st.session_state.final_img.save(buf, format="PNG")

        st.download_button(
            "⬇ Download Image",
            buf.getvalue(),
            file_name="edited_image.png",
            mime="image/png"
        )
