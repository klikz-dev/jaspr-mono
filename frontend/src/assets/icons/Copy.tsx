const Copy = ({
    color = '#ffffff',
    height = 20,
    ariaHidden = false,
}: {
    color?: string;
    height?: number;
    ariaHidden?: boolean;
}) => {
    const width = height * 0.85;
    return (
        <svg
            width={width}
            height={height}
            viewBox={`0 0 ${width} ${height}`}
            fill="none"
            aria-hidden={ariaHidden ? 'true' : 'false'}
        >
            <rect
                x="3.75"
                y="3.75"
                width="12.5"
                height="15.5"
                rx="2.25"
                stroke={color}
                strokeWidth="1.5"
            />
            <rect
                x="0.75"
                y="0.75"
                width="12.5"
                height="15.5"
                rx="2.25"
                stroke={color}
                strokeWidth="1.5"
            />
        </svg>
    );
};

export default Copy;
