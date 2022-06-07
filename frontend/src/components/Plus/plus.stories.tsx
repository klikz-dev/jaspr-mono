import { ComponentStory, ComponentMeta } from '@storybook/react';
import Plus from '.';

export default {
    title: 'Components/Plus',
    component: Plus,
} as ComponentMeta<typeof Plus>;

const Template: ComponentStory<typeof Plus> = (args) => {
    return <Plus {...args} />;
};

export const Small = Template.bind({});
Small.args = {
    size: 15,
};

export const Large = Template.bind({});
Large.args = {
    size: 30,
};
