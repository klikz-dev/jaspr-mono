import { action } from '@storybook/addon-actions';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import LockoutHelpModal from '.';

export default {
    title: 'Components/LockoutHelpModal',
    component: LockoutHelpModal,
} as ComponentMeta<typeof LockoutHelpModal>;

const Template: ComponentStory<typeof LockoutHelpModal> = (args) => {
    return <LockoutHelpModal {...args} goBack={action('Clicked Back')} />;
};

export const Default = Template.bind({});
