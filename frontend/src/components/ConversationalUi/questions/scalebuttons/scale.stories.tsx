import { action } from '@storybook/addon-actions';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import ScaleButtons from '.';

export default {
    title: 'ConversationalUi/ScaleButtons',
    component: ScaleButtons,
    argTypes: {},
} as ComponentMeta<typeof ScaleButtons>;

const Template: ComponentStory<typeof ScaleButtons> = (args) => {
    const setAnswered = action('setAnswered');
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
                width: '100%',
            }}
        >
            <ScaleButtons
                setAnswered={setAnswered}
                answered={false}
                min={0}
                max={10}
                minLabel="Low Distress"
                maxLabel="High Distress"
                answerKey="distress0"
            />
        </div>
    );
};

export const Default = Template.bind({});
