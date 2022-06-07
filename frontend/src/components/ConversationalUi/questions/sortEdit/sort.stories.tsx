import { action } from '@storybook/addon-actions';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import SortEdit from '.';

export default {
    title: 'ConversationalUi/SortEdit',
    component: SortEdit,
    argTypes: {},
} as ComponentMeta<typeof SortEdit>;

const Template: ComponentStory<typeof SortEdit> = (args) => {
    const setAnswered = action('setAnswered');
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
                width: '100%',
            }}
        >
            <SortEdit answered={false} setAnswered={setAnswered} />
        </div>
    );
};

export const Default = Template.bind({});
