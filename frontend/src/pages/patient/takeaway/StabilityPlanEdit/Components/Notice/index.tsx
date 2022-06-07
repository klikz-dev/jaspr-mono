import styles from './index.module.scss';

interface NoticeProps {
    text: string;
    close: () => void;
}

const Notice = ({ text, close }: NoticeProps) => {
    return (
        <>
            <div className={styles.text}>{text}</div>
            <div className={styles.button} onClick={close}>
                Close
            </div>
        </>
    );
};

export default Notice;
