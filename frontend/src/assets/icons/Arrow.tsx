type Direction = 'left' | 'right' | 'up' | 'down';

const Arrow = ({ color = '#117383', direction }: { direction?: Direction; color?: string }) => {
    const getDegrees = (direction: Direction) => {
        switch (direction) {
            case 'left':
                return '0deg';
            case 'right':
                return '180deg';
            case 'down':
                return '-90deg';
            default:
                return '90deg';
        }
    };
    return (
        <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            style={{ transform: `rotate(${getDegrees(direction)})` }}
        >
            <path
                d="M12 19.5L4.5 12L12 4.5"
                stroke={color}
                strokeWidth="3"
                strokeLinecap="round"
                strokeLinejoin="round"
            />
            <path d="M4.5 12H21" stroke={color} strokeWidth="3" strokeLinecap="round" />
        </svg>
    );
};

export default Arrow;
