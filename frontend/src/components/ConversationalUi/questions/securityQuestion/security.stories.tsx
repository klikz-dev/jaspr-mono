import { action } from '@storybook/addon-actions';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import SecurityQuestion from '.';

export default {
    title: 'ConversationalUi/SecurityQuestion',
    component: SecurityQuestion,
    argTypes: {},
} as ComponentMeta<typeof SecurityQuestion>;

const Template: ComponentStory<typeof SecurityQuestion> = (args) => {
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
                width: '100%',
            }}
        >
            <SecurityQuestion
                currentQuestion={true}
                {...args}
                setShowValidation={(value: boolean) => action('set show valid')}
                setIsValid={() => action('set valid')}
                // @ts-ignore
                validate={{ current: action('validating') }}
            />
        </div>
    );
};

export const Default = Template.bind({});
Default.parameters = {
    initialState: {
        user: {
            privacyImages: [
                { id: 4, url: 'https://media.jaspr-development.com/Dog3x_1.png' },
                { id: 6, url: 'https://media.jaspr-development.com/Grass3x_1.png' },
                { id: 8, url: 'https://media.jaspr-development.com/Pineapple3x_1.png' },
            ],
            securityQuestion: { question: 'Where were you born?' },
        },
    },
};
