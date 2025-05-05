type PDFViewerProps = {
	url: string;
};

// Define the component
const PDFViewer = ({ url }: PDFViewerProps) => {
	return (
		<div>
			<h2>Resume Viewer</h2>
			{/* Embed the PDF in an iframe */}
			<iframe src={url} width="100%" height="600px" title="Resume viewer"></iframe>
			<br />
			{/* Provide a download link for the PDF */}
			<a href={url} download="resume.pdf">
				Download PDF
			</a>
		</div>
	);
};

export default PDFViewer;
