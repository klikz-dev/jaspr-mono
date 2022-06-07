import { action } from '@storybook/addon-actions';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import SecurityImage from '.';

export default {
    title: 'ConversationalUi/SecurityImage',
    component: SecurityImage,
    argTypes: {},
} as ComponentMeta<typeof SecurityImage>;

const Template: ComponentStory<typeof SecurityImage> = (args) => {
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
            }}
        >
            <SecurityImage
                currentQuestion={true}
                {...args}
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
