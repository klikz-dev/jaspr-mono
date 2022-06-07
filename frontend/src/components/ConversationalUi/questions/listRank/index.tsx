import { CSSProperties, forwardRef, useEffect, useState } from 'react';
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

import { useQuestion } from 'components/ConversationalUi/hooks/useQuestion';
import hamburger from 'assets/greyHamburger.png';
import styles from './index.module.scss';
import { QuestionProps } from '../../question';

const Item = forwardRef<HTMLDivElement, { answer: string; idx: number; style: CSSProperties }>(
    ({ idx, answer, ...props }, ref) => {
        return (
            <div className={styles.rankItem} {...props} ref={ref}>
                <div className={styles.index}>{idx + 1}</div>
                <div className={styles.labels}>{answer}</div>
                <img alt="" src={hamburger} style={{ width: '12px', marginRight: '15px' }} />
            </div>
        );
    },
);

const SortableItem = ({
    answer,
    id,
    idx,
    active,
}: {
    answer: string;
    id: string;
    idx: number;
    active: boolean;
}) => {
    const { attributes, listeners, setNodeRef, transform, transition } = useSortable({
        id,
    });

    const style: CSSProperties = {
        transform: CSS.Transform.toString(transform),
        transition,
        touchAction: 'none',
    };

    if (active) {
        style['borderBottom'] = '1px solid rgba(151, 151, 151, 0.3)';
        style['zIndex'] = 2;
    }

    return (
        <Item
            ref={setNodeRef}
            style={style}
            {...attributes}
            {...listeners}
            idx={idx}
            answer={answer}
        />
    );
};

type ListRankQuestionProps = Pick<QuestionProps, 'answerKey' | 'answered' | 'setAnswered'>;

const ListRankQuestion = (props: ListRankQuestionProps) => {
    const { answerKey, answered, setAnswered } = props;
    const [, updatedAnswer, setAnswer, saveAnswer] = useQuestion<string[]>(answerKey, [], false);
    const [activeId, setActiveId] = useState(null);
    const keyboardCoordinatesGetter: KeyboardCoordinateGetter = (event, { currentCoordinates }) => {
        const delta = 74;
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

    useEffect(() => {
        if (answered) {
            saveAnswer();
        }
    }, [answered, saveAnswer]);

    const handleDragStart = ({ active }: DragStartEvent) => setActiveId(active.id);

    const handleDragEnd = ({ active, over }: DragEndEvent) => {
        if (active.id !== over.id) {
            const oldIndex = updatedAnswer.indexOf(active.id);
            const newIndex = updatedAnswer.indexOf(over.id);
            setAnswered && setAnswered(false);
            setAnswer(arrayMove(updatedAnswer, oldIndex, newIndex));
        }
        setActiveId(null);
    };

    return (
        <DndContext
            sensors={sensors}
            collisionDetection={closestCenter}
            onDragStart={handleDragStart}
            onDragEnd={handleDragEnd}
            modifiers={[restrictToVerticalAxis, restrictToParentElement]}
        >
            <SortableContext items={updatedAnswer} strategy={verticalListSortingStrategy}>
                {updatedAnswer.map((answer, idx) => (
                    <SortableItem
                        key={answer}
                        id={answer}
                        idx={idx}
                        answer={answer}
                        active={activeId === answer}
                    />
                ))}
            </SortableContext>
        </DndContext>
    );
};

export { ListRankQuestion };
export default ListRankQuestion;
