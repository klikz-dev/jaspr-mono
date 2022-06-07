import { ComponentStory, ComponentMeta } from '@storybook/react';
import Progress from '.';

export default {
    title: 'Components/Progress',
    component: Progress,
} as ComponentMeta<typeof Progress>;

const Template: ComponentStory<typeof Progress> = (args) => {
    return <Progress {...args} />;
};

export const Zero = Template.bind({});
Zero.args = {
    progress: 0,
};

export const One = Template.bind({});
One.args = {
    progress: 1,
};

export const Two = Template.bind({});
Two.args = {
    progress: 2,
};

export const Three = Template.bind({});
Three.args = {
    progress: 3,
};
