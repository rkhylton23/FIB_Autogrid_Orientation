import streamlit as st

# Function to determine grid orientations and Krios tilt
def determine_grid_orientation(notch_direction, lamellae_location, milling_angle, shuttle_type):
    # Fixed circular notch directions
    notch_directions = ["Up", "Up-Right", "Right", "Down-Right", "Down", "Down-Left", "Left", "Up-Left"]

    # Lamellae-based rotation (cassette)
    lamellae_rotation = {"bottom-right": 2, "top-left": -2}  # 90° clockwise = 2 steps, counter = -2 steps
    cassette_rotation = lamellae_rotation[lamellae_location]
    
    # Find cassette notch direction
    start_index = notch_directions.index(notch_direction)
    cassette_index = (start_index + cassette_rotation) % 8
    cassette_notch = notch_directions[cassette_index]

    # Krios stage rotation (90° clockwise from cassette)
    krios_index = (cassette_index + 2) % 8
    krios_notch = notch_directions[krios_index]

    # Krios stage tilt angle
    shuttle_offsets = {"45": 7, "35": 3}
    base_tilt = milling_angle + shuttle_offsets[shuttle_type]
    tilt_sign = 1 if lamellae_location == "bottom-right" else -1
    krios_stage_tilt = base_tilt * tilt_sign

    # Results
    return cassette_notch, krios_notch, krios_stage_tilt

# Streamlit App Interface
st.title("Cryo-ET Grid Orientation Helper")

st.write("""
This tool helps you determine the correct orientation for loading your grid into the cassette and the Titan Krios stage tilt angle.
""")

# User Inputs
notch_direction = st.selectbox("1. Select the notch direction in the FIB Shuttle:", 
                               ["Up", "Up-Right", "Right", "Down-Right", "Down", "Down-Left", "Left", "Up-Left"])

lamellae_location = st.selectbox("2. Select the lamellae location:", ["bottom-right", "top-left"])

milling_angle = st.number_input("3. Enter the milling angle (degrees):", min_value=0, max_value=90, step=1, value=10)

shuttle_type = st.selectbox("4. Select the shuttle type:", ["45", "35"])

# Run logic
if st.button("Calculate"):
    cassette_notch, krios_notch, krios_stage_tilt = determine_grid_orientation(
        notch_direction, lamellae_location, milling_angle, shuttle_type
    )
    
    # Display Results
    st.subheader("Results:")
    st.write(f"**1. Cassette Notch Direction:** {cassette_notch}")
    st.write(f"**2. Krios Stage Notch Direction:** {krios_notch}")
    st.write(f"**3. Krios Stage Tilt Angle:** {krios_stage_tilt:.1f}°")
