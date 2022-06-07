import React from 'react';
import { DateTime } from 'luxon';
import styles from './index.module.scss';
import { Preferences } from 'state/types';
import CircleCheck from 'assets/icons/CircleCheck';

const formatTime = (datetime: string, timezone: string): string => {
    const date = DateTime.fromISO(datetime, { zone: timezone });
    if (!date.isValid) return '';
    return date.toFormat('h:mm a ZZZZ ON M/dd/yyyy');
};

export type StatusType = 'Not Started' | 'In Progress' | 'Completed' | 'Updated';
export type ActivityType =
    | 'outro'
    | 'intro'
    | 'lethal_means'
    | 'comfort_and_skills'
    | 'suicide_assessment'
    | 'stability_plan'
    | 'jah';

interface BoxProps {
    children?: React.ReactNode;
    status: StatusType;
    type: ActivityType;
    title: string;
    completedTimestamp?: string; // 2020-07-24T17:55:05.357000Z
    assigned?: boolean;
    preferences?: Preferences;
}

const Section = ({
    children,
    status = 'Not Started',
    type,
    title,
    completedTimestamp,
    assigned = true,
    preferences = {
        timezone: 'America/New_York',
        providerNotes: false,
        stabilityPlanLabel: 'Stability Plan',
    },
}: BoxProps) => {
    const { timezone = 'America/New_York' } = preferences;

    return (
        <div className={`${styles.section} ${assigned ? styles.assigned : styles.unassigned}`}>
            {type !==
                'comfort_and_skills' /* TODO For activities without forward progress, like C&S */ && (
                <CircleCheck showCheck={status === 'Completed' || status === 'Updated'} />
            )}
            {type === 'comfort_and_skills' && <div className={styles.assignedCircle} />}
            <div className={`typography--overline ${styles.status}`}>
                {status}{' '}
                {(status === 'Completed' || status === 'Updated') &&
                    completedTimestamp &&
                    formatTime(completedTimestamp, timezone)}
            </div>
            <h6>{title}</h6>
            {children}
        </div>
    );
};

export default Section;
