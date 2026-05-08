import streamlit as st
from PIL import Image
import numpy as np

st.title("🧪 Auto pH Detector")

# THE BRAIN: 0-14 Universal Scale
PH_SCALE = {
    0: (230, 0, 0),    1: (255, 30, 0),   2: (255, 80, 0),
    3: (255, 140, 0),  4: (255, 200, 0),  5: (255, 230, 0),
    6: (200, 255, 0),  7: (50, 230, 50),  8: (0, 200, 100),
    9: (0, 180, 180),  10: (0, 120, 230), 11: (0, 50, 200),
    12: (80, 0, 180),  13: (130, 0, 150), 14: (60, 0, 80)
}

uploaded_file = st.file_uploader("Upload a CLEAR, cropped photo of just the pH strip color", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file).convert('RGB')
    st.image(img, caption="Targeting the center of this photo...", use_container_width=True)
    
    # Logic: Get the color of the pixel in the dead center of the photo
    width, height = img.size
    center_pixel = img.getpixel((width // 2, height // 2))
    r, g, b = center_pixel
    
    st.write(f"**Detected Color at Center:** RGB({r}, {g}, {b})")
    
    # Compare detected color to our database
    user_rgb = np.array((r, g, b))
    best_ph = min(PH_SCALE.keys(), key=lambda x: np.linalg.norm(user_rgb - np.array(PH_SCALE[x])))
    
    st.divider()
    st.header(f"Detected pH Level: {best_ph}")
    
    if best_ph < 7:
        st.error("Result: ACIDIC")
    elif best_ph > 7:
        st.info("Result: BASIC")
    else:
        st.success("Result: NEUTRAL")

