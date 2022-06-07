import { ComponentStory, ComponentMeta } from '@storybook/react';
import CheckinMonitor from '.';

export default {
    title: 'Components/CheckinMonitor',
    component: CheckinMonitor,
    argTypes: {},
} as ComponentMeta<typeof CheckinMonitor>;

const Template: ComponentStory<typeof CheckinMonitor> = (args) => <CheckinMonitor {...args} />;

export const InterviewUnlocked = Template.bind({});
InterviewUnlocked.args = {
    selectedItem: 'home',
};
InterviewUnlocked.parameters = {
    initialState: {
        ...InterviewUnlocked.parameters,
        user: {
            inEr: true,
            timeSinceCheckin: 0,
            assessmentLockTimer: 0,
            userType: 'patient',
            authenticated: true,
        },
        assessment: {
            assessmentLocked: false,
            currentSectionUid: 'ratePsych',
        },
    },
};

export const Checkin = Template.bind({});
Checkin.args = {
    selectedItem: 'home',
};
Checkin.parameters = {
    initialState: {
        ...Checkin.parameters,
        user: {
            inEr: true,
            timeSinceCheckin: 30,
            assessmentLockTimer: 0,
            userType: 'patient',
            authenticated: true,
        },
        assessment: {
            assessmentLocked: false,
            currentSectionUid: 'ratePsych',
        },
    },
};
