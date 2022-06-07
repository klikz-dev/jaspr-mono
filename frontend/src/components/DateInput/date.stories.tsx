import { ComponentStory, ComponentMeta } from '@storybook/react';
import DateInput from '.';

export default {
    title: 'Components/DateInput',
    component: DateInput,
} as ComponentMeta<typeof DateInput>;

const Template: ComponentStory<typeof DateInput> = (args) => {
    return <DateInput {...args} />;
};

export const IeFallback = Template.bind({});
