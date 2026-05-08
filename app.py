import streamlit as st
from PIL import Image
import numpy as np

st.title("🧪 Easy pH Color Detector")
st.write("Upload a photo of your pH strip and enter the RGB values to get the result.")

# Database of pH colors
PH_DATA = {
    1: (230, 50, 50),   
    7: (50, 180, 50),   
    13: (100, 50, 150)  
}

uploaded_file = st.file_uploader("Choose a photo...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Your pH Strip", use_container_width=True)
    
    st.subheader("Enter RGB values from Digital Color Meter:")
    col1, col2, col3 = st.columns(3)
    with col1:
        r = st.number_input("Red (R)", 0, 255, 128)
    with col2:
        g = st.number_input("Green (G)", 0, 255, 128)
    with col3:
        b = st.number_input("Blue (B)", 0, 255, 128)
    
    user_color = np.array((r, g, b))
    distances = {ph: np.linalg.norm(user_color - np.array(color)) for ph, color in PH_DATA.items()}
    best_ph = min(distances, key=distances.get)
    
    st.divider()
    if best_ph < 7:
        st.error(f"Result: This is an ACID (Estimated pH: {best_ph})")
    elif best_ph > 7:
        st.info(f"Result: This is a BASE (Estimated pH: {best_ph})")
    else:
        st.success(f"Result: This is NEUTRAL (pH: 7)")