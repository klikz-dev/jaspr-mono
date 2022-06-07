import styles from './index.module.scss';

interface BookmarkProps {
    title: string;
    description: string;
    Icon: any;
    navigateTo: (route: string) => void; // Route
}

const Bookmark = ({ title, description, Icon, navigateTo }: BookmarkProps) => {
    return (
        <div
            className={styles.bookmark}
            style={{ cursor: 'pointer' }}
            onClick={() => navigateTo('/takeaway')}
        >
            <div className={`${styles.iconContainer} ${styles.iconContainerWeb}`}>
                <Icon height={42} color="rgba(255,255,255,0.3)" />
            </div>
            <div className={styles.info}>
                <div className={styles.title}>{title}</div>
                <p className={styles.description}>{description}</p>
            </div>
        </div>
    );
};

export default Bookmark;
