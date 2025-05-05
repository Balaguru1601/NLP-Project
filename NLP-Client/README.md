# Resume Classification System - Client

This is the client-side application for the **Resume Classification System**, built using **React** and **TypeScript**. The application allows users to upload their resumes, get a predicted job role, download a newly generated resume tailored to that role, and browse relevant job listings.

## Features

-   **Resume Upload:** Users can upload a resume in PDF or DOCX format.
-   **Role Prediction:** The system predicts the most suitable job role based on the content of the uploaded resume.
-   **AI-Generated Resume:** Based on the predicted role, a new professional resume is generated in LaTeX format and converted to PDF. The user can download the Resume if required.
-   **Job Recommendations:** Users receive relevant job openings based on the predicted job role.

## Technologies Used

-   **React**: A JavaScript library for building user interfaces.
-   **TypeScript**: A superset of JavaScript that adds static types to improve the development experience.
-   **Axios**: For making HTTP requests to the Flask backend.
-   **File Upload Handling**: To manage resume file uploads.

## Prerequisites

Before you can run this project, ensure you have the following installed:

-   [Node.js](https://nodejs.org/) (v14 or higher)
-   [npm](https://www.npmjs.com/) (Node package manager)
-   [React](https://reactjs.org/) (via Create React App)

## Getting Started

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/Balaguru1601/NLP-Project.git
cd NLP-Project/NLP-Client
```

### 2. Install Dependencies

Install the necessary dependencies by running the following command:

```bash
npm install
```

### 3. Start the Development Server

To start the development server, run:

```bash
npm start
```

This will start the application on [http://localhost:5173](http://localhost:5173).

### 4. Folder Structure

The folder structure of the client-side application is as follows:

```
NLP-Client/
├── public/
├── src/
│   ├── components/
│   │   ├── Upload.tsx
│   │   ├── Intro.tsx
│   │   ├── Footer.tsx
│   │   ├── Navbar.tsx
│   │   ├── SectionA.tsx
│   │   ├── SectionB.tsx
│   │   ├── PdfViewer.tsx
│   │   ├── Loader.tsx
│   │   ├── ViewJobs.tsx
├── App.tsx
├── main.tsx
├── App.css
```
