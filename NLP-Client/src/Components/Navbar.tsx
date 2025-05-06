type NavbarProps = {
	changePage: (page: number) => void;
};

function Navbar({ changePage }: NavbarProps) {
	return (
		<nav className="navbar">
			<span className="nav-item">CS6320 - Term Project</span>
			<span className="nav-item center">
				<span onClick={() => changePage(1)}>Home</span>
				<span onClick={() => changePage(2)}>Report</span>
			</span>
			<span className="nav-item"></span>
		</nav>
	);
}

export default Navbar;
