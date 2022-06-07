import styles from './index.module.scss';

type SavedSharedStoriesListItemAddProps = {
    onAdd: () => void;
};

const SavedSharedStoriesListItemAdd = (props: SavedSharedStoriesListItemAddProps): JSX.Element => {
    const { onAdd } = props;

    return (
        <li className={styles.regularItem} onClick={onAdd}>
            <div
                className={styles.verticalPlusLine}
                style={{ transform: 'translate(-50%, -50%)' }}
            />
            <div
                className={styles.horizontalPlusLine}
                style={{ transform: 'translate(-50%, -50%)' }}
            />
        </li>
    );
};

export default SavedSharedStoriesListItemAdd;
