import { ComponentStory, ComponentMeta } from '@storybook/react';
import StabilityCard from '.';

export default {
    title: 'ConversationalUi/StabilityCard',
    component: StabilityCard,
    argTypes: {},
} as ComponentMeta<typeof StabilityCard>;

const Template: ComponentStory<typeof StabilityCard> = (args) => {
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
                width: '100%',
            }}
        >
            <StabilityCard
                answered={false}
                answers={{
                    copingTop: ['Coping 1', 'Coping 2'],
                    reasonsLive: ['Reason1', 'Reason 2'],
                    wsTop: ['Warning 1', 'Warning 2'],
                }}
            />
        </div>
    );
};

export const Default = Template.bind({});
