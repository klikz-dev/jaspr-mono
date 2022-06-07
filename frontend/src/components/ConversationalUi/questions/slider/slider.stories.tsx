import { action } from '@storybook/addon-actions';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import Slider from '.';

export default {
    title: 'ConversationalUi/Slider',
    component: Slider,
    argTypes: {},
} as ComponentMeta<typeof Slider>;

const Template: ComponentStory<typeof Slider> = (args) => {
    const setAnswered = action('setAnswered');
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
                width: '100%',
            }}
        >
            <Slider
                answered={false}
                setAnswered={setAnswered}
                minLabel="Not at all confident"
                maxLabel="Very confident"
                min={0}
                max={100}
                step={1}
                answerKey="stabilityConfidence"
            />
        </div>
    );
};

export const Default = Template.bind({});
