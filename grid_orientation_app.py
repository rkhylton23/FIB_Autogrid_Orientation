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
st.set_page_config(
    page_title="FIB₂TEM: Grid Orientation Assistant",
    page_icon="autogrid_32x32.png",
    layout="centered",
)

st.title("FIB₂TEM: Grid Orientation Assistant")

st.write("""
This tool helps you determine the correct orientation for loading your grid into the cassette and the Titan Krios stage tilt angle.
""")

# User Inputs
notch_direction = st.selectbox("1. Select the notch direction in the FIB Shuttle:", 
                               ["Up", "Up-Right", "Right", "Down-Right", "Down", "Down-Left", "Left", "Up-Left"])

# Lamellae Location Section
st.write("2. Select the lamellae location:")
lamellae_bottom_right = st.checkbox("Lamellae in Bottom-right (Normal Load)")
lamellae_top_left = st.checkbox("Lamellae in Top-left (Reverse Load)")

# Validate Lamellae Selection
if lamellae_bottom_right and lamellae_top_left:
    st.error("Please select only one lamella location.")
elif lamellae_bottom_right:
    lamellae_location = "bottom-right"
elif lamellae_top_left:
    lamellae_location = "top-left"

# Shuttle Type Section
st.write("3. Select the shuttle type:")
shuttle_45 = st.checkbox("45° Shuttle")
shuttle_35 = st.checkbox("35° Shuttle")

# Validate Shuttle Type Selection
if shuttle_45 and shuttle_35:
    st.error("Please select only one shuttle type.")
elif shuttle_45:
    shuttle_type = "45"
elif shuttle_35:
    shuttle_type = "35"

# Milling Angle Input
milling_angle = st.number_input("4. Enter the milling angle (degrees):", min_value=0, max_value=90, step=1, value=10)

# Run logic if everything is valid
if st.button("Calculate"):
    if not (lamellae_bottom_right or lamellae_top_left) or not (shuttle_45 or shuttle_35):
        st.error("Please fix the above errors before calculating.")
    else:
        cassette_notch, krios_notch, krios_stage_tilt = determine_grid_orientation(
            notch_direction, lamellae_location, milling_angle, shuttle_type
        )

        # Display Results
        st.subheader("Results:")
        st.write(f"**1. Cassette Notch Direction:** {cassette_notch}")
        st.write(f"**2. Krios Stage Notch Direction:** {krios_notch}")
        st.write(f"**3. Krios Stage Tilt Angle:** {krios_stage_tilt:.1f}°")
