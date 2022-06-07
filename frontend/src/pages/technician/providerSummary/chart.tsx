interface CircleDimensions {
    cx: number;
    cy: number;
}

const computeTimestamp = (dateString: string) => {
    const d = new Date(dateString);
    // @ts-ignore // TODO Confirm this is still best way to validate a string is a date
    if (dateString && d instanceof Date && !isNaN(d)) {
        return `${d.getFullYear()}${('0' + (d.getMonth() + 1)).slice(-2)}${(
            '0' + d.getDate()
        ).slice(-2)} ${('0' + d.getHours()).slice(-2)}:${('0' + d.getMinutes()).slice(-2)}`;
    }
    return '';
};

const DistressCircle = ({ cy = 0, cx = 0 }: CircleDimensions) => (
    <circle
        cx={cx}
        cy={cy}
        r="4"
        strokeWidth="2"
        stroke="rgba(62,129,209,1)"
        fill="rgba(62,129,209,1)"
    />
);

const FrustrationCircle = ({ cy = 0, cx = 0 }: CircleDimensions) => (
    <circle cx={cx} cy={cy} r="4" stroke="rgba(243,114,22,1)" strokeWidth="2" fill="white" />
);

const SplitCircle = ({ cy = 0, cx = 0 }: CircleDimensions) => (
    <g transform={`translate(${cx - 5}, ${cy - 5}) scale(2)`}>
        <circle
            stroke="#F37216"
            strokeWidth="0.666666667"
            fill="#FFFFFF"
            cx="2.375"
            cy="2.25"
            r="1.91666667"
        ></circle>
        <path
            d="M3.5,3.375 C3.5,2.13235931 2.49264069,1.125 1.25,1.125 C0.00735931295,1.125 -1,2.13235931 -1,3.375 L3.5,3.375 Z"
            fill="#3E81D1"
            transform="translate(1.25, 2.25) rotate(-90) translate(-1.25, -2.25) "
        ></path>
    </g>
);

interface ChartProperties {
    checkInTime0: string | null;
    checkInTime1: string | null;
    distress0: null | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;
    distress1: null | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;
    frustration0: null | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;
    frustration1: null | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;
}

const Chart = ({
    checkInTime0,
    checkInTime1,
    distress0 = null,
    distress1 = null,
    frustration0 = null,
    frustration1 = null,
}: ChartProperties) => {
    const chartHeight = 75;
    const yTick = chartHeight / 10;
    return (
        <svg
            width="310"
            height="150"
            viewBox="0 0 300 150"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
        >
            <g transform="translate(95, 5)" fill="blue" width="205" height={chartHeight}>
                <line
                    x1="10"
                    y1="5"
                    x2="10"
                    y2={chartHeight}
                    stroke="rgba(151,151,151,1)"
                    strokeDasharray="4"
                />

                <line
                    x1="185"
                    y1="5"
                    x2="185"
                    y2={chartHeight}
                    stroke="rgba(151,151,151,1)"
                    strokeDasharray="4"
                />

                {frustration0 !== null && frustration1 !== null && (
                    <line
                        x1="10"
                        y1={yTick * (10 - frustration0)}
                        x2="185"
                        y2={yTick * (10 - frustration1)}
                        stroke="rgba(243,114,22,1)"
                        strokeWidth="2"
                    />
                )}

                {distress0 !== null && distress1 !== null && (
                    <line
                        x1="10"
                        y1={yTick * (10 - distress0)}
                        x2="185"
                        y2={yTick * (10 - distress1)}
                        stroke="rgba(62,129,209,1)"
                        strokeWidth="2"
                    />
                )}

                {frustration0 === distress0 && distress0 !== null && (
                    <SplitCircle cx={10} cy={yTick * (10 - distress0)} />
                )}
                {frustration0 !== distress0 && (
                    <>
                        {distress0 !== null && (
                            <DistressCircle cx={10} cy={yTick * (10 - distress0)} />
                        )}

                        {frustration0 !== null && (
                            <FrustrationCircle cx={10} cy={yTick * (10 - frustration0)} />
                        )}
                    </>
                )}

                {frustration1 === distress1 && distress1 !== null && (
                    <SplitCircle cx={185} cy={yTick * (10 - distress1)} />
                )}

                {frustration1 !== distress1 && (
                    <>
                        {distress1 !== null && (
                            <DistressCircle cx={185} cy={yTick * (10 - distress1)} />
                        )}

                        {frustration1 !== null && (
                            <FrustrationCircle cx={185} cy={yTick * (10 - frustration1)} />
                        )}
                    </>
                )}

                {frustration0 !== null && (
                    <text
                        x="10"
                        y="119"
                        stroke="rgba(0,0,0,1)"
                        fontWeight="100"
                        fontSize="13px"
                        textAnchor="middle"
                    >
                        {frustration0}
                    </text>
                )}

                {frustration1 !== null && (
                    <text
                        x="185"
                        y="119"
                        stroke="rgba(0,0,0,1)"
                        fontWeight="100"
                        fontSize="13px"
                        textAnchor="middle"
                    >
                        {frustration1}
                    </text>
                )}

                {distress0 !== null && (
                    <text
                        x="10"
                        y="139"
                        stroke="rgba(0,0,0,1)"
                        fontWeight="100"
                        fontSize="13px"
                        textAnchor="middle"
                    >
                        {distress0}
                    </text>
                )}

                {distress1 !== null && (
                    <text
                        x="185"
                        y="139"
                        stroke="rgba(0,0,0,1)"
                        fontWeight="100"
                        fontSize="13px"
                        textAnchor="middle"
                    >
                        {distress1}
                    </text>
                )}
            </g>

            <text
                x="100"
                y="90"
                stroke="rgba(151,151,151,1)"
                fontSize="11px"
                letterSpacing="-0.18px"
                textAnchor="middle"
            >
                {computeTimestamp(checkInTime0)
                    .split(' ')
                    .map((value, idx) => (
                        <tspan key={value} x="105" textAnchor="middle" dy={idx * 15}>
                            {value}
                        </tspan>
                    ))}
            </text>

            <text
                x="100"
                y="90"
                stroke="rgba(151,151,151,1)"
                fontSize="11px"
                letterSpacing="-0.18px"
                textAnchor="middle"
            >
                {computeTimestamp(checkInTime1)
                    .split(' ')
                    .map((value, idx) => (
                        <tspan key={value} x="280" textAnchor="middle" dy={idx * 15}>
                            {value}
                        </tspan>
                    ))}
            </text>

            <FrustrationCircle cx={0} cy={120} />
            <text x="15" y="124" stroke="rgba(0,0,0,1)" fontWeight="100" fontSize="13px">
                Agitation
            </text>

            <DistressCircle cx={0} cy={140} />
            <text x="15" y="144" stroke="rgba(0,0,0,1)" fontWeight="100" fontSize="13px">
                Distress
            </text>
        </svg>
    );
};

export default Chart;
