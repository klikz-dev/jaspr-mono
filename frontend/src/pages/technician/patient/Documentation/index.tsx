import { useState } from 'react';
import { NavLink, useRouteMatch } from 'lib/router';
import styles from './index.module.scss';
import ButtonsQuestion from './Questions/Buttons';
import QuestionChoice from './Questions/ChoiceButtons';
import QuestionRank from './Questions/Rank';
import QuestionScaleButtons from './Questions/ScaleButtons';
import QuestionText from './Questions/Text';
import QuestionList from './Questions/List';
import ProviderNotes from './ProviderNotes';
import SupportivePeople from './Questions/SupportivePeople';
import RankTop from './Questions/RankTop';
import Slider from './Questions/Slider';
import Counter from './Questions/Counter';
import TabChoice from './Questions/TabChoice';
import Sentry from 'lib/sentry';
import { PatientData, Preferences } from 'state/types';
import { GetResponse as ProviderCommentsGetResponse } from 'state/types/api/technician/encounter/_id/provider-comments';
import { Question } from 'components/ConversationalUi/questions';

interface DocumentationProps {
    patientData: PatientData;
    providerComments?: ProviderCommentsGetResponse;
    setProviderComments?: (providerComments: ProviderCommentsGetResponse) => void;
    currentEncounter: number;
    preferences: Preferences;
}

