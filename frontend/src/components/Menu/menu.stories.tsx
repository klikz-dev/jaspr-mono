import { ComponentStory, ComponentMeta } from '@storybook/react';
import Menu from '.';

export default {
    title: 'Components/Menu',
    component: Menu,
    argTypes: {},
} as ComponentMeta<typeof Menu>;

const Template: ComponentStory<typeof Menu> = (args) => (
    <div style={{ position: 'relative', minHeight: 686 }}>
        <Menu {...args} />
    </div>
);

export const HomeSelected = Template.bind({});
HomeSelected.args = {
    selectedItem: 'home',
};
HomeSelected.parameters = {
    initialState: {
        ...HomeSelected.parameters,
        user: {
            inEr: true,
            timeSinceCheckin: 0,
            assessmentLockTimer: 0,
        },
        assessment: {
            assessmentLocked: false,
            currentSectionUid: 'ratePsych',
        },
    },
};

export const FirstCheckIndicator = Template.bind({});
FirstCheckIndicator.args = {
    selectedItem: 'home',
    timeSinceCheckin: 21,
};
FirstCheckIndicator.parameters = {
    initialState: {
        ...FirstCheckIndicator.parameters,
        user: {
            inEr: true,
            timeSinceCheckin: 20,
            assessmentLockTimer: 5,
        },
        assessment: {
            assessmentLocked: false,
            currentSectionUid: 'ratePsych',
        },
    },
};

export const SecondCheckIndicator = Template.bind({});
SecondCheckIndicator.args = {
    selectedItem: 'home',
    timeSinceCheckin: 21,
};
SecondCheckIndicator.parameters = {
    initialState: {
        ...SecondCheckIndicator.parameters,
        user: {
            inEr: true,
            timeSinceCheckin: 30,
            assessmentLockTimer: 5,
        },
        assessment: {
            assessmentLocked: false,
            currentSectionUid: 'ratePsych',
        },
    },
};
