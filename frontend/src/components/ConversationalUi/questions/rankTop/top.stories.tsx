import { action } from '@storybook/addon-actions';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import RankTop from '.';

export default {
    title: 'ConversationalUi/RankTop',
    component: RankTop,
    argTypes: {},
} as ComponentMeta<typeof RankTop>;

const Template: ComponentStory<typeof RankTop> = (args) => {
    const setAnswered = action('setAnswered');
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
                width: '100%',
            }}
        >
            <RankTop
                setAnswered={setAnswered}
                answered={false}
                answerKey="copingTop"
                lists={[
                    'copingBody',
                    'copingDistract',
                    'copingHelpOthers',
                    'copingCourage',
                    'copingSenses',
                    'supportivePeople',
                ]}
                dropTitle="Coping Strategies"
                targetCount={7}
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
                copingBody: ['Cold shower', 'Hot bath'],
                copingHelpOthers: ['Do something kind', 'Give a compliment', 'Offer encouragement'],
                copingCourage: ['Encourage myself'],
                copingSenses: [
                    'Eat a favorite food',
                    'Use scented soap or lotion',
                    'Light a candle',
                ],
                supportivePeople: [
                    {
                        name: 'Jane Doe',
                        phone: '555-555-5555',
                    },
                ],
            },
        },
    },
};
