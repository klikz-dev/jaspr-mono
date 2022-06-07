import styles from './index.module.scss';

type Props = {
    size: number;
    onClick: () => void;
};

const Plus = (props: Props) => {
    const { size, onClick } = props;
    return (
        <div
            className={styles.plus}
            data-plus // Allow other components to select for CSS this way if needed.
            onClick={onClick}
            style={{ width: `${size}px`, height: `${size}px`, borderRadius: `${size / 2}px` }}
        >
            {/* <span style={{ fontSize: `${size / 10}vw` }}>+</span> */}
            <span style={{ fontSize: `${size}px` }}>+</span>
        </div>
    );
};

export { Plus };
export default Plus;
