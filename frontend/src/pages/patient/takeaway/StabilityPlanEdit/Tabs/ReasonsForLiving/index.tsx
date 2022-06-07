import React, { useState, forwardRef, CSSProperties } from 'react';
import {
    DndContext,
    closestCenter,
    KeyboardSensor,
    PointerSensor,
    useSensor,
    useSensors,
    KeyboardCoordinateGetter,
    DraggableAttributes,
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
import Section from '../../Components/Section';
import styles from './index.module.scss';
import hamburger from 'assets/greyHamburger.png';
import { AssessmentAnswers } from 'state/types';
import Chevron from 'assets/icons/Chevron';
import { SyntheticListenerMap } from '@dnd-kit/core/dist/hooks/utilities';

const ITEM_COUNT = 5;

interface SortableElementProp {
    id: string;
    idx?: number;
    reasonsLive?: string[];
    setAnswers?: (
        answers: AssessmentAnswers | ((answers: AssessmentAnswers) => AssessmentAnswers),
    ) => void;
    reason?: string;
    style?: CSSProperties;
    listeners: SyntheticListenerMap;
    attributes: DraggableAttributes;
}

const Item = forwardRef<HTMLDivElement, SortableElementProp>(
    ({ idx, reason, reasonsLive, setAnswers, listeners, attributes, ...props }, ref) => {
        const onChange = ({ target }: React.ChangeEvent<HTMLInputElement>) => {
            setAnswers((answers) => {
                const updatedReasons = [...reasonsLive];
                updatedReasons[idx] = target.value;
                return { ...answers, reasonsLive: updatedReasons };
            });
        };
        const moveReasons = ({ newIndex, oldIndex }: { newIndex: number; oldIndex: number }) => {
            const newReasonsLive = [...reasonsLive];
            newReasonsLive.splice(newIndex, 0, newReasonsLive.splice(oldIndex, 1)[0]);
            setAnswers((answers) => ({ ...answers, reasonsLive: newReasonsLive }));
        };
        return (
            <div className={styles.rankItem} {...props} ref={ref}>
                <img
                    alt=""
                    className={styles.handle}
                    src={hamburger}
                    {...attributes}
                    {...listeners}
                />
                <div className={styles.index}>{idx + 1}</div>
                <input className={styles.reason} value={reason} onChange={onChange} />
                <div
                    onClick={() => {
                        if (idx > 0) {
                            moveReasons({ oldIndex: idx, newIndex: idx - 1 });
                        }
                    }}
                >
                    <Chevron
                        direction="up"
                        color={idx === 0 ? 'rgba(73, 77, 87, 0.25)' : 'rgba(73, 77, 87, 1)'}
                    />
                </div>
                <div
                    onClick={() => {
                        if (reasonsLive && idx < reasonsLive.length - 1) {
                            moveReasons({ oldIndex: idx, newIndex: idx + 1 });
                        }
                    }}
                >
                    <Chevron
                        direction="down"
                        color={
                            idx === reasonsLive?.length - 1
                                ? 'rgba(73, 77, 87, 0.25)'
                                : 'rgba(73, 77, 87, 1)'
                        }
                    />
                </div>
            </div>
        );
    },
);

const SortableItem = ({
    reason,
    id,
    idx,
    reasonsLive,
    setAnswers,
    active,
}: {
    reason: string;
    id: string;
    idx: number;
    reasonsLive: string[];
    setAnswers: (
        answers: AssessmentAnswers | ((answers: AssessmentAnswers) => AssessmentAnswers),
    ) => void;
    active: boolean;
}) => {
    const { attributes, listeners, setNodeRef, transform, transition } = useSortable({
        id,
    });
    if (transform) {
        console.log(transform);
    }

    const style: CSSProperties = {
        transform: CSS.Transform.toString(transform),
        transition,
        touchAction: 'none',
    };

    if (active) {
        style['zIndex'] = 2;
    }

    return (
        <Item
            ref={setNodeRef}
            style={style}
            attributes={attributes}
            listeners={listeners}
            id={id}
            idx={idx}
            reason={reason}
            reasonsLive={reasonsLive}
            setAnswers={setAnswers}
        />
    );
};

interface SupportivePeopleTabProps {
    setAnswers: (
        answers:
            | Partial<AssessmentAnswers>
            | ((answers: Partial<AssessmentAnswers>) => Partial<AssessmentAnswers>),
    ) => void;
    answers: Partial<AssessmentAnswers>;
}

const SupportivePeopleTab = ({ answers, setAnswers }: SupportivePeopleTabProps) => {
    const { reasonsLive = [] } = answers;
    const sortableReasons = [
        ...(reasonsLive || []),
        ...Array(ITEM_COUNT - (reasonsLive || []).length).fill(''),
    ];

    const [activeId, setActiveId] = useState(null);

    const keyboardCoordinatesGetter: KeyboardCoordinateGetter = (event, { currentCoordinates }) => {
        const delta = 45;
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
            const oldIndex = parseInt(active.id, 10);
            const newIndex = parseInt(over.id, 10);
            setAnswers({ ...answers, reasonsLive: arrayMove(sortableReasons, oldIndex, newIndex) });
        }
        setActiveId(null);
    };

    return (
        <Section
            number="3"
            title="My Reasons for Living"
            tooltip="What are some reasons you would not kill yourself? You can drag them to rank by importance."
        >
            <div className={styles.container}>
                <div className={styles.label}>MOST IMPORTANT</div>

                <DndContext
                    sensors={sensors}
                    collisionDetection={closestCenter}
                    onDragStart={handleDragStart}
                    onDragEnd={handleDragEnd}
                    modifiers={[restrictToVerticalAxis, restrictToParentElement]}
                >
                    <SortableContext
                        items={[...Array(ITEM_COUNT)].map((_, idx) => idx.toString())}
                        strategy={verticalListSortingStrategy}
                    >
                        <div className={styles.ranker}>
                            {sortableReasons.map((reason, idx) => (
                                <SortableItem
                                    key={idx}
                                    id={idx.toString()}
                                    idx={idx}
                                    reason={reason}
                                    reasonsLive={reasonsLive || []}
                                    setAnswers={setAnswers}
                                    active={activeId === idx.toString()}
                                />
                            ))}
                        </div>
                    </SortableContext>
                </DndContext>

                <div className={styles.label}>LEAST IMPORTANT</div>
            </div>
        </Section>
    );
};

export default SupportivePeopleTab;
