import { action } from '@storybook/addon-actions';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import JahSignup from '.';

export default {
    title: 'ConversationalUi/JahSignup',
    component: JahSignup,
    argTypes: {},
} as ComponentMeta<typeof JahSignup>;

const Template: ComponentStory<typeof JahSignup> = (args) => {
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
            }}
        >
            <JahSignup {...args} close={action('Close')} />
        </div>
    );
};

export const Default = Template.bind({});
