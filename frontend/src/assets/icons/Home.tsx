const Home = ({
    color = '#ffffff',
    height = 20,
    ariaHidden = false,
}: {
    color?: string;
    height?: number;
    ariaHidden?: boolean;
}) => {
    const width = height * 1.167;
    return (
        <svg
            width={width}
            height={height}
            viewBox="0 0 49 42"
            fill="none"
            aria-hidden={ariaHidden ? 'true' : 'false'}
        >
            <path
                d="M20.2 40.1314C20.8249 40.1314 21.3314 39.6249 21.3314 39V27.4255H27.6686V39C27.6686 39.6249 28.1751 40.1314 28.8 40.1314H39.55C40.1749 40.1314 40.6814 39.6249 40.6814 39V23.1903H46C46.47 23.1903 46.8911 22.8997 47.0578 22.4602C47.2246 22.0207 47.1023 21.524 46.7505 21.2122L25.2505 2.15334C24.8222 1.77365 24.1778 1.77365 23.7495 2.15334L2.24947 21.2122C1.89774 21.524 1.77542 22.0207 1.94216 22.4602C2.1089 22.8997 2.52997 23.1903 3 23.1903H8.31857V39C8.31857 39.6249 8.82513 40.1314 9.45 40.1314H20.2Z"
                stroke={color}
                strokeWidth="2.26286"
                strokeLinejoin="round"
            />
        </svg>
    );
};

export default Home;
