#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import fitz  # PyMuPDF

import warnings
warnings.filterwarnings('ignore')
#%%
df = pd.read_csv('/kaggle/input/resume-dataset/UpdatedResumeDataSet.csv')
df.head()
#%%
df.shape
#%%
df['Category'].value_counts()
#%%
plt.figure(figsize=(15,5))
sns.countplot(x='Category', data=df)
plt.xticks(rotation=90)
plt.show()
#%%
df['Resume'][0]
#%%
# print('Original Category Distribution')
# print(df['Category'].value_counts())

# max_size = df['Category'].value_counts().max()

# balanced_df = df.groupby('Category').apply(lambda x: x.sample(max_size, replace=True)).reset_index(drop=True)

# df = balanced_df.sample(frac=1).reset_index(drop=True)

# print('\nBalanced Category Distribution after Oversampling')
# print(df['Category'].value_counts())
#%% md
# # Cleaning Data
#%%
import re
import string
def CleanResume(txt):
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
    
#%%

#%%
df['Resume'] = df['Resume'].apply(lambda x: CleanResume(x))
#%%
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
#%%
le.fit(df['Category'])
df['Category'] = le.transform(df['Category'])
#%%
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(stop_words='english')

tfidf.fit(df['Resume'])
text = tfidf.transform(df['Resume'])
#%%
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(text, df['Category'], test_size=0.2, random_state=42)
#%%
X_train.shape, X_test.shape
#%%
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

X_train = X_train.toarray()
X_test = X_test.toarray()

#%%
knn_model = KNeighborsClassifier()
knn_model.fit(X_train, y_train)
y_pred_knn = knn_model.predict(X_test)
print('\nKNeighborsClassifierResults:')
print(f'Accuracy: {accuracy_score(y_test, y_pred_knn):.4f}')
report_dict = classification_report(y_test, y_pred_knn, output_dict=True)

# Convert to DataFrame for better formatting
report_df = pd.DataFrame(report_dict).transpose()

# Round values to 4 decimal places
report_df = report_df.round(4)

print("\nClassification Report:")
print(report_df)

#%%
svc_model = SVC()
svc_model.fit(X_train, y_train)
y_pred_svc = svc_model.predict(X_test)
print("\nSVC Results:")
print(f"Accuracy: {accuracy_score(y_test, y_pred_svc):.4f}")
print(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred_svc)}")
report_dict = classification_report(y_test, y_pred_svc, output_dict=True)

# Convert to DataFrame for better formatting
report_df = pd.DataFrame(report_dict).transpose()

# Round values to 4 decimal places
report_df = report_df.round(4)

print("\nClassification Report:")
print(report_df)
#%% md
# # Save
#%%
# import pickle
# pickle.dump(tfidf, open('tfidf.pkl','wb'))
# pickle.dump(svc_model, open('clf.pkl', 'wb'))
# pickle.dump(le, open('encoder.pkl', 'wb'))
#%%
# !pip install pipreqs

#%%
# !pip freeze | grep -E 'numpy|pandas|matplotlib|seaborn' > requirements.txt

#%%

#%%
def extract_text_from_pdf(pdf_path):
    """Extract text from each page of a PDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text
#%%
def predict_resume_from_pdf(pdf_path):
    # Step 1: Extract text from PDF
    raw_text = extract_text_from_pdf(pdf_path)

    # Step 2: Clean the extracted text
    cleaned_text = CleanResume(raw_text)

    # Step 3: Vectorize using the same TF-IDF vectorizer
    transformed_text = tfidf.transform([cleaned_text])
    transformed_text = transformed_text.toarray()

    # Step 4: Predict using the trained model
    predicted_label = knn_model.predict(transformed_text)[0]

    # Step 5: Decode the label to original category
    predicted_category = le.inverse_transform([predicted_label])[0]

    return predicted_category
#%%
pdf_path = '/kaggle/input/testing/python-developer2 - Template 18.pdf'
predicted_category = predict_resume_from_pdf(pdf_path)
print(f"Predicted Resume Category: {predicted_category}")
#%%
