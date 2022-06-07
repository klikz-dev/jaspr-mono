import { useEffect, useState, forwardRef, CSSProperties } from 'react';
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
    DraggableAttributes,
} from '@dnd-kit/core';
import {
    arrayMove,
    useSortable,
    SortableContext,
    verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { restrictToParentElement, restrictToVerticalAxis } from '@dnd-kit/modifiers';
import { CSS } from '@dnd-kit/utilities';
import { useQuestion } from 'components/ConversationalUi/hooks/useQuestion';
import styles from './index.module.scss';
import { QuestionProps } from '../../question';
import { SyntheticListenerMap } from '@dnd-kit/core/dist/hooks/utilities';

const Item = forwardRef<
    HTMLDivElement,
    {
        id: string;
        answer: string;
        idx: number;
        style: CSSProperties;
        listeners: SyntheticListenerMap;
        attributes: DraggableAttributes;
        setEditing: (index: number) => void;
    }
>(({ idx, answer, setEditing, listeners, attributes, style }, ref) => {
    return (
        <div className={styles.reason} style={style} ref={ref}>
            <span className={styles.drag} {...listeners} {...attributes} />
            <span className={styles.content}>{answer}</span>
            <span className={styles.edit} onClick={() => setEditing(idx)} />
        </div>
    );
});

const SortableItem = ({
    id,
    idx,
    answer,
    active,
    setEditing,
}: {
    id: string;
    idx: number;
    answer: string;
    active: boolean;
    setEditing: (index: number) => void;
}) => {
    const { attributes, listeners, setNodeRef, transform, transition } = useSortable({
        id: idx.toString(),
    });

    const style: CSSProperties = {
        transform: CSS.Transform.toString(transform),
        transition,
        touchAction: 'none',
    };

    if (active) {
        style['zIndex'] = 2;
        style['borderTop'] = '1px solid #979797';
        style['backgroundColor'] = 'white';
    }

    return (
        <Item
            ref={setNodeRef}
            style={style}
            answer={answer}
            attributes={attributes}
            listeners={listeners}
            setEditing={setEditing}
            id={id}
            idx={idx}
        />
    );
};

type SortEditQuestionProps = Pick<QuestionProps, 'answerKey' | 'setAnswered' | 'answered'>;

const SortEditQuestion = (props: SortEditQuestionProps) => {
    const { answerKey, setAnswered, answered } = props;
    const [, updatedAnswer, setAnswer, saveAnswer] = useQuestion<string[]>(answerKey, [], false);
    const [editing, setEditing] = useState<number | null>(null);
    const [activeId, setActiveId] = useState(null);

    const keyboardCoordinatesGetter: KeyboardCoordinateGetter = (event, { currentCoordinates }) => {
        const delta = 57;
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
            const oldIndex = parseInt(active.id);
            const newIndex = parseInt(over.id);
            setAnswer(arrayMove(updatedAnswer, oldIndex, newIndex));
        }
        setActiveId(null);
    };

    useEffect(() => {
        if (answered) {
            saveAnswer();
        }
    }, [answered, saveAnswer]);

    return (
        <div className={styles.container}>
            <div
                className={styles.header}
                style={{ filter: editing !== null ? 'blur(10px)' : 'none' }}
            >
                <span>Reasons for Living</span>
            </div>
            {editing !== null && (
                <div className={styles.editor}>
                    <input
                        value={updatedAnswer[editing]}
                        autoFocus
                        onChange={(e) => {
                            const newAnswers = [...updatedAnswer];
                            newAnswers[editing] = e.target.value;
                            setAnswer(newAnswers);
                            setAnswered(false);
                        }}
                    />
                    <div
                        className={styles.trash}
                        onClick={() => {
                            const newAnswers = [...updatedAnswer];
                            newAnswers.splice(editing, 1);
                            setAnswer(newAnswers);
                            setEditing(null);
                            setAnswered(false);
                        }}
                    />
                    <div className={styles.done} onClick={() => setEditing(null)}>
                        Done
                    </div>
                </div>
            )}

            <DndContext
                sensors={sensors}
                collisionDetection={closestCenter}
                onDragStart={handleDragStart}
                onDragEnd={handleDragEnd}
                modifiers={[restrictToVerticalAxis, restrictToParentElement]}
            >
                <SortableContext
                    items={updatedAnswer.map((_, idx) => idx.toString())}
                    strategy={verticalListSortingStrategy}
                >
                    <div
                        className={styles.sortableContainer}
                        style={{ filter: editing !== null ? 'blur(10px)' : 'none' }}
                    >
                        {updatedAnswer.map((answer, idx) => (
                            <SortableItem
                                key={idx}
                                answer={answer}
                                id={idx.toString()}
                                setEditing={setEditing}
                                idx={idx}
                                active={activeId === answer}
                            />
                        ))}
                    </div>
                </SortableContext>
            </DndContext>

            {updatedAnswer.length < 5 && (
                <div
                    className={styles.add}
                    style={{ filter: editing !== null ? 'blur(10px)' : 'none' }}
                    onClick={() => {
                        const newAnswers = [...updatedAnswer];
                        newAnswers.push('');
                        setAnswer(newAnswers);
                        setAnswered(false);
                    }}
                >
                    Add another
                </div>
            )}
        </div>
    );
};

export { SortEditQuestion };
export default SortEditQuestion;
