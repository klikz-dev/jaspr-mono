import { ComponentStory, ComponentMeta } from '@storybook/react';
import CrossedPlus from '.';

export default {
    title: 'Components/CrossedPlus',
    component: CrossedPlus,
} as ComponentMeta<typeof CrossedPlus>;

const Template: ComponentStory<typeof CrossedPlus> = (args) => {
    return <CrossedPlus {...args} />;
};

export const Small = Template.bind({});
Small.args = {
    size: 15,
};

export const Large = Template.bind({});
Large.args = {
    size: 30,
};
