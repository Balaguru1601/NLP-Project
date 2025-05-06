from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from fake_useragent import UserAgent
import fitz
from google import genai
import os
import re
import string
import pickle
import warnings
from dotenv import load_dotenv

warnings.filterwarnings('ignore')

def clean_resume(txt):
    txt = re.sub(r'http\S+', ' ', txt)

    # Remove mentions (e.g., @username)
    txt = re.sub(r'@\S+', ' ', txt)

    # Remove hashtags (keeping words)
    txt = re.sub(r'#\S+', ' ', txt)

    # Remove RT (retweets) and common Twitter elements
    txt = re.sub(r'\bRT\b|cc', ' ', txt)

    # Remove special characters, punctuations
    txt = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', txt)

    # Remove numbers
    txt = re.sub(r'\d+', ' ', txt)

    # Remove extra whitespace
    txt = re.sub(r'\s+', ' ', txt).strip()

    # Convert to lowercase
    txt = txt.lower()

    return txt

def generate_resume(role, raw_text):
    load_dotenv()
    gkey = os.getenv('google_api_key')
    print(gkey)

    client = genai.Client(api_key=gkey)

    prompt = (f"Generate a professional resume for a candidate applying for the role of {role}. "
              "The resume should be based on the following text extracted from a PDF: "
              f"{raw_text}. "    
              "Include relevant skills, experiences, certifications, and a summary that aligns with industry standards. "
              "The resume should be in a modern format with sections such as Summary, Skills, Professional Experience, "
              "Education, and Certifications. Assume the candidate has 3–5 years of experience unless stated otherwise. "
              "Tailor the content specifically for this role. "
              "The structure of the resume should be in a LATEX format with the following keys: "
              "summary, skills, professional_experience, education, certifications."
              "Make sure that the resume is well-organized and easy to read and fits in ONE page or 2 at max. "
              "The response should only be the latex object without any additional text or explanation.")

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    return response.text


def extract_text_from_pdf(pdf_path):
    """Extract text from each page of a PDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def get_jobs(query = "",try_count = 0):
    try:
        user_agent = UserAgent().random
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        options.add_argument(f"user-agent={user_agent}")


        driver= webdriver.Firefox(options=options)

        job_query = query
        location_query = "Texas"

        driver.get(f"https://www.simplyhired.com/search?q={job_query}&l={location_query}")
        time.sleep(5)

        articles = driver.find_elements(By.XPATH,'//*[@id="job-list"]/li')
        print(len(articles))

        all_jobs = []

        for article in articles:
            title = article.find_element(By.XPATH, './/div/div[1]/h2/a').text
            job_link = article.find_element(By.XPATH, './/div/div[1]/h2/a').get_attribute('href')
            company = article.find_element(By.XPATH, './/div/p[1]/span[1]/span').text
            location = article.find_element(By.XPATH, './/div/p[1]/span[2]').text
            description = article.find_element(By.XPATH, './/div/p[2]').text
            all_jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "link": job_link
            })


        # time.sleep(100)

        driver.quit()
        return all_jobs
    except Exception as e:
        print(f"Error: {e}")
        if try_count < 3:
            print("Retrying...")
            time.sleep(3)
            try_count += 1
            return get_jobs(query)
        else:
            return []


def latex_to_pdf(file_name, try_count = 0):
    try:
        current_directory = os.getcwd()
        options = webdriver.FirefoxOptions()
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", current_directory + "\pdf")
        options.add_argument('--headless')

        driver = webdriver.Firefox(options=options)

        driver.get(f"https://texviewer.herokuapp.com/")
        time.sleep(5)

        text_area = driver.find_element(By.XPATH, '//*[@id="fileload1"]')
        text_area.send_keys(current_directory + f"\\tex\\{file_name}.tex")  # replace with the path to your file
        time.sleep(2)
        generate_btn = driver.find_element(By.XPATH, '//*[@id="tabletop"]/table/tbody/tr/td[7]/button')
        generate_btn.click()

        # delete all files in pdf folder
        for f in os.listdir(current_directory + "\pdf"):
            file_path = os.path.join(current_directory + "\pdf", f)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"Deleted pdf file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

        time.sleep(2)
        download_btn = driver.find_element(By.XPATH, '//*[@id="pdfdlink"]')
        download_btn.click()
        time.sleep(2)

        driver.quit()
    except Exception as e:
        if try_count < 3:
            print("Pdf conversion - Retrying...")
            print(file_name)
            time.sleep(3)
            try_count += 1
            return latex_to_pdf(file_name, try_count)
        else:
            print(f"Error: {e}")
            return None


def predict_role_from_resume(pdf_path):
    # Step 1: Extract text from PDF
    raw_text = extract_text_from_pdf("uploads/" + pdf_path + ".pdf")
    file_name = pdf_path.split("/")[-1].split(".")[0]

    with open('models/knn_model.pkl', 'rb') as model_file:
        knn_model = pickle.load(model_file)

    with open('models/tfidf.pkl', 'rb') as vectorizer_file:
        tfidf = pickle.load(vectorizer_file)

    with open('models/le.pkl', 'rb') as encoder_file:
        le = pickle.load(encoder_file)

    # Step 2: Clean the extracted text
    cleaned_text = clean_resume(raw_text)

    # Step 3: Vectorize using the same TF-IDF vectorizer
    transformed_text = tfidf.transform([cleaned_text])
    transformed_text = transformed_text.toarray()

    # Step 4: Predict using the trained model
    predicted_label = knn_model.predict(transformed_text)[0]

    # Step 5: Decode the label to original category
    predicted_category = le.inverse_transform([predicted_label])[0]

    # Step 6: Generate resume using the Google Gemini API
    generated_resume = generate_resume(predicted_category, cleaned_text)

    generated_resume.replace("latex","")

    # delete all files in tex folder
    for f in os.listdir("tex"):
        file_path = os.path.join("tex", f)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                print(f"Deleted tex file: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

    with open("tex/" + file_name + ".tex", "w") as f:
        f.write(generated_resume)

    with open("tex/" + file_name+'.tex', 'r') as file:
        lines = file.readlines()

    # Remove the first and last lines
    modified_lines = lines[1:-1]  # This slices the list to remove the first and last lines

    with open("tex/" +file_name + '.tex', 'w') as file:
        file.writelines(modified_lines)

    latex_to_pdf(file_name)

    return predicted_category
