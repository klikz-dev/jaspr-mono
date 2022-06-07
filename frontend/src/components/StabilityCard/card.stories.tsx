import { ComponentStory, ComponentMeta } from '@storybook/react';
import SortEdit from '.';

export default {
    title: 'Components/StabilityCard',
    component: SortEdit,
    argTypes: {},
} as ComponentMeta<typeof SortEdit>;

const Template: ComponentStory<typeof SortEdit> = (args) => {
    return (
        <SortEdit
            answers={{
                copingTop: ['Coping 1', 'Coping 2'],
                reasonsLive: ['Reason1', 'Reason 2'],
                wsTop: ['Warning 1', 'Warning 2'],
            }}
        />
    );
};

export const Default = Template.bind({});
