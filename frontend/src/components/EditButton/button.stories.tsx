import { action } from '@storybook/addon-actions';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import EditButton from '.';

export default {
    title: 'Components/EditButton',
    component: EditButton,
} as ComponentMeta<typeof EditButton>;

const Template: ComponentStory<typeof EditButton> = (args) => {
    return <EditButton {...args} onClick={action('Clicked')} />;
};

export const Default = Template.bind({});
