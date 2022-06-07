import { action } from '@storybook/addon-actions';
import { useState } from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import Select from '.';

export default {
    title: 'Components/Select',
    component: Select,
} as ComponentMeta<typeof Select>;

const Template: ComponentStory<typeof Select> = (args) => {
    const [value, setValue] = useState();
    const onChange = (value: any) => {
        setValue(value);
        action('change');
    };
    return <Select {...args} value={value} onChange={onChange} />;
};

export const Light = Template.bind({});
Light.args = {
    placeholder: 'Choose an option...',
    mode: 'light',
    options: [
        { value: 1, label: 'Option 1' },
        { value: 2, label: 'Option 2' },
        { value: 3, label: 'Option 3' },
        { value: 4, label: 'Option 4' },
    ],
};

export const Dark = Template.bind({});
Dark.args = {
    placeholder: 'Choose an option...',
    mode: 'dark',
    options: [
        { value: 1, label: 'Option 1' },
        { value: 2, label: 'Option 2' },
        { value: 3, label: 'Option 3' },
        { value: 4, label: 'Option 4' },
    ],
};
