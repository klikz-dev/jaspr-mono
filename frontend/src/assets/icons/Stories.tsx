const Stories = ({
    color = '#ffffff',
    height = 20,
    ariaHidden = false,
}: {
    color?: string;
    height?: number;
    ariaHidden?: boolean;
}) => {
    const width = height * 1.19;
    return (
        <svg
            width={width}
            height={height}
            viewBox="0 0 50 42"
            fill="none"
            aria-hidden={ariaHidden ? 'true' : 'false'}
        >
            <g>
                <path
                    d="M30.0957 24.5449H22.2843C18.7356 24.5449 15.8965 20.3685 15.8965 16.7254V6.75343C15.8965 3.34632 18.4567 1 22.2843 1H42.8915C46.6376 1 48.9999 3.34632 48.9999 6.75343V16.7254C48.9999 19.0157 47.9608 21.1217 46.2442 22.3409L48.6662 28.7253C49.0199 29.6615 48.0185 30.4963 47.1585 30.0365L37.5786 24.2781"
                    stroke={color}
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                />
                <path
                    d="M19.6519 12.6667H27.895C31.7476 12.6667 34.0759 14.6288 34.0759 17.9682V28.2318C34.0759 31.8123 31.4016 35.8165 27.8422 35.8165L24.1217 35.811H24.8736H16.2821L2.92215 40.8827C1.92206 41.3287 1.19854 40.4139 1.46508 39.6294L3.86883 33.5561C2.10053 32.3309 1 30.2154 1 27.9278V17.9682C1 14.6288 3.35034 12.6667 7.28666 12.6667H11.5037"
                    stroke={color}
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                />
            </g>
        </svg>
    );
};

export default Stories;
