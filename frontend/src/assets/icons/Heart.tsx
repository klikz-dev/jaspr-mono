const Heart = ({
    color = '#ffffff',
    height = 20,
    fill = 'none',
    ariaHidden = false,
}: {
    color?: string;
    fill?: string;
    height?: number;
    ariaHidden?: boolean;
}) => {
    const width = height * 1.05;
    return (
        <svg
            width={width}
            height={height}
            viewBox="0 0 40 38"
            fill={fill}
            aria-hidden={ariaHidden ? 'true' : 'false'}
        >
            <path
                fillRule="evenodd"
                clipRule="evenodd"
                d="M20 6.12849C17.9809 3.06273 14.5848 1.00017 11.0516 1C10.0018 1 8.94007 1.18201 7.89861 1.57393C2.4827 3.61169 -0.329624 9.85927 1.61709 15.5283C3.45754 20.8882 18.3042 35.3039 19.9183 36.8605C19.9301 36.9513 19.9367 37 19.9367 37C19.9367 37 19.9597 36.978 20 36.9392C20.0402 36.978 20.0632 37 20.0632 37C20.0632 37 20.0696 36.9513 20.0816 36.8605C21.6957 35.3039 36.5424 20.8882 38.383 15.5283C40.3295 9.85927 37.5172 3.61169 32.1015 1.57393C31.0602 1.18218 29.998 1 28.9485 1C25.415 1 22.0191 3.06238 20 6.12849Z"
                stroke={color}
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
            />
        </svg>
    );
};

export default Heart;
