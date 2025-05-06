import "./App.css";
import Upload from "./Components/Upload";
import Navbar from "./Components/Navbar";
import Intro from "./Components/Intro";
import SectionA from "./Components/SectionA";
import SectionB from "./Components/SectionB";
import { useState } from "react";
import Loader from "./Components/Loader";
import Footer from "./Components/Footer";

function App() {
	const [loading, setLoading] = useState(false);
	const [page, setPage] = useState(1);
	return (
		<>
			{loading && <Loader />}
			<Navbar
				changePage={(p) => {
					console.log(p);
					setPage(p);
				}}
			/>
			<Intro />
			{page == 1 ? (
				<>
					<SectionA />
					<SectionB />
					<Upload setLoading={(val: boolean) => setLoading(val)} />
					{/* <FileUpload uploadUrl="http://localhost:5000/api/upload" />
			{selectedFile && (
				<div>
					<p>Selected File: {selectedFile.name}</p>
				</div>
			)} */}
				</>
			) : (
				<div style={{ width: "100%", height: "800px", textAlign: "center" }}>
					<h2 style={{ marginTop: "20px", fontSize: "2rem" }}>Project Report</h2>
					<iframe
						src="/NLP_Project_Report.pdf"
						width="100%"
						height="100%"
						style={{ border: "none" }}
						title="Report"
					/>
				</div>
			)}
			<Footer />
		</>
	);
}

export default App;
