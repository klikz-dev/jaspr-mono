const CirclePlus = ({
    color = '#117383',
    height = 25,
    ariaHidden = false,
    showPlus = true,
}: {
    color?: string;
    showPlus?: boolean;
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
            aria-hidden={ariaHidden}
        >
            <circle cx="12" cy="12" r="10.5" stroke="#B8BCCC" fill="#fff" strokeWidth={1} />
            {showPlus && (
                <>
                    <path
                        d="M6.45312 12L17.5474 12"
                        stroke="#117383"
                        strokeWidth="3"
                        strokeLinecap="round"
                    />
                    <path
                        d="M12 6.45288L12 17.5471"
                        stroke="#117383"
                        strokeWidth="3"
                        strokeLinecap="round"
                    />
                </>
            )}
        </svg>
    );
};

export default CirclePlus;
