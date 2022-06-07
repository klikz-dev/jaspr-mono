import React, { useState } from 'react';
import useAxios from 'lib/useAxios';
import Segment, { AnalyticNames } from 'lib/segment';
import Comment from './Comment';
import Button from '../../../../components/Button';
import { PostResponse } from 'state/types/api/technician/encounter/_id/amendments';
import { PutResponse } from 'state/types/api/technician/encounter/_id/amendments/_id';
import styles from './index.module.scss';

interface CommentProps {
    id: number | null;
    comment: string;
    technician?: {
        id: number;
        email: string;
        canEdit: boolean;
    };
    created: string;
    modified: string;
    noteType: 'stability-plan' | 'narrative-note'; // TODO Review if this is sent over wire
}

interface CommentsProps {
    open?: boolean;
    currentEncounter: number;
    comments: CommentProps[];
    setComments: (comment: CommentProps[] | ((comment: CommentProps[]) => CommentProps[])) => void;
    noteType: 'stability-plan' | 'narrative-note';
}

const Comments = React.forwardRef<HTMLDivElement, CommentsProps>(
    ({ open = false, comments, setComments, currentEncounter, noteType }, ref) => {
        const axios = useAxios();
        const [commentIsDirty, setCommentIsDirty] = useState(false);
        const [saving, setSaving] = useState(false);
        const [comment, setComment] = useState<Pick<CommentProps, 'id' | 'noteType' | 'comment'>>({
            id: null,
            noteType,
            comment: '',
        });

        const onChange = ({ target }: React.ChangeEvent<HTMLTextAreaElement>) => {
            setCommentIsDirty(true);
            setComment({
                ...comment,
                comment: target.value,
            });
        };

        const saveComment = async () => {
            if (!commentIsDirty) {
                setComment({
                    id: null,
                    noteType,
                    comment: '',
                });
                return;
            }

            try {
                setSaving(true);
                if (comment.id) {
                    // Edit comment
                    const response = await axios.put<PutResponse>(
                        `/technician/encounter/${currentEncounter}/amendments/${comment.id}`,
                        {
                            ...comment,
                            noteType,
                        },
                    );
                    const updatedComment = response.data;
                    setComments((comments) =>
                        comments.map((originalComment) =>
                            originalComment.id === comment.id ? updatedComment : originalComment,
                        ),
                    );
                    setComment({ id: null, noteType, comment: '' });
                    setSaving(false);
                    Segment.track(AnalyticNames.NOTE_MODIFIED_COMMENT_ON_NOTE, noteType);
                } else {
                    // New comment
                    const response = await axios.post<PostResponse>(
                        `/technician/encounter/${currentEncounter}/amendments`,
                        {
                            noteType,
                            comment: comment.comment,
                        },
                    );
                    const commentResponse = response.data;
                    setComments((comments) => [...comments, commentResponse]);
                    setComment({
                        id: null,
                        noteType,
                        comment: '',
                    });
                    Segment.track(AnalyticNames.NOTE_ADDED_COMMENT_TO_NOTE, noteType);
                    setSaving(false);
                }
            } catch (err) {
                setSaving(false);
            }
        };

        return (
            <div
                className={styles.comments}
                ref={ref}
                style={{ display: open ? 'inherit' : 'none' }}
            >
                <div className={styles.previousComments}>
                    {comments
                        .sort((a, b) => a.created.localeCompare(b.created))
                        .map((comment) => (
                            // @ts-ignore   // TODO Fix when we add editing
                            <Comment key={comment.id} setComment={setComment} comment={comment} />
                        ))}
                </div>
                <div className={styles.newComment}>
                    <span className={styles.title}>
                        {comment.id ? 'Edit Comment' : 'New Comment'}
                    </span>
                    <textarea value={comment.comment} onChange={onChange} disabled={saving} />
                    <Button
                        label="Save"
                        disabled={saving || comment.comment.length === 0}
                        onClick={saveComment}
                    />
                </div>
            </div>
        );
    },
);

export default Comments;
