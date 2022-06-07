const CircleCheck = ({
    color = '#117383',
    height = 25,
    ariaHidden = false,
    showCheck = true,
}: {
    color?: string;
    showCheck?: boolean;
    height?: number;
    ariaHidden?: boolean;
}) => {
    const width = height;
    return (
        <svg
            width={width}
            height={height}
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
        >
            <circle
                cx="12"
                cy="12"
                r="10.5"
                fill={showCheck ? '#117383' : '#fff'}
                stroke={showCheck ? '#117383' : '#B8BCCC'}
                strokeWidth={3}
            />
            {showCheck && (
                <path
                    d="M7.5 13.05L10.5938 15.75L16.5 9"
                    stroke="white"
                    strokeWidth="3"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                />
            )}
        </svg>
    );
};

export default CircleCheck;
