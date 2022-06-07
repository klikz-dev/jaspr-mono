import React from 'react';
import scrollIntoView from 'smooth-scroll-into-view-if-needed';
import chevron from 'assets/chevron.svg';
import styles from './index.module.scss';
import Segment, { AnalyticNames } from 'lib/segment';

interface CommentCountProps {
    commentsInView: boolean;
    count: number;
    noteRef: React.RefObject<HTMLDivElement>;
    commentRef: React.RefObject<HTMLDivElement>;
}

const CommentCount = ({ commentsInView, count, noteRef, commentRef }: CommentCountProps) => {
    const onClick = () => {
        scrollIntoView(commentsInView ? noteRef.current : commentRef.current, {
            behavior: 'smooth',
            block: 'start',
        });
        Segment.track(AnalyticNames.TECHNICIAN_SCROLLED_TO_NOTE_COMMENTS);
    };

    return (
        <div
            className={`${styles.container} ${commentsInView ? styles.commentView : ''}`}
            onClick={onClick}
        >
            <img className={styles.chevronDown} src={chevron} alt="" />
            {!commentsInView && (
                <>
                    <span className={styles.text}>Comments</span>
                    <div className={styles.count}>{count > 9 ? '9+' : count}</div>
                </>
            )}
        </div>
    );
};

export default CommentCount;
