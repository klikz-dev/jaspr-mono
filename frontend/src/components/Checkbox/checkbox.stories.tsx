import { useState } from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import { Checkbox } from './';

export default {
    title: 'Components/Checkbox',
    component: Checkbox,
} as ComponentMeta<typeof Checkbox>;

const Template: ComponentStory<typeof Checkbox> = (args) => {
    const [checked, setChecked] = useState(args.checked);
    return <Checkbox {...args} checked={checked} onChange={() => setChecked(!checked)} />;
};

export const Checked = Template.bind({});
Checked.args = {
    checked: true,
};

export const CheckedLabel = Template.bind({});
CheckedLabel.args = {
    checked: true,
    label: 'This is a checkbox',
};

export const CheckedDisabled = Template.bind({});
CheckedDisabled.args = {
    checked: true,
    disabled: true,
};

export const Unchecked = Template.bind({});
Unchecked.args = {
    checked: false,
};

export const UncheckedDisabled = Template.bind({});
UncheckedDisabled.args = {
    checked: false,
    disabled: true,
};
