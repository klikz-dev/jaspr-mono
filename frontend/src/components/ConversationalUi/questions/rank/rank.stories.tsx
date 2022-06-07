/* eslint no-template-curly-in-string: 0 */
import { action } from '@storybook/addon-actions';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import Rank from '.';

export default {
    title: 'ConversationalUi/Rank',
    component: Rank,
    argTypes: {},
} as ComponentMeta<typeof Rank>;

const Template: ComponentStory<typeof Rank> = (args) => {
    const setAnswered = action('setAnswered');
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
                width: '100%',
            }}
        >
            <Rank
                answerKey="rankFeelings"
                setAnswered={setAnswered}
                answered={false}
                options={[
                    {
                        //@ts-ignore
                        question: 'Psychological pain',
                        answerKey: 'ratePsych|mostPainful',
                        //@ts-ignore
                        title: "PSYCHOLOGICAL PAIN: ${ratePsych || '[-]'} out of 5",
                        //@ts-ignore
                        subtitle: "What I find most painful is ${mostPainful || '[-]'}",
                    },
                    {
                        //@ts-ignore
                        question: 'Stress',
                        answerKey: 'rateStress|mostStress',
                        title: "STRESS: ${rateStress || '[-]'} out of 5",
                        subtitle: "What I find most stressful is ${mostStress || '[-]'}",
                    },
                    {
                        //@ts-ignore
                        question: 'Agitation',
                        answerKey: 'rateAgitation|causesAgitation',
                        title: "AGITATION: ${rateAgitation || '[-]'} out of 5",
                        subtitle: "I most need to take action when ${causesAgitation || '[-]'}",
                    },
                    {
                        //@ts-ignore
                        question: 'Hopelessness',
                        answerKey: 'rateHopeless|mostHopeless',
                        title: "HOPELESSNESS: ${rateHopeless || '[-]'} out of 5",
                        subtitle: "I feel most hopeless when ${mostHopeless || '[-]'}",
                    },
                    {
                        //@ts-ignore
                        question: 'Self-hate',
                        answerKey: 'rateSelfHate|mostHate',
                        title: "SELF-HATE: ${rateSelfHate || '[-]'} out of 5",
                        subtitle: "What I hate most about myself is ${mostHate || '[-]'}",
                    },
                ]}
                minLabel="LEAST IMPORTANT"
                maxLabel="MOST IMPORTANT"
            />
        </div>
    );
};

export const Default = Template.bind({});
Default.parameters = {
    initialState: {
        ...Default.parameters,
        assessment: {
            answers: {
                ratePsych: 1,
                mostHate: 'I hate everything',
                rateStress: 4,
                mostStress: "I can't handle my job",
                rateAgitation: 5,
                rateHopeless: 2,
                mostHopeless: "I don't think I can fix it",
                rateSelfHate: 4,
            },
        },
    },
};
