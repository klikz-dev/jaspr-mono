import { useContext, useEffect, useState, forwardRef, CSSProperties } from 'react';
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
import StoreContext from 'state/context/store';
import { useQuestion } from 'components/ConversationalUi/hooks/useQuestion';
import hamburger from 'assets/greyHamburger.png';
import styles from './index.module.scss';
import { QuestionProps } from '../../question';

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

type RankTopQuestionProps = Pick<QuestionProps, 'answerKey' | 'setAnswered' | 'answered'> & {
    dropTitle: string;
    targetCount: number;
    lists: string[];
};

const RankTopQuestion = (props: RankTopQuestionProps) => {
    const { answerKey, setAnswered, answered, lists, dropTitle, targetCount } = props;
    const [store] = useContext(StoreContext);
    const { assessment } = store;
    const { answers } = assessment;
    const [, updatedAnswer, setAnswer, saveAnswer] = useQuestion<string[]>(answerKey, [], false);
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
            const oldIndex = updatedAnswer.indexOf(active.id);
            const newIndex = updatedAnswer.indexOf(over.id);
            setAnswered && setAnswered(false);
            setAnswer(arrayMove(updatedAnswer, oldIndex, newIndex));
        }
        setActiveId(null);
    };

    const targetOptions = updatedAnswer;
    const sourceOptions = lists
        .map((list) =>
            (answers[list] || []).map((item: any) => {
                if (typeof item === 'object' && 'name' in item && 'phone' in item) {
                    return `${item.name} (${item.phone})`;
                }
                return item;
            }),
        )
        ?.flat()
        ?.filter((source) => !targetOptions.includes(source));

    const remove = (value: string): void => {
        setAnswered(false);
        setAnswer(targetOptions.filter((option) => option !== value));
    };

    const add = (value: string): void => {
        setAnswered(false);
        if (targetOptions.length < targetCount) {
            setAnswer([...targetOptions, value]);
        }
    };

    useEffect(() => {
        if (answered) {
            saveAnswer();
        }
    }, [answered, saveAnswer]);

    const emptyArrayLength = targetCount - targetOptions.length;
    const canAddOptions = targetOptions.length < targetCount;
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
                            .map((_, emptyIndex) => (
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

export { RankTopQuestion };
export default RankTopQuestion;
