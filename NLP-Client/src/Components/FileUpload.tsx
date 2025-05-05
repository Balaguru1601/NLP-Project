import React, { useState } from "react";
import axios from "axios";

// Define a type for the file object (optional, but helps with TypeScript)
type FileUploadProps = {
	uploadUrl: string; // URL to which you are uploading the file (Flask server)
};

const FileUpload: React.FC<FileUploadProps> = ({ uploadUrl }) => {
	const [pdfFile, setPdfFile] = useState<File | null>(null);
	const [error, setError] = useState<string | null>(null);
	const [uploading, setUploading] = useState<boolean>(false);
	const [responseMessage, setResponseMessage] = useState<string>("");

	// Handle the file selection
	const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		const file = e.target.files?.[0]; // Get the first file selected
		if (file && file.type === "application/pdf") {
			setPdfFile(file);
			setError(null); // Reset error on valid file
		} else {
			setError("Please upload a valid PDF file.");
			setPdfFile(null);
		}
	};

	// Handle form submission to upload the file
	const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();

		if (!pdfFile) {
			setError("No file selected");
			return;
		}

		setUploading(true);
		setError(null);
		const formData = new FormData();
		formData.append("file", pdfFile);

		try {
			const test = await axios.get("http://localhost:5000/api/data");
			console.log(test);
			const response = await axios.post(uploadUrl, formData, {
				headers: {
					"Content-Type": "multipart/form-data",
					Accept: "application/json",
				},
				maxContentLength: Infinity,
				withCredentials: false,
				maxBodyLength: Infinity,
			});
			setResponseMessage(`File uploaded successfully: ${response.data.filename}`);
			setTimeout(() => {
				setResponseMessage("");
			}, 5000); // Clear message after 5 seconds
		} catch (error) {
			console.error("Error uploading file:", error);
			setError("There was an error uploading the file.");
		} finally {
			setUploading(false);
		}
	};

	return (
		<div>
			<h2>Upload PDF File</h2>
			<form onSubmit={handleSubmit}>
				<div>
					<input type="file" accept="application/pdf" onChange={handleFileChange} />
				</div>
				<button type="submit" disabled={uploading}>
					{uploading ? "Uploading..." : "Upload PDF"}
				</button>
			</form>
			{error && <div style={{ color: "red" }}>{error}</div>}
			{responseMessage && <div style={{ color: "green" }}>{responseMessage}</div>}
		</div>
	);
};

export default FileUpload;
