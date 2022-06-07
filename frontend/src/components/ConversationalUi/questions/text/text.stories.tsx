import { action } from '@storybook/addon-actions';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import Text from '.';

export default {
    title: 'ConversationalUi/Text',
    component: Text,
    argTypes: {},
} as ComponentMeta<typeof Text>;

const Template: ComponentStory<typeof Text> = (args) => {
    const setAnswered = action('setAnswered');
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
                width: '100%',
            }}
        >
            <Text
                label="My text input"
                maxLength={10000}
                setAnswered={setAnswered}
                answered={false}
            />
        </div>
    );
};

export const Default = Template.bind({});
