import streamlit as st
import uv
from pint import UnitRegistry

ureg = UnitRegistry()

def convert_units(value, from_unit, to_unit):
    """Convert units while handling temperature conversions separately."""
    try:
        from_unit = from_unit.lower().replace(" ", "_")  # Normalize unit names
        to_unit = to_unit.lower().replace(" ", "_")

        quantity = ureg.Quantity(value, from_unit)

        # Special handling for temperature conversions
        if from_unit in ["celsius", "fahrenheit", "kelvin"] and to_unit in ["celsius", "fahrenheit", "kelvin"]:
            result = quantity.to_reduced_units().to(to_unit)
        else:
            result = quantity.to(to_unit)

        return result.magnitude, result.units
    except Exception as e:
        return None, str(e)

def set_dynamic_theme(theme):
    """Set background and text color dynamically based on selected theme."""
    if theme == "Light Mode":
        bg_color = "#ffffff"
        text_color = "black"
        sidebar_color = "#f0f2f6"  # Light gray sidebar
    else:
        bg_color = "#1E1E1E"  # Dark background
        text_color = "white"
        sidebar_color = "#333333"  # Dark gray sidebar

    st.markdown(
        f"""
        <style>
        body, .stApp {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
        }}
        .sidebar .sidebar-content {{
            background-color: {sidebar_color} !important;
        }}
        h1, h2, h3, h4, h5, h6, p, label, span {{
            color: {text_color} !important;
        }}
        .stButton>button {{
            background-color: #4CAF50; /* Green button */
            color: white !important;
            border-radius: 5px;
        }}
        .stNumberInput input, .stSelectbox div {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    st.set_page_config(page_title="Google Unit Converter", page_icon="🔄", layout="centered")

    # Theme Selector in Sidebar
    theme = st.sidebar.radio("Select Theme", ["Light Mode", "Dark Mode"])
    set_dynamic_theme(theme)  # Apply background and text color dynamically

    st.title("🔄 Google Unit Converter")
    st.write("Easily convert between different units of measurement.")

    categories = ["Length", "Mass", "Temperature", "Time", "Speed", "Volume"]
    selected_category = st.sidebar.selectbox("Choose a Category", categories)

    units = {
        "Length": ["meter", "kilometer", "mile", "inch", "foot", "yard", "centimeter"],
        "Mass": ["gram", "kilogram", "pound", "ounce", "ton"],
        "Temperature": ["celsius", "fahrenheit", "kelvin"],
        "Time": ["second", "minute", "hour", "day"],
        "Speed": ["meter/second", "kilometer/hour", "mile/hour", "foot/second"],
        "Volume": ["liter", "milliliter", "gallon", "cup", "pint"]
    }

    value = st.number_input("Enter Value:", min_value=0.0, step=0.01)
    from_unit = st.selectbox("From Unit", units[selected_category])
    to_unit = st.selectbox("To Unit", units[selected_category])

    if st.button("Convert"):
        result, unit = convert_units(value, from_unit, to_unit)
        if result is not None:
            st.success(f"Converted Value: {result:.4f} {unit}")
        else:
            st.error(f"Conversion Error: {unit}")

if __name__ == "__main__":
    main()
