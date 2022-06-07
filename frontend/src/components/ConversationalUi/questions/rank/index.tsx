import { forwardRef, useEffect, useContext, useState, CSSProperties } from 'react';
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
import { useSortable, SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { restrictToParentElement, restrictToVerticalAxis } from '@dnd-kit/modifiers';
import { CSS } from '@dnd-kit/utilities';
import template from 'lodash/template';
import StoreContext from 'state/context/store';
import { useQuestion } from 'components/ConversationalUi/hooks/useQuestion';
import styles from './rank.module.scss';
import hamburger from 'assets/greyHamburger.png';
import { AssessmentAnswers } from 'state/types';
import { QuestionProps } from 'components/ConversationalUi/question';

interface RankOption {
    question: string;
    answerKey: string;
    title: string;
    subtitle: string;
}

const Item = forwardRef<
    HTMLDivElement,
    {
        id: string;
        idx: number;
        style: CSSProperties;
        question: RankOption;
        answers: AssessmentAnswers;
    }
>(({ idx, style, question, answers, ...props }, ref) => {
    let subtitle = '[-]';
    let title = '[-]';

    if (Object.keys(answers).length > 0) {
        try {
            const templateExecutor = template(question.subtitle);
            subtitle = templateExecutor({ ...answers });
        } catch (err) {
            // Catches errors when the variable is missing or unset, which is
            // expected
        }
        try {
            const templateExecutor = template(question.title);
            title = templateExecutor({ ...answers });
        } catch (err) {
            // Catches errors when the variable is missing or unset, which is
            // expected
        }
    }

    return (
        <div className={styles.rankItem} style={style} ref={ref} {...props}>
            <div className={styles.index}>{idx + 1}</div>
            <div className={styles.labels}>
                {title} <br />
                {subtitle}
            </div>
            <img alt="" src={hamburger} style={{ width: '12px', marginRight: '15px' }} />
        </div>
    );
});

const SortableItem = ({
    id,
    idx,
    question,
    answers,
    active,
}: {
    id: string;
    idx: number;
    active: boolean;
    question: RankOption;
    answers: AssessmentAnswers;
}) => {
    const { attributes, listeners, setNodeRef, transform, transition } = useSortable({
        id: question.answerKey,
    });
    const style: CSSProperties = {
        transform: CSS.Transform.toString(transform),
        transition,
        touchAction: 'none',
    };

    if (active) {
        style['zIndex'] = 2;
        style['borderBottom'] = '1px solid rgba(151, 151, 151, 0.3)';
    }

    return (
        <Item
            ref={setNodeRef}
            style={style}
            answers={answers}
            question={question}
            {...attributes}
            {...listeners}
            id={id}
            idx={idx}
        />
    );
};

type RankQuestionProps = Pick<QuestionProps, 'answerKey' | 'setAnswered' | 'answered'> & {
    options: RankOption[];
    minLabel: string;
    maxLabel: string;
};

const Rank = ({
    setAnswered,
    answerKey,
    answered,
    options,
    minLabel = 'Least Important',
    maxLabel = 'Most Important',
}: RankQuestionProps) => {
    const [store] = useContext(StoreContext);
    const { assessment } = store;
    const { answers } = assessment;
    const [, updatedAnswer, setAnswer, saveAnswer] = useQuestion<string | null>(
        answerKey,
        null,
        false,
    );
    const [questionOrder, setQuestionOrder] = useState(
        [...Array(options.length + 1).keys()].slice(1),
    );

    const questions = questionOrder.map((idx) => {
        return options[idx - 1];
    });

    const [activeId, setActiveId] = useState(null);

    const keyboardCoordinatesGetter: KeyboardCoordinateGetter = (event, { currentCoordinates }) => {
        const delta = 76;
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
            const oldIndex = questions.findIndex((question) => question.answerKey === active.id);
            const newIndex = questions.findIndex((question) => question.answerKey === over.id);
            let questionOrder = [...Array(options.length + 1).keys()].slice(1);

            if (updatedAnswer) {
                questionOrder = updatedAnswer.split(',').map((i) => parseInt(i, 10));
            }

            if (newIndex > questionOrder.length - 1 || newIndex < 0) return;
            const newAnswers = [...questionOrder];
            if (newIndex >= newAnswers.length) {
                var k = newIndex - newAnswers.length + 1;
                while (k--) {
                    newAnswers.push(undefined);
                }
            }
            newAnswers.splice(newIndex, 0, newAnswers.splice(oldIndex, 1)[0]);
            if (answerKey && newAnswers.join(',') !== updatedAnswer) {
                setAnswered && setAnswered(false);
                setAnswer(newAnswers.join(','));
            }
        }
        setActiveId(null);
    };

    useEffect(() => {
        if (answerKey && updatedAnswer) {
            const updatedOrder = updatedAnswer.split(',').map((i) => parseInt(i, 10));
            if (questionOrder.join(',') !== updatedOrder.join(',')) {
                setQuestionOrder(updatedOrder);
            }
        } else if (answerKey && updatedAnswer === null) {
            // Initialize a default for the ordering (if it's not present already).
            const answer = [...questionOrder].join(',');
            if (answer !== updatedAnswer) {
                setAnswer(answer);
                setAnswered(false);
            }
        }
    }, [answerKey, questionOrder, setAnswer, setAnswered, updatedAnswer]);

    useEffect(() => {
        if (answered) {
            saveAnswer();
        }
    }, [answered, saveAnswer]);

    return (
        <DndContext
            sensors={sensors}
            collisionDetection={closestCenter}
            onDragStart={handleDragStart}
            onDragEnd={handleDragEnd}
            modifiers={[restrictToVerticalAxis, restrictToParentElement]}
        >
            <div className={styles.mostImportant}>{maxLabel}</div>
            <SortableContext
                items={questions.map((question) => question.answerKey)}
                strategy={verticalListSortingStrategy}
            >
                <div className={styles.ranker}>
                    {questions.map((question, idx) => (
                        <SortableItem
                            id={question.answerKey}
                            key={`item-${idx}`}
                            idx={idx}
                            answers={answers}
                            active={activeId === question.answerKey}
                            question={question}
                        />
                    ))}
                </div>
            </SortableContext>
            <div className={styles.leastImportant}>{minLabel}</div>
        </DndContext>
    );
};

export { Rank };
export default Rank;
