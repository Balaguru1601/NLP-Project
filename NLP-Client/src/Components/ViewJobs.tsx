type JobCard = {
	company: string;
	description: string;
	link: string;
	location: string;
	title: string;
};

const styles = {
	card: {
		border: "1px solid #ddd",
		borderRadius: "8px",
		padding: "16px",
		margin: "16px auto",
		maxWidth: "600px",
		boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
		fontFamily: "Arial, sans-serif",
		backgroundColor: "#000",
		color: "whitesmoke",
	},
	header: {
		display: "flex",
		justifyContent: "space-between",
		alignItems: "flex-start",
		marginBottom: "12px",
	},
	title: {
		fontSize: "1.25rem",
		fontWeight: "bold",
		margin: 0,
		flex: 1,
	},
	company: {
		fontSize: "1rem",
		color: "#bbb",
		marginLeft: "12px",
		whiteSpace: "nowrap",
	},
	footer: {
		marginTop: "12px",
		display: "flex",
		justifyContent: "space-between",
		alignItems: "center",
	},
	link: {
		textDecoration: "none",
		color: "#007BFF",
		fontWeight: "bold",
	},
};

function getJobCards(data: JobCard[]) {
	return data.map((job, index) => (
		<div style={styles.card} key={index}>
			<div style={styles.header}>
				<h2 style={styles.title}>{job.title}</h2>
				<span style={styles.company}>{job.company}</span>
			</div>
			<p>{job.description}</p>
			<div style={styles.footer}>
				<span>{job.location}</span>
				<a href={job.link} target="_blank" rel="noopener noreferrer" style={styles.link}>
					Apply
				</a>
			</div>
		</div>
	));
}

type ViewJobsProps = {
	jobs: JobCard[];
};

function ViewJobs(props: ViewJobsProps) {
	return (
		<section className="view-jobs">
			<h2>Jobs based on recommendation</h2>
			<div className="job-section">{getJobCards(props.jobs)}</div>
		</section>
	);
}

export default ViewJobs;
