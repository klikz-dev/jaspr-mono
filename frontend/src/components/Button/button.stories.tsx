import { ComponentStory, ComponentMeta } from '@storybook/react';
import { Button } from '.';

export default {
    title: 'Components/Button',
    component: Button,
    argTypes: {
        icon: {
            control: {
                type: 'select',
            },
        },
    },
} as ComponentMeta<typeof Button>;

const Template: ComponentStory<typeof Button> = (args) => {
    const { children, ...rest } = args;
    return <Button {...rest}>{children}</Button>;
};

export const Primary = Template.bind({});
Primary.args = {
    variant: 'primary',
    children: 'Submit',
    dark: false,
    disabled: false,
};

export const PrimaryDark = Template.bind({});
PrimaryDark.args = {
    variant: 'primary',
    children: 'Submit',
    dark: true,
    disabled: false,
};

export const PrimaryWithIcon = Template.bind({});
PrimaryWithIcon.args = {
    variant: 'primary',
    children: 'Submit',
    icon: 'plus',
    dark: false,
    disabled: false,
};

export const PrimaryDarkWithIcon = Template.bind({});
PrimaryDarkWithIcon.args = {
    variant: 'primary',
    children: 'Submit',
    icon: 'plus',
    dark: true,
    disabled: false,
};

export const PrimaryDarkWithIconDisabled = Template.bind({});
PrimaryDarkWithIconDisabled.args = {
    variant: 'primary',
    children: 'Submit',
    icon: 'plus',
    dark: true,
    disabled: true,
};

export const Secondary = Template.bind({});
Secondary.args = {
    variant: 'secondary',
    children: 'Submit',
    dark: false,
};

export const SecondaryDark = Template.bind({});
SecondaryDark.args = {
    variant: 'secondary',
    children: 'Submit',
    dark: true,
};

export const SecondaryWithIcon = Template.bind({});
SecondaryWithIcon.args = {
    variant: 'secondary',
    children: 'Submit',
    icon: 'plus',
    dark: false,
};

export const SecondaryDarkWithIcon = Template.bind({});
SecondaryDarkWithIcon.args = {
    variant: 'secondary',
    children: 'Submit',
    icon: 'plus',
    dark: true,
};

export const Tertiary = Template.bind({});
Tertiary.args = {
    variant: 'tertiary',
    children: 'Submit',
    dark: false,
};

export const TertiaryDark = Template.bind({});
TertiaryDark.args = {
    variant: 'tertiary',
    children: 'Submit',
    dark: true,
};

export const TertiaryWithPencil = Template.bind({});
TertiaryWithPencil.args = {
    variant: 'tertiary',
    children: 'Submit',
    icon: 'plus',
    dark: false,
};

export const TertiaryDarkWithPencil = Template.bind({});
TertiaryDarkWithPencil.args = {
    variant: 'tertiary',
    children: 'Submit',
    icon: 'plus',
    dark: true,
};
