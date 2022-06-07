import { action } from '@storybook/addon-actions';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import ConfirmLogoutModal from './';

export default {
    title: 'Components/ConfirmLogoutModal',
    component: ConfirmLogoutModal,
} as ComponentMeta<typeof ConfirmLogoutModal>;

const Template: ComponentStory<typeof ConfirmLogoutModal> = (args) => {
    return <ConfirmLogoutModal {...args} />;
};

export const Confirm = Template.bind({});
Confirm.args = {
    confirmLogoutOpen: true,
    logout: action('Logout'),
    goBack: action('Go Back'),
};
