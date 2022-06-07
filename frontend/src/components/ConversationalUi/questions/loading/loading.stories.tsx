import { ComponentStory, ComponentMeta } from '@storybook/react';
import Loading from '.';

export default {
    title: 'ConversationalUi/Loading',
    component: Loading,
    argTypes: {},
} as ComponentMeta<typeof Loading>;

const Template: ComponentStory<typeof Loading> = (args) => {
    return <Loading />;
};

export const Default = Template.bind({});
