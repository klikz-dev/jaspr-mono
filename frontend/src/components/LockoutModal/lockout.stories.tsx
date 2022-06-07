import { ComponentStory, ComponentMeta } from '@storybook/react';
import LockoutModal from '.';

export default {
    title: 'Components/LockoutModal',
    component: LockoutModal,
} as ComponentMeta<typeof LockoutModal>;

const Template: ComponentStory<typeof LockoutModal> = (args) => {
    return <LockoutModal {...args} />;
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
