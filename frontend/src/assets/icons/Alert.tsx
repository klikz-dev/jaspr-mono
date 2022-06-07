const Alert = ({
    color = '#DD1D1D',
    height = 33,
    ariaHidden = false,
}: {
    color?: string;
    height?: number;
    ariaHidden?: boolean;
}) => {
    const width = height;
    return (
        <svg width={width} height={height} viewBox="0 0 33 33" fill="none" aria-hidden={ariaHidden}>
            <path
                fillRule="evenodd"
                clipRule="evenodd"
                d="M16 30.5C23.732 30.5 30 24.232 30 16.5C30 8.76801 23.732 2.5 16 2.5C8.26801 2.5 2 8.76801 2 16.5C2 24.232 8.26801 30.5 16 30.5ZM16 20C15.1716 20 14.5 19.3284 14.5 18.5V8.16358C14.5 7.33516 15.1716 6.66358 16 6.66358C16.8284 6.66358 17.5 7.33516 17.5 8.16358V18.5C17.5 19.3284 16.8284 20 16 20ZM16 26.3364C15.1716 26.3364 14.5 25.6648 14.5 24.8364V23.5C14.5 22.6716 15.1716 22 16 22C16.8284 22 17.5 22.6716 17.5 23.5V24.8364C17.5 25.6648 16.8284 26.3364 16 26.3364Z"
                fill={color}
            />
        </svg>
    );
};

export default Alert;
