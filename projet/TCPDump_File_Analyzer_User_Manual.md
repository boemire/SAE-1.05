
# **User Manual: TCPDump File Analyzer**

This document provides step-by-step instructions on how to use the **TCPDump File Analyzer**. The program allows you to parse, analyze, and visualize data from a tcpdump log file.

---

## **System Requirements**

- **Python**: Ensure Python 3.6 or later is installed.
- **Dependencies**:
  - Install the required Python libraries using:
    ```bash
    pip install matplotlib
    ```

---

## **Features**

1. Parse tcpdump log files and extract relevant network data.
2. Analyze the extracted data for:
   - Frequent source and destination IPs.
   - Potential port scans.
   - Suspicious UDP traffic.
   - SSH connection attempts.
   - Hourly activity.
3. Generate:
   - A Markdown report (`rapport.md`) summarizing the analysis.
   - A CSV file (`packets.csv`) with all parsed data for further processing in Excel.
   - A pie chart showing the top 5 most frequent source IPs.
4. Provide an intuitive graphical interface for ease of use.

---

## **How to Use**

1. **Launch the Program**:
   - Run the script using:
     ```bash
     python script_name.py
     ```
   - A graphical user interface (GUI) will appear.

2. **Select a tcpdump File**:
   - Click the **Browse** button.
   - Navigate to and select your tcpdump log file (in `.txt` format).
   - The file path will appear in the text field.

3. **Analyze the File**:
   - Click the **Analyze** button to process the file.
   - The program will:
     - Parse and analyze the file.
     - Save the analysis results in `rapport.md` and `packets.csv`.

4. **View the Report**:
   - Click the **View Report** button to open the Markdown file (`rapport.md`) in your default browser or text editor.

5. **Open the CSV File**:
   - Click the **Open CSV** button to open the CSV file (`packets.csv`) for further exploration in Excel or another spreadsheet application.

6. **Generate and View the Pie Chart**:
   - Click the **Generate Chart** button to display a pie chart of the top 5 most frequent source IPs.

---

## **Output Files**

1. **Markdown Report (`rapport.md`)**:
   - Summarizes key statistics and findings, including:
     - Most frequent source and destination IPs.
     - Frequent connections.
     - Port scans.
     - UDP traffic.
     - SSH attempts.
     - Hourly activity.

2. **CSV File (`packets.csv`)**:
   - Contains the parsed data with the following columns:
     - Timestamp
     - Source IP
     - Source Port
     - Destination IP
     - Destination Port
     - Protocol

3. **Pie Chart**:
   - Visual representation of the top 5 source IPs based on frequency.

---

## **Troubleshooting**

- **Error: Missing Dependencies**:
  - Ensure all required libraries are installed. Use:
    ```bash
    pip install matplotlib
    ```

- **File Not Found**:
  - Confirm the selected file exists and is in `.txt` format.

- **Analysis Errors**:
  - Ensure the tcpdump file follows the expected format with valid timestamp, IP, and port details.

---

## **Extending the Program**

- Modify the Python code to customize the analysis or add new features.
- Upload the code to GitHub to share with team members globally.

---

By following this guide, you should be able to successfully use the **TCPDump File Analyzer** to process and understand network data. For any additional help, refer to the comments in the source code.
