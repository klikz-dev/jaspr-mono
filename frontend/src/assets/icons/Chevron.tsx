type Direction = 'left' | 'right' | 'up' | 'down';

const Chevron = ({
    color = '#000000',
    direction,
    height = 22,
}: {
    direction?: Direction;
    color?: string;
    height?: number;
}) => {
    const getDegrees = (direction: Direction) => {
        switch (direction) {
            case 'left':
                return '-90deg';
            case 'right':
                return '90deg';
            case 'down':
                return '0deg';
            default:
                return '180deg';
        }
    };

    const width = height * 1.6923;
    return (
        <svg
            width={width}
            height={height}
            viewBox="0 0 22 13"
            fill="none"
            style={{
                transform: `rotate(${getDegrees(direction)})`,
                transition: 'transform 0.5s ease',
            }}
        >
            <path
                d="M21.0607 3.06066C21.6464 2.47487 21.6464 1.52513 21.0607 0.93934C20.4749 0.353553 19.5251 0.353553 18.9393 0.93934L21.0607 3.06066ZM11 11L9.93934 12.0607C10.5251 12.6464 11.4749 12.6464 12.0607 12.0607L11 11ZM3.06066 0.93934C2.47487 0.353553 1.52513 0.353553 0.939341 0.93934C0.353554 1.52513 0.353554 2.47487 0.939341 3.06066L3.06066 0.93934ZM18.9393 0.93934L9.93934 9.93934L12.0607 12.0607L21.0607 3.06066L18.9393 0.93934ZM12.0607 9.93934L3.06066 0.93934L0.939341 3.06066L9.93934 12.0607L12.0607 9.93934Z"
                fill={color}
            />
        </svg>
    );
};

export default Chevron;
