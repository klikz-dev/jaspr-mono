import { formatDateTime } from 'lib/helpers';
import pencil from 'assets/pencil.svg';
import styles from './index.module.scss';
import { GetResponse } from 'state/types/api/technician/encounter/_id/amendments/_id';

interface CommentProps {
    comment: Pick<GetResponse, 'id' | 'comment' | 'noteType' | 'technician' | 'created'>;
    commentIsDirty: boolean;
    setComment: (comment: Pick<GetResponse, 'id' | 'comment' | 'noteType'>) => void;
}

const Comment = ({ comment, commentIsDirty, setComment }: CommentProps) => {
    const { created, comment: text, technician } = comment;
    const { email, canEdit } = technician;

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <span>{formatDateTime(created)}</span>
                &nbsp;-&nbsp;
                <span>{email}</span>
            </div>
            {text}
            {canEdit && !commentIsDirty && (
                <img
                    className={styles.editButton}
                    alt="Edit comment"
                    src={pencil}
                    onClick={() => setComment(comment)}
                />
            )}
        </div>
    );
};

export default Comment;
