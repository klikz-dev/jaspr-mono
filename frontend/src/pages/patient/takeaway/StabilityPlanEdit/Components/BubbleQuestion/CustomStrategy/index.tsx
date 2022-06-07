import React, { useEffect, useRef, useState } from 'react';
import AddButton from '../../AddButton';
import styles from './index.module.scss';

interface CustomStrategyProps {
    setAnswer: (answer: string[]) => void;
    answer: string[];
}

const CustomStrategy = ({ setAnswer, answer }: CustomStrategyProps) => {
    const [isEditing, setIsEditing] = useState(false);
    const [strategy, setStrategy] = useState('');
    const inputRef = useRef<HTMLInputElement>(null!);
    const measureRef = useRef<HTMLDivElement>(null!);

    const saveStrategy = () => {
        if (strategy !== '' && !answer.includes(strategy)) {
            setAnswer([...answer, strategy]);
        }
        setIsEditing(false);
        setStrategy('');
    };

    useEffect(() => {
        if (isEditing && inputRef && inputRef.current) {
            inputRef.current.focus();
        }
    }, [inputRef, isEditing]);

    const onEnter = (e: React.KeyboardEvent<HTMLInputElement>) => {
        // TODO Update deprecated keyCode
        if (e.keyCode === 13) {
            // Enter key
            saveStrategy();
        }
    };

    const calculateWidth = () => {
        const width = measureRef?.current?.clientWidth;
        if (width > 110) {
            return width + 30; // 15 px padding on each side
        }
        return 127;
    };

    if (isEditing) {
        return (
            <>
                <div className={styles.measure} ref={measureRef}>
                    {strategy}
                </div>
                {/* Hidden div used for measuring text length */}
                <input
                    type="text"
                    ref={inputRef}
                    autoFocus // for mobile safari
                    value={strategy}
                    onChange={(e) => {
                        setStrategy(e.target.value);
                    }}
                    className={styles.input}
                    onKeyDown={onEnter}
                    onBlur={saveStrategy}
                    maxLength={10000}
                    style={{ width: calculateWidth() }}
                />
            </>
        );
    }
    return <AddButton label="Add custom" onClick={() => setIsEditing(true)} />;
};

export default CustomStrategy;
