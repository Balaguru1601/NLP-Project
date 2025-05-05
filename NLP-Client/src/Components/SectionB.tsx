import GraphicManager from "./GraphicManager";

function SectionB() {
	return (
		<section className="section-b">
			<div>
				<h2>Why Choose SmartResume?</h2>
				<p>
					AI-Driven Job Matching Our KNN model leverages advanced classification
					techniques to accurately suggest roles that match your skills, experience, and
					career aspirations.
				</p>
				<h2>Tailored Resume Generation</h2>
				<p>
					Want to apply for a specific role? Our LLM-powered tool helps you create a
					professional, tailored resume that highlights the right skills for the job,
					boosting your chances of landing an interview.
				</p>
				<h2>Access Open Job Opportunities</h2>
				<p>
					Don't waste time searching for jobs manually. SmartResume instantly generates a
					list of open job roles that fit your qualifications, giving you a curated,
					up-to-date list of opportunities you can apply for immediately.
				</p>
			</div>
			<GraphicManager />
		</section>
	);
}

export default SectionB;
