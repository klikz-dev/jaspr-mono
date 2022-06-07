import React, { useRef, useState } from 'react';
import useClickOutside from 'lib/useClickOutside';
import styles from './index.module.scss';

interface SectionProps {
    number: string; // Stringified number
    title: string;
    tooltip: string;
    children: React.ReactNode;
}

const Section = ({ number, title, tooltip, children }: SectionProps) => {
    const [showTooltip, setShowTooltip] = useState(false);
    const containerRef = useRef<HTMLDivElement>(null!);

    useClickOutside(containerRef, () => setShowTooltip(false), showTooltip);

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <div className={styles.number}>{number}</div>
                <div className={styles.title}>{title}</div>
                {Boolean(tooltip) && (
                    <div className={styles.tooltip}>
                        <div className={styles.tipIcon} onMouseDown={() => setShowTooltip(true)}>
                            i
                        </div>
                        {showTooltip && (
                            <div className={styles.tooltipContainer} ref={containerRef}>
                                <div className={styles.tooltipText}>{tooltip}</div>
                                <button
                                    className={styles.tooltipClose}
                                    onClick={() => setShowTooltip(false)}
                                >
                                    Close
                                </button>
                            </div>
                        )}
                    </div>
                )}
            </div>

            <div className={styles.content}>{children}</div>
        </div>
    );
};

export default Section;
