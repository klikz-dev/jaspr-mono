import { action } from '@storybook/addon-actions';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import MeansCustom from '.';

export default {
    title: 'ConversationalUi/MeansCustom',
    component: MeansCustom,
    argTypes: {},
} as ComponentMeta<typeof MeansCustom>;

const Template: ComponentStory<typeof MeansCustom> = (args) => {
    const setAnswered = action('setAnswered');

    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
            }}
        >
            <MeansCustom
                {...args}
                setAnswered={setAnswered}
                answerKey="strategiesCustom"
                reviewKeys={[
                    { answerKey: 'strategiesGeneral', label: 'General' },
                    { answerKey: 'strategiesFirearm', label: 'Firearm' },
                    { answerKey: 'strategiesMedicine', label: 'Medicine' },
                    { answerKey: 'strategiesPlaces', label: 'Dangerous Places' },
                    { answerKey: 'strategiesOther', label: 'Other Hazards' },
                ]}
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
                strategiesGeneral: ['Dispose of method'],
                strategiesFirearm: ['Gun dealers', 'Pawn shop'],
                strategiesMedicine: ['Stored with a trusted person'],
                strategiesPlaces: ['Limit access when and where it is possible'],
                strategiesOther: [],
            },
        },
    },
};
