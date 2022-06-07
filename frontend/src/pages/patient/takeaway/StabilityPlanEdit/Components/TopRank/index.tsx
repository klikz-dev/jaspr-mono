import { useCallback, useEffect, useState, useMemo, forwardRef, CSSProperties } from 'react';
import {
    DndContext,
    closestCenter,
    KeyboardSensor,
    PointerSensor,
    useSensor,
    useSensors,
    KeyboardCoordinateGetter,
    DragStartEvent,
    DragEndEvent,
} from '@dnd-kit/core';
import {
    arrayMove,
    useSortable,
    SortableContext,
    verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { restrictToParentElement, restrictToVerticalAxis } from '@dnd-kit/modifiers';
import { CSS } from '@dnd-kit/utilities';
import hamburger from 'assets/greyHamburger.png';
import styles from './index.module.scss';
import { AnswerKeyType } from 'components/ConversationalUi/questions';
import { AssessmentAnswers } from 'state/types';

const Item = forwardRef<
    HTMLDivElement,
    { id: string; remove: (id: string) => void; style: CSSProperties }
>(({ id, remove, ...props }, ref) => {
    return (
        <div className={`${styles.targetOption} ${styles.set}`} {...props} ref={ref}>
            <img alt="" src={hamburger} />
            <span className={styles.optionValue}>{id}</span>
            <span className={styles.delete} onClick={() => remove(id)}>
                &times;
            </span>
        </div>
    );
});

const SortableItem = ({ id, remove, active }: { id: string; remove: any; active: boolean }) => {
    const { attributes, listeners, setNodeRef, transform, transition } = useSortable({
        id,
    });

    const style: CSSProperties = {
        transform: CSS.Transform.toString(transform),
        transition,
        touchAction: 'none',
    };

    if (active) {
        style['zIndex'] = 2;
        style['borderBottom'] = '1px solid rgba(151, 151, 151, 1)';
    }

    return (
        <Item
            ref={setNodeRef}
            style={style}
            {...attributes}
            {...listeners}
            id={id}
            remove={remove}
        />
    );
};

interface RankTopQuestionProps {
    answerKey: AnswerKeyType;
    setAnswers: (
        answers:
            | Partial<AssessmentAnswers>
            | ((answers: Partial<AssessmentAnswers>) => Partial<AssessmentAnswers>),
    ) => void;
    answers: Partial<AssessmentAnswers>;
    lists: string[]; // ListType question key
    dropTitle: string;
    targetCount: number;
}

const RankTopQuestion = ({
    answerKey,
    setAnswers,
    answers,
    lists,
    dropTitle,
    targetCount,
}: RankTopQuestionProps) => {
    const [activeId, setActiveId] = useState(null);

    const keyboardCoordinatesGetter: KeyboardCoordinateGetter = (event, { currentCoordinates }) => {
        const delta = 64;
        switch (event.code) {
            case 'ArrowRight':
            case 'ArrowDown':
                return {
                    ...currentCoordinates,
                    y: currentCoordinates.y + delta,
                };
            case 'ArrowLeft':
            case 'ArrowUp':
                return {
                    ...currentCoordinates,
                    y: currentCoordinates.y - delta,
                };
        }

        return undefined;
    };

    const sensors = useSensors(
        useSensor(PointerSensor),
        useSensor(KeyboardSensor, {
            coordinateGetter: keyboardCoordinatesGetter,
        }),
    );

    const handleDragStart = ({ active }: DragStartEvent) => {
        setActiveId(active.id);
    };

    const handleDragEnd = ({ active, over }: DragEndEvent) => {
        if (active.id !== over.id) {
            const oldIndex = answers[answerKey].indexOf(active.id);
            const newIndex = answers[answerKey].indexOf(over.id);

            const newAnswers = [...answers[answerKey]];
            newAnswers.splice(newIndex, 0, newAnswers.splice(oldIndex, 1)[0]);
            setAnswers({
                ...answers,
                [answerKey]: arrayMove(answers[answerKey], oldIndex, newIndex),
            });
        }
        setActiveId(null);
    };

    const availableOptions: string[] = lists
        .map((list) =>
            (answers[list] || []).map((item: string | { phone: string; name: string }) => {
                if (typeof item === 'object' && 'name' in item && 'phone' in item) {
                    return `${item.name} (${item.phone})`;
                }
                return item;
            }),
        )
        ?.flat();

    const targetOptions: string[] = useMemo(() => answers[answerKey] || [], [answerKey, answers]);

    // Deduplicate options in case duplicate values have been entered on multiple questions
    const sourceOptions = [
        ...new Set(availableOptions?.filter((source) => !targetOptions.includes(source))),
    ];

    const answer: string[] = answers[answerKey];

    const remove = useCallback(
        (value) => {
            setAnswers((answers) => ({
                ...answers,
                [answerKey]: targetOptions.filter((option) => option !== value),
            }));
        },
        [answerKey, setAnswers, targetOptions],
    );

    const add = (value: string) => {
        if (targetOptions.length < targetCount) {
            setAnswers((answers) => ({
                ...answers,
                [answerKey]: [...targetOptions, value],
            }));
        }
    };

    const emptyArrayLength = targetCount - targetOptions.length;
    const canAddOptions = targetOptions.length < targetCount;

    useEffect(() => {
        (answer || []).forEach((option) => {
            if (!availableOptions.includes(option)) {
                remove(option);
            }
        });
    }, [answer, remove, availableOptions]);

    return (
        <div className={styles.container}>
            <div style={{ display: 'flex', flexGrow: 1 }}>
                <div className={styles.source}>
                    {sourceOptions.map((option, index) => (
                        <div className={styles.option} key={index}>
                            <span className={styles.optionValue}>{option}</span>
                            <span
                                className={styles.add}
                                style={{
                                    color: canAddOptions
                                        ? 'rgba(255,255,255,1)'
                                        : 'rgba(255,255,255,0.3)',
                                }}
                                onClick={() => add(option)}
                            >
                                &#xff0b;
                            </span>
                        </div>
                    ))}
                </div>
                <div className={styles.target}>
                    <div className={styles.header}>{dropTitle}</div>
                    <DndContext
                        sensors={sensors}
                        collisionDetection={closestCenter}
                        onDragStart={handleDragStart}
                        onDragEnd={handleDragEnd}
                        modifiers={[restrictToVerticalAxis, restrictToParentElement]}
                    >
                        <SortableContext
                            items={targetOptions}
                            strategy={verticalListSortingStrategy}
                        >
                            <div className={styles.ranker}>
                                {targetOptions.map((option) => (
                                    <SortableItem
                                        key={option}
                                        id={option}
                                        remove={remove}
                                        active={activeId === option}
                                    />
                                ))}
                            </div>
                        </SortableContext>
                    </DndContext>
                    {emptyArrayLength > 0 &&
                        new Array(emptyArrayLength)
                            .fill('')
                            .map((emptyItem, emptyIndex) => (
                                <div
                                    key={`empty-${emptyIndex}`}
                                    className={styles.targetOption}
                                ></div>
                            ))}
                </div>
            </div>
        </div>
    );
};

export default RankTopQuestion;
