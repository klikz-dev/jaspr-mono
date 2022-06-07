const Plus = ({
    color = '#ffffff',
    height = 20,
    ariaHidden = false,
}: {
    color?: string;
    height?: number;
    ariaHidden?: boolean;
}) => {
    const midpoint = height / 2;
    const width = height;
    return (
        <svg
            width={`${width}px`}
            height={`${height}px`}
            viewBox={`0 0 ${width} ${height}`}
            version="1.1"
            aria-hidden={ariaHidden ? 'true' : 'false'}
        >
            <g stroke="none" strokeWidth="1" fill="none" fillRule="evenodd">
                <g stroke={color} strokeWidth="2">
                    <line x1={midpoint} x2={midpoint} y1={height} y2={0} />
                    <line x1={0} x2={width} y1={midpoint} y2={midpoint} />
                </g>
            </g>
        </svg>
    );
};

export default Plus;
