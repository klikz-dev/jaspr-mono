import React, { useContext, useState } from 'react';
import useAxios from 'lib/useAxios';
import StoreContext from 'state/context/store';
import styles from './index.module.scss';
import { AnswerKeyType } from 'components/ConversationalUi/questions';
import { Technician } from 'state/types';
import {
    GetResponse as ProviderCommentsGetResponse,
    PostResponse as ProviderCommentsPostResponse,
    ProviderComment,
} from 'state/types/api/technician/encounter/_id/provider-comments';
import Segment, { AnalyticNames } from 'lib/segment';

interface ProviderNotesProps {
    currentEncounter: number;
    answerKey: AnswerKeyType;
    indent?: boolean;
    enabled?: boolean;
    providerComments: ProviderCommentsGetResponse;
    setProviderComments: (providerComments: ProviderCommentsGetResponse) => void;
}

const ProviderComments = ({
    currentEncounter,
    providerComments = {},
    answerKey,
    indent = false,
    setProviderComments,
    enabled = true,
}: ProviderNotesProps) => {
    const axios = useAxios();
    const [store] = useContext(StoreContext);
    const { firstName, lastName, id, email } = store.user as Technician;
    const [comment, setComment] = useState('');
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState('');
    const [editing, setEditing] = useState(false);

    if (!enabled) return null;

    // Grow text area height to match text
    const adjustTextAreaHeight = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        const el = e.target;
        // @ts-ignore
        el.style.height = el.scrollHeight >= el.clientHeight ? el.scrollHeight + 'px' : '21px';
    };

    const submit = async (body: { answerKey: string; comment: string }) => {
        try {
            const response = await axios.post<ProviderCommentsPostResponse>(
                `/technician/encounter/${currentEncounter}/provider-comments`,
                body,
            );

            const { data } = response;

            const updatedNotes = { ...providerComments };

            if (answerKey in updatedNotes) {
                updatedNotes[answerKey] = [...updatedNotes[answerKey], data];
            } else {
                updatedNotes[answerKey] = [data];
            }
            Segment.track(AnalyticNames.TECHNICIAN_CREATED_PROVIDER_COMMENT, { answerKey });
            setProviderComments(updatedNotes);
        } catch (err) {
            setComment(body.comment);
            setError('There was an error saving your note.  Please try again.');
        }

        setSubmitting(false);
    };

    const onKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter') {
            // submit
            // TODO Handle Editing too
            e.preventDefault();
            setSubmitting(true);
            setComment('');
            // @ts-ignore
            e.target.style.height = '21px';
            submit({ answerKey, comment });
        }
    };

    const renderTechnician = (technician: ProviderComment['technician']) => (
        <div className={styles.providerName}>
            {technician.lastName && (
                <span>
                    {technician.lastName}, {technician.firstName.substr(0, 1)}
                </span>
            )}
            {!technician.lastName && <span>{technician.email}</span>}
        </div>
    );

    return (
        <div className={`${styles.notes} ${indent ? styles.indent : ''}`}>
            {providerComments[answerKey]?.map((providerComment) => (
                <div className={styles.providerComment} key={providerComment.id}>
                    {renderTechnician(providerComment.technician)}
                    <div className={styles.providerNote}>{providerComment.comment}</div>
                </div>
            ))}
            {editing && (
                <div className={styles.providerName}>
                    {renderTechnician({ firstName, lastName, id, email, canEdit: true })}
                </div>
            )}
            <textarea
                onKeyUp={adjustTextAreaHeight}
                onKeyPress={onKeyPress}
                onChange={({ target }) => setComment(target.value)}
                value={comment}
                disabled={submitting}
                onFocus={() => setEditing(true)}
                onBlur={() => setEditing(false)}
            ></textarea>
            {error && <div className={styles.error}>{error}</div>}
        </div>
    );
};

export default ProviderComments;
