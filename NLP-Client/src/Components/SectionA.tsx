import GraphicResume from "./GraphicResume";

function SectionA() {
	return (
		<section className="section-a">
			<GraphicResume />
			<div className="content">
				<h2> How It Works? </h2>
				<p>
					Analyze Your Resume Upload your resume and let our K-Nearest Neighbors (KNN)
					algorithm classify your skills, experience, and qualifications. The AI will then
					recommend the most suitable roles for you based on the most relevant jobs in the
					industry.
				</p>
				<h2> Personalized Job Recommendations</h2>
				<p>
					Using a powerful Large Language Model (LLM), SmartResume doesn't just stop at
					suggesting a role. We also generate a custom resume tailored to your desired
					position and give you a list of real-time, open job positions that match your
					skills. It's your one-stop-shop for career development.
				</p>
			</div>
		</section>
	);
}

export default SectionA;
