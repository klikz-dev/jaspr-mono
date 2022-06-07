import { ComponentStory, ComponentMeta } from '@storybook/react';
import Message from '.';

export default {
    title: 'ConversationalUi/Message',
    component: Message,
    argTypes: {},
} as ComponentMeta<typeof Message>;

const Template: ComponentStory<typeof Message> = (args) => {
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
            }}
        >
            <Message {...args} />
        </div>
    );
};

export const Default = Template.bind({});
Default.args = {
    message: 'This is the message',
};