const Documentation = ({
    patientData,
    providerComments,
    setProviderComments,
    currentEncounter,
    preferences,
}: DocumentationProps) => {
    const match = useRouteMatch<{ patientId: string }>();
    const [sectionIndex, setSectionIndex] = useState(0);
    const patientId = parseInt(match.params.patientId, 10);
    const { questions } = patientData ?? {};

    const answers = patientData?.answers.answers;

    const sections = questions
        ?.filter((question) => question.providerOrder !== undefined)
        .sort((a, b) => a.providerOrder - b.providerOrder)
        .reduce((sections, question) => {
            const isSectionBoundary = question.actions.some(
                (action) => action.type === 'section-change',
            );
            if (isSectionBoundary) {
                sections.push({ label: question.providerLabel, questions: [] });
            } else {
                sections[sections.length - 1]?.questions.push(question);
            }
            return sections;
        }, [])
        .filter((section) => section.questions.length);

    return (
        <div className={styles.documentation}>
            <aside className={styles.sectionLinks}>
                {sections?.map((section, idx) => (
                    <NavLink
                        to={`/technician/patients/${patientId}/documentation/notes`}
                        onClick={(e) => {
                            e.preventDefault();
                            setSectionIndex(idx);
                        }}
                        activeClassName={styles.active}
                        className={styles.sectionLink}
                        key={section.label}
                        isActive={() => idx === sectionIndex}
                    >
                        <span>{section.label}</span>
                    </NavLink>
                ))}
            </aside>
            <section style={{ display: 'block', backgroundColor: 'white', overflowY: 'auto' }}>
                {sections?.[sectionIndex]?.questions.map((question: Question) => (
                    <div
                        className={styles.question}
                        key={question.uid}
                        style={
                            question.actions.some((action) => action.type === 'list')
                                ? {
                                      flexDirection: 'row',
                                      display: 'flex',
                                      flexWrap: 'wrap',
                                      flexBasis: '50%',
                                  }
                                : { flexDirection: 'column' }
                        }
                    >
                        {question.actions
                            .filter(
                                (action) =>
                                    ('answerKey' in action && action.answerKey) ||
                                    ('groups' in action &&
                                        action.groups?.some((group) => group.answerKey)),
                            )
                            ?.map((action, idx) => {
                                switch (action.type) {
                                    case 'rank':
                                        return (
                                            <QuestionRank
                                                key={
                                                    // @ts-ignore
                                                    action.answerKey ||
                                                    // @ts-ignore
                                                    action.groups.find((group) => group.answerKey)
                                                        ?.answerKey
                                                }
                                                action={action}
                                                assessment={answers}
                                                providerComments={providerComments}
                                                setProviderComments={setProviderComments}
                                                currentEncounter={currentEncounter}
                                                preferences={preferences}
                                            />
                                        );
                                    case 'scalebuttons':
                                        return (
                                            <QuestionScaleButtons
                                                key={action.answerKey}
                                                action={action}
                                                question={question}
                                                assessment={answers}
                                                providerComments={providerComments}
                                                setProviderComments={setProviderComments}
                                                currentEncounter={currentEncounter}
                                                preferences={preferences}
                                            />
                                        );
                                    case 'text':
                                        return (
                                            <QuestionText
                                                key={action.answerKey}
                                                actionIndex={idx}
                                                action={action}
                                                question={question}
                                                assessment={answers}
                                                providerComments={providerComments}
                                                setProviderComments={setProviderComments}
                                                currentEncounter={currentEncounter}
                                                preferences={preferences}
                                            />
                                        );
                                    case 'list':
                                        return (
                                            <QuestionList
                                                key={action.answerKey}
                                                action={action}
                                                assessment={answers}
                                            />
                                        );
                                    case 'buttons':
                                        return (
                                            <ButtonsQuestion
                                                key={action.answerKey}
                                                // @ts-ignore TODO Need guard that only actions with answerKeys
                                                action={action}
                                                question={question}
                                                assessment={answers}
                                            />
                                        );
                                    case 'choice':
                                        return (
                                            <QuestionChoice
                                                key={`idx-${action.options
                                                    .map((option) => option.label)
                                                    .join('-')}`}
                                                // @ts-ignore
                                                action={action}
                                                question={question}
                                                assessment={answers}
                                            />
                                        );
                                    case 'supportive-people':
                                        return (
                                            <SupportivePeople
                                                key={`${idx}-supportive-people`}
                                                action={action}
                                                assessment={answers}
                                                providerComments={providerComments}
                                                setProviderComments={setProviderComments}
                                                currentEncounter={currentEncounter}
                                                preferences={preferences}
                                            />
                                        );
                                    case 'rank-top':
                                        return (
                                            <RankTop
                                                key={action.answerKey}
                                                action={action}
                                                question={question}
                                                assessment={answers}
                                                providerComments={providerComments}
                                                setProviderComments={setProviderComments}
                                                currentEncounter={currentEncounter}
                                                preferences={preferences}
                                            />
                                        );
                                    case 'slider':
                                        return (
                                            <Slider
                                                key={action.answerKey}
                                                action={action}
                                                question={question}
                                                assessment={answers}
                                                providerComments={providerComments}
                                                setProviderComments={setProviderComments}
                                                currentEncounter={currentEncounter}
                                                preferences={preferences}
                                            />
                                        );
                                    case 'counter':
                                        return (
                                            <Counter
                                                key={action.answerKey}
                                                action={action}
                                                question={question}
                                                assessment={answers}
                                                providerComments={providerComments}
                                                setProviderComments={setProviderComments}
                                                currentEncounter={currentEncounter}
                                                preferences={preferences}
                                            />
                                        );
                                    case 'tab-choice':
                                        return (
                                            <TabChoice
                                                key={action.groups?.[0]?.answerKey}
                                                action={action}
                                                question={question}
                                                assessment={answers}
                                                providerComments={providerComments}
                                                setProviderComments={setProviderComments}
                                                currentEncounter={currentEncounter}
                                                preferences={preferences}
                                            />
                                        );
                                }

                                Sentry.captureException(
                                    `Provider Notes can't render question action of type ${action.type} for question ${question.uid}}`,
                                );
                                return null;
                            })}
                        {question.actions.some((action) => action.type === 'list') && (
                            <div
                                style={{
                                    display: 'grid',
                                    flexBasis: '100%',
                                    gridTemplateColumns: '0.25fr 4fr',
                                }}
                            >
                                <ProviderNotes
                                    providerComments={providerComments}
                                    setProviderComments={setProviderComments}
                                    currentEncounter={currentEncounter}
                                    enabled={preferences.providerNotes}
                                    answerKey={
                                        // prettier-ignore
                                        // @ts-ignore
                                        question.actions.find((action) => 'answerKey' in action)?.answerKey
                                    }
                                />
                            </div>
                        )}
                    </div>
                ))}
            </section>
        </div>
    );
};

export default Documentation;
