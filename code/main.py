import subprocess
import streamlit as st
import os
import pandas as pd

# Add a logo to the Streamlit app
st.markdown(
    """
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h1 style="margin: 0;">RegMind - Regulatory Reporting Made Easy</h1>
        <img src="src/resources/logo.png" width="100" alt="RegMind Logo">
    </div>
    """,
    unsafe_allow_html=True
)

# Custom CSS to enhance the UI with a white and blue theme and remove white space
st.markdown(
    """
    <style>
    .css-18e3th9, .css-1d391kg, .css-1v3fvcr {
        padding: 0;
    }
    .css-18e3th9 {
        background-color: white;
    }
    .stButton>button {
        background-color: #007BFF;
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        color: white; /* Ensure text color remains white on hover */
    }
    .stProgress > div > div > div > div {
        background-color: #007BFF;
    }
    .stFileUploader {
        border: 2px dashed #007BFF;
        border-radius: 8px;
        padding: 10px;
    }
    .stFileUploader:hover {
        border-color: #0056b3;
    }
    .dataframe-container {
        overflow-x: auto;
        overflow-y: auto;
        background-color: white;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
        max-height: 400px; /* Set a fixed height for vertical scrolling */
    }
    .dataframe-container table {
        width: 100%;
    }
    .dataframe-container th {
        text-align: center;
    }
    .stMarkdown {
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'processing_done' not in st.session_state:
    st.session_state.processing_done = False

# Function to save uploaded file with a new name and path
def save_uploaded_file(uploaded_file, new_name, new_path):
    try:
        os.makedirs(new_path, exist_ok=True)
        with open(os.path.join(new_path, new_name), "wb") as f:
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
        if save_uploaded_file(uploaded_file1, "Instruction.txt", "src/resources/dataInput"):
            st.session_state.step = 2
            st.query_params = {"step": 2}

# Step 2: Upload Mock Data
if st.session_state.step == 2:
    uploaded_file2 = st.file_uploader("Upload Mock Data (.csv)", type=["csv"], key="file2")
    if uploaded_file2 is not None:
        if save_uploaded_file(uploaded_file2, "train.csv", "src/resources/dataInput"):
            st.session_state.step = 3
            st.query_params = {"step": 3}

# Step 3: Upload Column Descriptions
if st.session_state.step == 3:
    uploaded_file3 = st.file_uploader("Upload Column Descriptions (.txt)", type=["txt"], key="file3")
    if uploaded_file3 is not None:
        if save_uploaded_file(uploaded_file3, "column_instructions.txt", "src/resources/dataInput"):
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
            st.write("Progress:")
            st.code(output)
            st.session_state.processing_done = True

# Display the CSV file in a scrollable table if processing is done
if st.session_state.processing_done:
    csv_file_path = "src/resources/dataOutput/final_anomalies_ui.csv"
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
        st.write("Anomaly Data:")
        
        # Add download button for the whole anomaly data
        whole_anomaly_data_path = "src/resources/dataOutput/final_anomalies.csv"
        if os.path.exists(whole_anomaly_data_path):
            with open(whole_anomaly_data_path, "rb") as file:
                btn = st.download_button(
                    label="Download Whole Anomaly Data",
                    data=file,
                    file_name="whole_anomaly_data.csv",
                    mime="text/csv"
                )
        else:
            st.error("Whole anomaly data file not found.")
        
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.write(df.to_html(index=False, classes='dataframe-container'), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("CSV file not found.")