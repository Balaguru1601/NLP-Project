import axios from "axios";
import React, { useRef, useState } from "react";
import PDFViewer from "./PdfViewer";
import ViewJobs from "./ViewJobs";
// import data from "./data.json"; // Import the test data

type UploadProps = {
	setLoading: (val: boolean) => void;
};

type JobCard = {
	company: string;
	description: string;
	link: string;
	location: string;
	title: string;
};

const Upload = ({ setLoading }: UploadProps) => {
	const [fileName, setFileName] = useState<string | null>(null);
	const [isDragActive, setIsDragActive] = useState<boolean>(false);
	const [pdfFile, setPdfFile] = useState<File | null>(null);
	const [error, setError] = useState<string | null>(null);
	const [uploading, setUploading] = useState<boolean>(false);
	const [responseMessage, setResponseMessage] = useState<string>("");
	const [pdfUrl, setPdfUrl] = useState<string | null>(null);
	const [jobs, setJobs] = useState<JobCard[]>([]); // State to hold job cards
	const [predictedRole, setPredictedRole] = useState<string | null>(null); // State to hold predicted role

	const fileInputRef = useRef<HTMLInputElement | null>(null);

	// Handles file selection from the Browse button
	const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
		event.preventDefault();
		const file = event.target.files?.[0];
		console.log(file);
		if (file && file.type === "application/pdf") {
			setFileName(file.name); // Set the file name for display
			setPdfFile(file);
			setError(null); // Reset error on valid file
		} else {
			setError("Please upload a valid PDF file.");
			setPdfFile(null);
		}
	};

	const handleCancel = () => {
		setFileName(null);
		setPdfFile(null); // Notify parent component about the cancellation
		setError(null); // Reset error state

		if (fileInputRef.current) {
			fileInputRef.current.value = ""; // Clear the file input value
		}
	};

	const handleSubmit = async (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
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
			setLoading(true);
			const response = await axios.post("http://localhost:5000/api/upload", formData, {
				headers: {
					"Content-Type": "multipart/form-data",
					Accept: "application/json",
				},
			});
			if (response.status !== 200) {
				throw new Error("Failed to upload file");
			}
			console.log(response.data);
			// If server status is 200,
			// get filename form response and send request to api/get-resume with filename
			// to get the pdf file
			if (response.data.jobs) {
				setJobs(response.data.jobs); // Set the jobs data in state
			}
			if (response.data.predicted_role) {
				setPredictedRole(response.data.predicted_role); // Set the predicted role in state
			}
			const pdfResponse = await axios.get(`http://localhost:5000/api/get-resume`, {
				params: { filename: response.data.filename },
				responseType: "blob", // Set response type to blob for PDF
			});
			if (pdfResponse.status !== 200) {
				throw new Error("Failed to fetch PDF file");
			}

			const fileURL = URL.createObjectURL(pdfResponse.data); // Create a Blob URL from the response
			setPdfUrl(fileURL); // Set the PDF URL in state
			setResponseMessage(`File uploaded successfully: ${response.data.filename}`);
			setTimeout(() => {
				setResponseMessage("");
			}, 5000); // Clear message after 5 seconds
		} catch (error) {
			console.error("Error uploading file:", error);
			setError("There was an error uploading the file.");
			setResponseMessage(""); // Clear any previous success message
			setTimeout(() => {
				setError(null); // Clear error message after 3 seconds
			}, 3000);
			setFileName(null);
			setPdfFile(null); // Notify parent component about the cancellation

			if (fileInputRef.current) {
				fileInputRef.current.value = ""; // Clear the file input value
			}
		} finally {
			setLoading(false);
			setUploading(false);
			setFileName(null); // Set the file name after <upload></upload>
		}
	};

	// Handles drag events
	const handleDragOver = (event: React.DragEvent) => {
		event.preventDefault();
		setIsDragActive(true);
	};

	const handleDragLeave = () => {
		setIsDragActive(false);
	};

	const handleDrop = (event: React.DragEvent) => {
		event.preventDefault();
		setIsDragActive(false);
		const file = event.dataTransfer.files ? event.dataTransfer.files[0] : null;
		if (file && file.type === "application/pdf") {
			setPdfFile(file);
			setError(null); // Reset error on valid file
		} else {
			setError("Please upload a valid PDF file.");
			setPdfFile(null);
		}
	};

	return (
		<>
			<div className="upload-section">
				<div
					className={`file-upload-container ${isDragActive ? "drag-active" : ""}`}
					onDragOver={handleDragOver}
					onDragLeave={handleDragLeave}
					onDrop={handleDrop}
				>
					<div className="upload-box">
						<p className="upload-text">Drop Resume</p>
						<p className="or-text">or</p>
						<label htmlFor="file-upload" className="browse-button">
							<span>Browse</span>
						</label>
						<input
							type="file"
							id="file-upload"
							className="file-input"
							onChange={handleFileSelect}
							accept="application/pdf"
							ref={fileInputRef}
						/>
						<div className="file-name">
							{fileName ? `Selected File: ${fileName}` : "No file selected"}
							{
								<p style={{ margin: 0 }}>
									<button
										onClick={handleCancel}
										style={{ visibility: fileName ? "visible" : "hidden" }}
									>
										Cancel
									</button>
								</p>
							}
						</div>

						{error && <div style={{ color: "red" }}>{error}</div>}
						{responseMessage && <div style={{ color: "green" }}>{responseMessage}</div>}
					</div>
				</div>
				<button disabled={uploading} onClick={handleSubmit}>
					{uploading ? "Uploading..." : "Upload PDF"}
				</button>
			</div>
			{predictedRole && <h2 className="prediction"> Predicted Role - {predictedRole}</h2>}
			{pdfUrl && <PDFViewer url={pdfUrl} />}
			{jobs.length > 0 && <ViewJobs jobs={jobs} />}
		</>
	);
};

export default Upload;
