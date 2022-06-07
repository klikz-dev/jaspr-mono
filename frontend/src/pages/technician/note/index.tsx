import { useCallback, useContext, useEffect, useRef, useState } from 'react';
import copy from 'copy-to-clipboard';
import VisibilitySensor from 'react-visibility-sensor';
import { useHistory, useParams } from 'react-router-dom';
import axios from 'axios';
import Sentry from 'lib/sentry';
import Segment, { AnalyticNames } from 'lib/segment';
import StoreContext from 'state/context/store';
import config from '../../../config';
import { formatDateTime } from 'lib/helpers';
import closeButton from 'assets/closeX.svg';
import check from 'assets/check.svg';
import CommentCount from './commentCount';
import styles from './index.module.scss';
import { GetResponse as PatientGetResponse } from 'state/types/api/technician/patients/_id';
import { GetResponse as NoteGetResponse } from 'state/types/api/technician/patients/_id/note';
import {
    GetResponse as AmendmentGetResponse,
    PostResponse as AmendmentPostResponse,
    DeleteResponse as AmendmentDeleteResponse,
} from 'state/types/api/technician/encounter/_id/amendments';
import { PutResponse as AmendmentPutResponse } from 'state/types/api/technician/encounter/_id/amendments/_id';

const Note = () => {
    const [store, dispatch] = useContext(StoreContext);
    const params = useParams<{ patientId: string }>();
    const history = useHistory();
    const patientId = parseInt(params.patientId, 10);
    const { user } = store;
    const { authenticated } = user;
    const [patient, setPatient] = useState<PatientGetResponse>();
    const [note, setNote] = useState('');
    const [comments, setComments] = useState<AmendmentGetResponse>([]);
    const [editComment, setEditComment] = useState({ id: null, comment: '' });
    const [saving, setSaving] = useState(false);
    const [confirmDelete, setConfirmDelete] = useState(false);
    const [commentsInView, setCommentsInView] = useState(false);
    const [fadeOverlay, setFadeOverlay] = useState(false);
    const [commentIsDirty, setCommentIsDirty] = useState(false);

    const { firstName = '', lastName = '', ssid = '', mrn = '' } = patient;

    const noteRef = useRef<HTMLDivElement>(null!);
    const commentRef = useRef<HTMLDivElement>(null!);

    useEffect(() => {
        if (saving) {
            const fadeTimer = window.setTimeout(() => setFadeOverlay(true), 3000);
            const savingTimer = window.setTimeout(() => {
                setSaving(false);
                setFadeOverlay(false);
            }, 4000);
            return () => {
                window.clearTimeout(savingTimer);
                window.clearTimeout(fadeTimer);
            };
        }
    }, [saving]);

    const confirmAbandonEdit = useCallback(
        (e?: BeforeUnloadEvent) => {
            const message =
                'You have a comment with unsaved changes, are you sure you want to leave without saving?';
            if (e && commentIsDirty) {
                e.preventDefault();
                e.returnValue = message;
                Segment.track(AnalyticNames.TECHNICIAN_TRIED_TO_LEAVE_DIRTY_COMMENT);
                return message;
            } else if (commentIsDirty) {
                return window.confirm(message);
            }
        },
        [commentIsDirty],
    );

    useEffect(() => {
        window.addEventListener('beforeunload', confirmAbandonEdit);
        return () => window.removeEventListener('beforeunload', confirmAbandonEdit);
    }, [confirmAbandonEdit]);

    useEffect(() => {
        if (authenticated) {
            (async () => {
                try {
                    const response = await axios.get<PatientGetResponse>(
                        `${config.apiRoot}/technician/patients/${patientId}`,
                    );
                    const json = response.data;
                    setPatient(json);
                } catch (err) {
                    const { response } = err;
                    if (response?.status === 401) {
                        return dispatch({ type: 'RESET_APP' });
                    } else {
                        Sentry.captureException(err);
                    }
                }
            })();

            (async () => {
                try {
                    const response = await axios.get<NoteGetResponse>(
                        `${config.apiRoot}/technician/patients/${patientId}/note`,
                    );
                    const json = response.data;
                    setNote(json.narrativeNote);
                } catch (err) {
                    const { response } = err;
                    if (response?.status === 401) {
                        return dispatch({ type: 'RESET_APP' });
                    } else {
                        Sentry.captureException(err);
                    }
                }
            })();

            (async () => {
                try {
                    const response = await axios.get<AmendmentGetResponse>(
                        `${config.apiRoot}/technician/patients/${patientId}/amendments`,
                    );
                    const comments = response.data;
                    setComments(comments);
                } catch (err) {
                    const { response } = err;
                    if (response?.status === 401) {
                        return dispatch({ type: 'RESET_APP' });
                    } else {
                        Sentry.captureException(err);
                    }
                }
            })();
        }
    }, [dispatch, authenticated, patientId]);

    useEffect(() => {
        if (!editComment.id && editComment.comment) {
            // New comment
            setCommentIsDirty(true);
        } else if (
            editComment.id &&
            comments.find((comment) => comment.id === editComment.id)?.comment !==
                editComment.comment
        ) {
            // Existing comment has changed
            setCommentIsDirty(true);
        } else {
            setCommentIsDirty(false);
        }
    }, [comments, editComment.comment, editComment.id]);

    const copyToClipboard = () => {
        let data = note;
        comments.forEach((comment) => {
            data =
                data +
                `\n\n${comment.technician.email}\n${formatDateTime(comment.created)}\n${
                    comment.comment
                }`;
        });
        copy(data, {
            format: 'text/plain',
        });
        Segment.track(AnalyticNames.NOTE_COPIED_TO_CLIPBOARD, { patient: patient.analyticsToken });
    };

    const saveComment = async () => {
        if (!commentIsDirty) {
            setEditComment({ id: null, comment: '' });
            return;
        }

        try {
            setSaving(true);
            if (editComment.id) {
                // Edit comment
                const response = await axios.put<AmendmentPutResponse>(
                    `${config.apiRoot}/technician/patients/${patientId}/amendments/${editComment.id}`,
                    {
                        ...editComment,
                    },
                );
                const updatedComment = response.data;
                setComments(
                    comments.map((comment) =>
                        comment.id === editComment.id ? updatedComment : comment,
                    ),
                );
                setEditComment({ id: null, comment: '' });
                Segment.track(AnalyticNames.NOTE_MODIFIED_COMMENT_ON_NOTE);
            } else {
                // New comment
                const response = await axios.post<AmendmentPostResponse>(
                    `${config.apiRoot}/technician/patients/${patientId}/amendments`,
                    {
                        ...editComment,
                    },
                );
                const comment = response.data;
                setComments([...comments, comment]);
                setEditComment({ id: null, comment: '' });
                Segment.track(AnalyticNames.NOTE_ADDED_COMMENT_TO_NOTE);
            }
        } catch (err) {
            const { response } = err;
            if (response?.status === 401) {
                return dispatch({ type: 'RESET_APP' });
            }
        }
    };

    const close = () => {
        if (commentIsDirty) {
            if (confirmAbandonEdit()) {
                history.goBack();
            }
        } else {
            history.goBack();
        }
    };

    const clearComment = () => {
        setEditComment({ id: null, comment: '' });
        setConfirmDelete(false);
    };

    const deleteComment = async () => {
        if (editComment.id) {
            try {
                if (editComment.id) {
                    // Edit comment
                    await axios.delete<AmendmentDeleteResponse>(
                        `${config.apiRoot}/technician/patients/${patientId}/amendments/${editComment.id}`,
                    );
                    setComments(comments.filter((comment) => comment.id !== editComment.id));
                }
            } catch (err) {
                const { response } = err;
                if (response?.status === 401) {
                    return dispatch({ type: 'RESET_APP' });
                }
            }
        }
        setEditComment({ id: null, comment: '' });
        setConfirmDelete(false);
    };

    return (
        <div className={styles.container}>
            <header>
                <div className={styles.meta}>
                    ID:
                    <br />
                    <span>{ssid ? `SSID: ${ssid}` : `MRN: ${mrn}`}</span>
                </div>
                <div className={styles.meta}>
                    Name:
                    <br />
                    <span>
                        {lastName}
                        {firstName && lastName ? ', ' : ''}
                        {firstName}
                    </span>
                </div>
                <div className={styles.buttons}>
                    <span className={styles.close} onClick={close}>
                        Close
                    </span>
                    <button onClick={copyToClipboard}>Copy to Clipboard</button>
                </div>
            </header>
            <div className={styles.content}>
                <CommentCount
                    count={comments.length}
                    commentsInView={commentsInView}
                    noteRef={noteRef}
                    commentRef={commentRef}
                />
                <div className={styles.note}>
                    <div className={styles.noteText} ref={noteRef}>
                        {note}
                    </div>
                    <VisibilitySensor
                        partialVisibility
                        onChange={(isVisible) => setCommentsInView(isVisible)}
                    >
                        <div className={styles.comments} ref={commentRef}>
                            {comments
                                .sort((a, b) => a.created.localeCompare(b.created))
                                .map((comment) => {
                                    /*
                                    <Comment
                                        key={comment.id}
                                        setEditComment={setEditComment}
                                        comment={comment}
                                        commentIsDirty={commentIsDirty}
                                    />*/
                                    return null;
                                })}
                        </div>
                    </VisibilitySensor>
                </div>
                <div className={styles.commentEditor}>
                    <div className={styles.commentHeader}>
                        New Comment
                        {editComment.comment && (
                            <img onClick={clearComment} src={closeButton} alt="Clear Comment" />
                        )}
                    </div>
                    <textarea
                        value={editComment.comment}
                        onChange={({ target }) => {
                            setEditComment({ ...editComment, comment: target.value });
                        }}
                    />

                    <div className={styles.buttons}>
                        {Boolean(editComment.id) && (
                            <span className={styles.delete} onClick={() => setConfirmDelete(true)}>
                                Delete
                            </span>
                        )}
                        <button
                            style={{ marginLeft: 'auto' }}
                            disabled={!editComment.id && !editComment.comment}
                            onClick={saveComment}
                        >
                            {commentIsDirty ? 'Save' : 'Cancel'}
                        </button>
                    </div>
                    {saving && (
                        <div className={`${styles.overlay} ${fadeOverlay ? styles.fade : ''}`}>
                            <div className={styles.overlayContent}>
                                <img src={check} alt="Comment saved successfully" />
                                <span className={styles.overlayBigText}>Comment Saved</span>
                            </div>
                            <div className={styles.overlayFooter}>
                                Go to comment to make any changes
                            </div>
                        </div>
                    )}
                    {confirmDelete && (
                        <div className={styles.overlay}>
                            <div className={styles.overlayContent}>
                                <span className={styles.overlayMedText}>
                                    Are you sure you want to delete this comment?
                                </span>
                                <span className={styles.overlaySmallText}>
                                    This action cannot be undone.
                                </span>
                                <div className={styles.buttons}>
                                    <button onClick={() => setConfirmDelete(false)}>No</button>
                                    <button className={styles.hallow} onClick={deleteComment}>
                                        Yes
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Note;
