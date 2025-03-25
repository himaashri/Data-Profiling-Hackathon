# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
In the banking sector, data profiling is a critical process that ensures the accuracy, consistency, and compliance of data used for decision-making, risk management, and reporting. From regulatory reporting to fraud detection, credit risk analysis, and transaction monitoring, banks rely on high-quality data to meet operational and compliance requirements. However, traditional data profiling methods are often manual, time-consuming, and prone to errors, making them inefficient for handling the growing complexity and volume of financial data.

This project introduces an AI-powered data profiling solution designed specifically for the banking industry. By leveraging Generative AI (LLMs) and unsupervised machine learning techniques, the solution automates the entire data profiling pipeline. It extracts validation rules from financial instructions, generates executable Python code for data validation, detects anomalies in datasets, and suggests remediation actions for flagged transactions.

The solution is not limited to regulatory reporting but extends to other critical banking use cases, such as fraud detection, transaction monitoring, and credit risk profiling. With its modular design, scalability, and explainability, this solution empowers banks to ensure data quality, improve operational efficiency, and make informed decisions in a rapidly evolving financial landscape.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)

## 💡 Inspiration
The banking sector relies heavily on accurate and consistent data for decision-making, compliance, and risk management. However, traditional data profiling methods are manual, time-consuming, and prone to errors, making them inefficient for handling the growing complexity and volume of financial data. 

This project was inspired by the need to automate and streamline data profiling processes using cutting-edge technologies like Generative AI (LLMs) and unsupervised machine learning. By addressing challenges such as anomaly detection, validation rule generation, and remediation suggestions, this solution aims to empower banks to ensure data quality, improve operational efficiency, and meet compliance requirements with ease.

## ⚙️ What It Does
The project implements an end-to-end pipeline for data profiling, anomaly detection, and reporting. Below is the detailed step-by-step process:

### Step 1: Configuration Management
**Objective:** Centralize all file paths, parameters, and settings for easy management.  
**Implementation:**  
- The `config.yml` file stores paths for input/output files, model parameters, and other configurations.  
- The `ConfigLoader` class reads the configuration file and provides access to the required parameters.

### Step 2: Prompt Preparation for Validation Code
**Objective:** Automate the generation of Python validation code using an LLM.  
**Implementation:**  
- **Input Files:**
  - `prompt.txt`: Base prompt for generating validation code.
  - `Instruction.txt`: Contains validation rules derived from regulatory instructions.
  - `column_instructions.txt`: Describes the columns in the dataset.
- **Process:**
  - The `append_file_contents_to_prompt` function combines the above files into a single prompt (`final_prompt.txt`).
  - The `get_gemini_response` function uses the Google Generative AI (Gemini) model to generate Python validation code based on the prompt.
  - The generated code is saved to `validations.py`.

### Step 3: Data Validation
**Objective:** Validate the anomalies dataset based on the generated validation rules.  
**Implementation:**  
- The `process_anomalies_dataset` function in `validations.py`:
  - Reads the anomalies dataset (CSV file).
  - Applies validation rules (e.g., checking valid identifier types, rounding numeric values, ensuring valid date formats).
  - Adds validation messages to a new column (`Validation_Messages`) in the dataset.
  - Saves the processed dataset to a new file.

### Step 4: Data Preprocessing
**Objective:** Prepare the dataset for anomaly detection by cleaning and transforming the data.  
**Implementation:**  
- The `ModelTraining` class handles preprocessing:
  - **Handle Missing Values:** Drop columns with >90% missing data and impute others.
  - **Feature Selection:** Remove low-variance numerical features and single-value features.
  - **Encoding:** Encode categorical features using frequency ranking.
  - **Date-Time Features:** Convert date-time columns into multiple components (e.g., year, month, day).

### Step 5: Anomaly Detection
**Objective:** Identify anomalies in the dataset using clustering algorithms.  
**Implementation:**  
- The DBSCAN algorithm is used for anomaly detection.
- If PCA is enabled, dimensionality reduction is applied to retain 90% of the variance.
- The model is trained on the processed dataset, and predictions are saved to an output file.

### Step 6: Anomaly Verification
**Objective:** Verify and save the anomalies detected by the model.  
**Implementation:**  
- The `VerifyAnomalies` class:
  - Reads the anomalies dataset and applies the validation rules using the `process_anomalies_dataset` function.
  - Saves the verified anomalies to a final output file.

### Step 7: Report Generation
**Objective:** Generate a comprehensive report summarizing the validation and anomaly detection results.  
**Implementation:**  
- The `RegulatoryReportingFactory` class orchestrates the entire pipeline:
  - Calls the prompt generation, validation, model training, and anomaly verification modules in sequence.
  - Generates the final report.

## 🛠️ How We Built It
Briefly outline the technologies, frameworks, and tools used in development.

## 🚧 Challenges We Faced
Describe the major technical or non-technical challenges your team encountered.

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/your-repo.git
   ```
2. Install dependencies  
   ```sh
   npm install  # or pip install -r requirements.txt (for Python)
   ```
3. Run the project  
   ```sh
   npm start  # or python app.py
   ```


## 🏗️ Tech Stack

## Programming Language:
- **Python**: The entire pipeline is implemented in Python.

## Libraries and Frameworks:
### Data Processing:
- **pandas**: For data manipulation and preprocessing.
- **numpy**: For numerical computations.

### Machine Learning:
- **scikit-learn**: For PCA, DBSCAN, and clustering.

### Visualization:
- **matplotlib**: For visualizing clustering results.

### Generative AI:
- **google.generativeai**: For generating validation code using the Gemini model.

### Configuration Management:
- **PyYAML**: For reading the YAML configuration file.

## File Formats:
- **YAML**: For configuration management (config.yml).
- **CSV**: For input and output datasets.
- **TXT**: For prompts and instructions.

## Tools:
- **Visual Studio Code**: IDE for development.

## 👥 Team
- **Himasree** - [GitHub](#) | [LinkedIn](#)
- **Talveen** - [GitHub](#) | [LinkedIn](#)
- **Subhojit** - [GitHub](#) | [LinkedIn](#)
- **Venkat** - [GitHub](#) | [LinkedIn](#)
- **Naveen** - [GitHub](#) | [LinkedIn](#)
````
