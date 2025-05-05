import "./App.css";
import Upload from "./Components/Upload";
import Navbar from "./Components/Navbar";
import Intro from "./Components/Intro";
import SectionA from "./Components/SectionA";
import SectionB from "./Components/SectionB";
import { useState } from "react";
import Loader from "./Components/Loader";
import Footer from "./Components/Footer";

// TODO
// Add page for showing the results
// 	Resume preview if possible
// Add workflow of the process

function App() {
	const [loading, setLoading] = useState(false);
	return (
		<>
			{loading && <Loader />}
			<Navbar />
			<Intro />
			<SectionA />
			<SectionB />
			<Upload setLoading={(val: boolean) => setLoading(val)} />
			{/* <FileUpload uploadUrl="http://localhost:5000/api/upload" />
			{selectedFile && (
				<div>
					<p>Selected File: {selectedFile.name}</p>
				</div>
			)} */}
			<Footer />
		</>
	);
}

export default App;
