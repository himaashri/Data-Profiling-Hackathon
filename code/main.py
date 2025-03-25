import subprocess
import streamlit as st
import os

# Custom CSS to change the background color to white
st.markdown(
    """
    <style>
    .css-18e3th9 {
        background-color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1

# Function to save uploaded file
def save_uploaded_file(uploaded_file, step):
    try:
        with open(os.path.join("src", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return False
    
def run_command():
    # Define the command you want to run in the terminal
    command = "python app.py"
    
    # Run the command in the terminal
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Return the output of the command
    return result.stdout

# Progress stepper
st.markdown(f"### Step {st.session_state.step} of 4")
st.progress(st.session_state.step / 4)

# Step 1: Upload Instructions
if st.session_state.step == 1:
    uploaded_file1 = st.file_uploader("Upload Instructions (.txt)", type=["txt"], key="file1")
    if uploaded_file1 is not None:
        if save_uploaded_file(uploaded_file1, 1):
            st.session_state.step = 2
            st.query_params = {"step": 2}

# Step 2: Upload Mock Data
if st.session_state.step == 2:
    uploaded_file2 = st.file_uploader("Upload Mock Data (.csv)", type=["csv"], key="file2")
    if uploaded_file2 is not None:
        if save_uploaded_file(uploaded_file2, 2):
            st.session_state.step = 3
            st.query_params = {"step": 3}

# Step 3: Upload Column Descriptions
if st.session_state.step == 3:
    uploaded_file3 = st.file_uploader("Upload Column Descriptions (.txt)", type=["txt"], key="file3")
    if uploaded_file3 is not None:
        if save_uploaded_file(uploaded_file3, 3):
            st.session_state.step = 4
            st.query_params = {"step": 4}

# Step 4: Process Data button
if st.session_state.step == 4:
    st.success("All files uploaded successfully!")
    if st.button("Process Data"):
        with st.spinner("Processing..."):
            # Simulate a long-running process
            import time
            time.sleep(3)
            output = run_command()
            st.write("Command Output:")
            st.code(output)