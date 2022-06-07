const Pencil = ({
    color = '#ffffff',
    height = 20,
    ariaHidden = false,
}: {
    color?: string;
    height?: number;
    ariaHidden?: boolean;
}) => {
    const width = height;
    return (
        <svg
            width={width}
            height={height}
            viewBox="0 0 29 29"
            aria-hidden={ariaHidden ? 'true' : 'false'}
        >
            <g stroke="none" strokeWidth="1" fill="none" fillRule="evenodd">
                <g transform="translate(-613.000000, -362.000000)" stroke={color}>
                    <g id="Edit-Pencil" transform="translate(614.000000, 363.000000)">
                        <g transform="translate(14.000000, 13.500000) rotate(-45.000000) translate(-14.000000, -13.500000) translate(-1.000000, 10.000000)">
                            <path d="M6.05853359,-3.63797881e-12 L28.3579362,-3.63797881e-12 C28.7721498,-3.6380549e-12 29.1079362,0.335786438 29.1079362,0.75 L29.1079362,6 C29.1079362,6.41421356 28.7721498,6.75 28.3579362,6.75 L6.05853359,6.75 C5.92711178,6.75 5.79799709,6.71546658 5.6841229,6.64985894 L0.281987571,3.53746473 C0.192260776,3.48576941 0.16143018,3.37112412 0.213125508,3.28139733 C0.229613796,3.25277886 0.2533691,3.22902355 0.281987571,3.21253527 L5.6841229,0.100141062 C5.79799709,0.0345334244 5.92711178,-3.64039145e-12 6.05853359,-3.63797881e-12 Z"></path>
                            <line
                                x1="23.8388348"
                                y1="6.68198052"
                                x2="23.8388348"
                                y2="0.681980515"
                                id="Line-2"
                                strokeLinecap="round"
                            ></line>
                        </g>
                        <polyline points="5.28058228 17.4360889 6.65751415 20.6574222 10.110864 22.2618678"></polyline>
                    </g>
                </g>
            </g>
        </svg>
    );
};

export default Pencil;
