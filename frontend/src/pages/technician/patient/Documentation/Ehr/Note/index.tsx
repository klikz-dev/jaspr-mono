import { useState } from 'react';
import Checkbox from 'components/Checkbox';
import styles from './index.module.scss';
import Chevron from 'assets/icons/Chevron';

interface NoteProps {
    checked: boolean;
    setChecked: (checked: boolean) => void;
    label: string;
    description?: string;
    active?: boolean;
    status?: string;
    note: string;
    noteType: 'stability-plan' | 'narrative-note';
    currentEncounter: number;
}

const Note = ({
    checked,
    setChecked,
    label,
    description = '',
    note = '',
    active = false,
    status = 'Not Assigned',
    noteType,
    currentEncounter,
}: NoteProps) => {
    const [open, setOpen] = useState(false);

    return (
        <div className={styles.note}>
            <div className={styles.controls}>
                <Checkbox
                    checked={active ? checked : false}
                    onChange={({ target }) => setChecked(target.checked)}
                    disabled={!active}
                />
                <div
                    className={`${styles.metadata} ${active ? styles.active : styles.inactive}`}
                    onClick={() => setOpen((open) => !open)}
                >
                    <span
                        className="typography--overline"
                        style={{ color: active ? '#4D4D4D' : '#7F7F7F' }}
                    >
                        {status}
                    </span>
                    <span className="typography--h6">{label}</span>
                    <span
                        className="typography--body2"
                        style={{ color: active ? '#4D4D4D' : '#7F7F7F' }}
                    >
                        {description}
                    </span>
                </div>

                {active && (
                    <span
                        className={`${styles.arrow} ${open ? styles.open : ''}`}
                        onClick={() => setOpen((open) => !open)}
                    >
                        <Chevron direction={open ? 'up' : 'down'} height={7} />
                    </span>
                )}
            </div>

            {active && (
                <div
                    className={`${styles.fulltext} ${open ? styles.open : ''}`}
                    style={{ maxHeight: open ? 10000 : 0 }}
                >
                    {note}
                </div>
            )}
        </div>
    );
};

export default Note;
