import { action } from '@storybook/addon-actions';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import SupportivePerson from '.';

export default {
    title: 'ConversationalUi/SupportivePerson',
    component: SupportivePerson,
    argTypes: {},
} as ComponentMeta<typeof SupportivePerson>;

const Template: ComponentStory<typeof SupportivePerson> = (args) => {
    const setAnswered = action('setAnswered');
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
                width: '100%',
            }}
        >
            <SupportivePerson setAnswered={setAnswered} answered={false} />
        </div>
    );
};

export const Default = Template.bind({});
