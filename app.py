import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Image Text Editor", layout="wide")

# -----------------------------
# SESSION STATE
# -----------------------------
if "final_img" not in st.session_state:
    st.session_state.final_img = None

# -----------------------------
# TITLE
# -----------------------------
st.title("🖼️ Image Text Editor (Urdu + English)")

# -----------------------------
# IMAGE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_container_width=True)

    # -----------------------------
    # TEXT INPUT
    # -----------------------------
    text = st.text_area("Enter Text (Urdu / English)")

    # -----------------------------
    # TEXT SETTINGS
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        font_size = st.slider("Font Size", 20, 200, 60)

    with col2:
        x_pos = st.slider("Position X", 0, image.width, 50)

    with col3:
        y_pos = st.slider("Position Y", 0, image.height, 50)

    text_color = st.color_picker("Text Color", "#ffffff")

    # -----------------------------
    # GENERATE BUTTON
    # -----------------------------
    if st.button("✅ Generate Image"):
        img_copy = image.copy()
        draw = ImageDraw.Draw(img_copy)

        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        draw.text((x_pos, y_pos), text, fill=text_color, font=font)

        st.session_state.final_img = img_copy

    # -----------------------------
    # SHOW RESULT
    # -----------------------------
    if st.session_state.final_img:
        st.image(st.session_state.final_img, caption="Final Image", use_container_width=True)

        buf = io.BytesIO()
        st.session_state.final_img.save(buf, format="PNG")

        st.download_button(
            "⬇ Download Image",
            buf.getvalue(),
            file_name="edited_image.png",
            mime="image/png"
        )
