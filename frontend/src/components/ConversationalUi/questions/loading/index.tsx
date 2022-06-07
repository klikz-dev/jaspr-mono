import styles from './index.module.scss';

const Loading = (): JSX.Element => {
    return (
        <div className={styles.loading}>
            <span className={styles.dot} />
            <span className={styles.dot} />
            <span className={styles.dot} />
        </div>
    );
};

export { Loading };
export default Loading;
