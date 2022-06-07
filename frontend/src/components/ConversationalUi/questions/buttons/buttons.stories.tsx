import { action } from '@storybook/addon-actions';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import Buttons from '.';

export default {
    title: 'ConversationalUi/Buttons',
    component: Buttons,
    argTypes: {},
} as ComponentMeta<typeof Buttons>;

const Template: ComponentStory<typeof Buttons> = (args) => {
    const setAnswered = action('answered');
    const next = action('next');
    const setShowValidation = action('setShowValidation');
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
            }}
        >
            <Buttons
                {...args}
                setShowValidation={setShowValidation}
                setAnswered={setAnswered}
                next={next}
            />
        </div>
    );
};

export const Vertical = Template.bind({});
Vertical.args = {
    buttons: [{ label: 'Button 1' }, { label: 'Button2' }, { label: 'Button3' }],
};

export const Horizontal = Template.bind({});
Horizontal.args = {
    orientation: 'horizontal',
    buttons: [{ label: 'Button 1' }, { label: 'Button2' }, { label: 'Button3' }],
};
