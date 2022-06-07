import React from 'react';
import styles from './index.module.scss';

interface Props {
    className?: string;
    size: number;
    onClick: (event: React.SyntheticEvent<HTMLDivElement, MouseEvent | TouchEvent>) => void;
}

const CrossedPlus = (props: Props) => {
    const { className = '', size, onClick } = props;
    return (
        <div
            className={`${styles.crossedPlus} ${className}`}
            data-cross // Allow other components to select for CSS this way if needed.
            onClick={onClick}
            style={{ width: `${size}px`, height: `${size}px`, borderRadius: `${size / 2}px` }}
        >
            <span style={{ fontSize: `${size / 20}vw` }}>&#x2716;</span>
        </div>
    );
};

export { CrossedPlus };
export default CrossedPlus;
