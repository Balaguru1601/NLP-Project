# Resume Classification System - Server

This is the backend server for the **Resume Classification System**, built using **Flask**. The server handles resume uploads, job role predictions, generating AI-powered resumes, and job recommendations.

---

## 🧠 Features

- **Resume Upload:** Accepts PDF or DOCX resume files uploaded by the client.
- **Role Prediction:** Analyzes the resume content and predicts the most suitable job role.
- **AI-Generated Resume:** Generates a new resume tailored to the predicted job role using AI (via LaTeX format).
- **Job Recommendations:** Scrapes job listings from external sources based on the predicted job role.

---

## 🛠️ Technologies Used

- **Flask:** A lightweight WSGI web application framework in Python.
- **Scikit-learn:** A machine learning library for Python used to build the job role prediction model.
- **NumPy / Pandas:** Libraries for data manipulation and analysis.
- **BeautifulSoup / Scrapy:** For scraping job listings (optional).
- **Gemini LLM:** For generating AI-powered resumes in LaTeX.
- **PyPDF2 / PDFKit:** For converting LaTeX-generated resumes to PDF.
- **Joblib / Pickle:** For saving and loading the trained ML model.

---

## ⚙️ Prerequisites

Ensure you have the following installed:

- [Python 3.x](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/) (optional but recommended)

---

## 🚀 Getting Started

### 📁 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

### 📦 2. Create a Virtual Environment (optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### 📥 3. Install Dependencies

```bash
pip install -r requirements.txt
```
### 🔧 4. Set Up Environment Variables
Create a `.env` file in the root directory and add the following variables:

```plaintext
google_api_key=your_google_api_key  #gemini api key
```

### 📊 5. Run the Flask Server

```bash
python server.py
```

### 🌐 6. Access the API

Upload a resume and get predictions by using the client


### API Endpoints
| Endpoint     | Method | Description                                      |
|--------------|--------|--------------------------------------------------|
| `/upload`    | POST   | Upload a resume file (PDF or DOCX)               |
| `/get-resume` | GET   | Get the generated resume in PDF format          |

### Project Structure
```plaintext
resume-screening.ipynb - Jupyter Notebook for resume screening, model training and evaluation
server.py - Main Flask application file
utils.py - Utility functions for file handling, model loading, Resume text extraction, Job scraping, Resume generation
requirements.txt - List of dependencies
/tex - Directory for LaTex generated resumes
/uploads - Directory for uploaded resumes
/pdfs - Directory for generated PDF resumes
```

### Developed by
#### Balaguru Sethuraman - BXS230069
#### Somesh Kennedy - SXK240047
#### For CS6320 - Natural Language Processing Spring 2025