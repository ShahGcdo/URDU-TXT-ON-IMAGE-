def load_font(size):
    font_path = os.path.join("fonts", "NotoNastaliqUrdu-VariableFont_wght.ttf")

    if not os.path.exists(font_path):
        st.warning("⚠️ Font file missing.")
        return ImageFont.load_default()

    try:
        # Try loading variable font normally
        font = ImageFont.truetype(font_path, size)
        return font

    except Exception as e:
        st.warning(f"⚠️ Variable font failed, trying fallback... ({e})")

        try:
            # Try with layout engine (fix for some environments)
            font = ImageFont.truetype(font_path, size, layout_engine=ImageFont.LAYOUT_BASIC)
            return font
        except:
            st.error("❌ Variable font not supported. Use static font instead.")
            return ImageFont.load_default()
