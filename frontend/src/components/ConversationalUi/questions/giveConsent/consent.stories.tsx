import { action } from '@storybook/addon-actions';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import GiveConsent from '.';

export default {
    title: 'ConversationalUi/GiveConsent',
    component: GiveConsent,
    argTypes: {},
} as ComponentMeta<typeof GiveConsent>;

const Template: ComponentStory<typeof GiveConsent> = (args) => {
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
            }}
        >
            <GiveConsent {...args} />
        </div>
    );
};

export const Default = Template.bind({});
Default.args = {
    answerKey: 'giveConsent',
    options: [
        {
            label: 'Yes',
            sublable: 'Save my entries so I can access them later.',
            value: true,
        },
        { label: 'No', sublable: '', value: false },
    ],
    next: action('Next'),
};
