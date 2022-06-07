const Upload = ({
    color = '#ffffff',
    height = 20,
    ariaHidden = false,
}: {
    color?: string;
    height?: number;
    ariaHidden?: boolean;
}) => {
    return (
        <svg
            width={height}
            height={height}
            viewBox="0 0 18 19"
            fill="none"
            aria-hidden={ariaHidden ? 'true' : 'false'}
        >
            <path
                d="M5.26968 8H1V18H17.0113V8H12.7416"
                stroke={color}
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
            />
            <path
                d="M9.4478 0.558058C9.20372 0.313981 8.808 0.313981 8.56392 0.558058L4.58644 4.53553C4.34236 4.77961 4.34236 5.17534 4.58644 5.41942C4.83052 5.6635 5.22625 5.6635 5.47033 5.41942L9.00586 1.88388L12.5414 5.41942C12.7855 5.6635 13.1812 5.6635 13.4253 5.41942C13.6694 5.17534 13.6694 4.77961 13.4253 4.53553L9.4478 0.558058ZM9.63086 13V1H8.38086V13H9.63086Z"
                fill={color}
            />
        </svg>
    );
};
export default Upload;
