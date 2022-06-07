const Interview = ({
    color = '#ffffff',
    height = 20,
    ariaHidden = false,
}: {
    color?: string;
    height?: number;
    ariaHidden?: boolean;
}) => {
    const width = height * 1.41;
    return (
        <svg
            width={width}
            height={height}
            viewBox="0 0 45 32"
            fill="none"
            aria-hidden={ariaHidden ? 'true' : 'false'}
        >
            <path
                d="M44 16H14"
                stroke={color}
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
            />
            <path
                d="M44 28H14"
                stroke={color}
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
            />
            <path
                d="M44 4H14"
                stroke={color}
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
            />
            <circle cx="4" cy="4" r="3" stroke={color} strokeWidth="2" />
            <circle cx="4" cy="16" r="3" stroke={color} strokeWidth="2" />
            <circle cx="4" cy="28" r="3" stroke={color} strokeWidth="2" />
        </svg>
    );
};

export default Interview;
