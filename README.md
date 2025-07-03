# lead_filterating_tool


# 💡 ODBus Intelligent Lead Filtration Tool

## Project Overview

The **ODBus Intelligent Lead Filtration Tool** is a powerful web application designed to revolutionize the lead generation process for sales and marketing teams. Leveraging the comprehensive **Canadian Open Database of Businesses (ODBus)**, this tool moves beyond generic lead lists to provide highly targeted and prioritized prospects. It's built with a focus on user experience, technical sophistication, and crucial **AI-readiness**, making it an invaluable asset for strategic sales outreach and data-driven decision-making.

## 🌟 Key Features & Innovations

Our solution stands out by offering:

* **Dynamic, Multi-Criteria Filtering:** Go beyond basic lookups. Our tool enables sophisticated queries by combining filters such as **industry (NAICS code with descriptive names)**, **employee count**, **province (full names)**, and **city**. This allows users to generate highly refined lead lists that are precise to their target market.
* **Intuitive User Experience (UX/UI):** Built with Gradio, the application offers a clean, professional, and easy-to-navigate interface. Thoughtful design decisions, like using full province names and descriptive NAICS categories, minimize the learning curve and enhance usability for non-technical users.
* **Simulated Lead Scoring (AI-Ready Component):** A core innovation, this feature automatically assigns a 'Lead Score' to each filtered business. Based on predefined business rules (e.g., company size, specific industries, key geographical locations), this score prioritizes high-potential prospects, providing **actionable intelligence** that streamlines sales efforts.
* **Robust Technical Execution:** The backend efficiently processes over 450,000 records using `pandas`, demonstrating reliable performance at scale. It effectively handles data quality aspects like missing values (`'..'`) and ensures consistent data types, providing a clean dataset for analysis.
* **Ethical Data Collection & Open Source Leveraging:** By utilizing the publicly available and legitimately licensed Canadian ODBus, the tool avoids the legal and ethical complexities associated with web scraping, ensuring a sustainable and compliant data source.
* **Seamless Data Export:** Filtered and prioritized lead lists are immediately downloadable as a clean CSV file, ready for direct integration into CRM systems or other sales workflow tools.

## ✨ AI Readiness Justification

This tool is a fundamental step in building an AI-powered sales strategy:

* **Data Quality & Structuring:** It acts as an automated **data preparation pipeline**, cleaning, structuring, and feature-engineering raw ODBus data. This process ensures the output is consistently formatted and ready for consumption by machine learning models.
* **Targeted Dataset Generation:** The ability to generate highly relevant and filtered subsets of the data (e.g., "high-score tech leads in Ontario") provides ideal, focused datasets for training specialized AI/ML models, such as:
    * **Predictive Lead Scoring Models:** The simulated lead score demonstrates the methodology for building a data-driven model to predict conversion probability.
    * **Lead Recommendation Engines:** For suggesting "look-alike" companies based on successful past clients.
    * **Automated Outreach Personalization:** Using NAICS descriptions and lead scores to tailor initial contact messages.
* **Scalability for AI Workloads:** The underlying `pandas` framework ensures the solution can handle growing datasets, supporting the iterative development and deployment of more complex AI solutions.

## 🚀 How to Use the App & Explore the Code

The ODBus Intelligent Lead Filtration Tool is deployed and fully functional on our GitHub Space!

### **Try the Live Demo:**

**[Click here to test the deployed app directly!](https://huggingface.co/spaces/devankit/Ankit_Lead_Filteration)**

### **Explore the Code & Data:**

You can view all the project files, including the application code (`app.py`), required libraries (`requirements.txt`), and even download the `ODBus_v1.csv` dataset, directly from this huggingface repository.

---

### **Local Setup (for Developers)**

If you wish to run the application locally or explore the code in your own environment:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/AnkitTsj/lead_filterating_tool.git](https://github.com/AnkitTsj/lead_filterating_tool.git)
    cd your-repo-name
    ```


2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download the Data:**
    The `ODBus_v1.csv` dataset is essential. You can download it directly from the "Files" section of the Huggingface Space linked above or within the main repository files. Place `ODBus_v1.csv` in the same directory as `app.py`. or [Click here to download data!](https://huggingface.co/spaces/devankit/Ankit_Lead_Filteration/blob/main/ODBus_v1.csv)

5.  **Run the application:**
    ```bash
    python app.py
    ```
    The application will typically open in your browser at `http://127.0.0.1:7860/`.


---
