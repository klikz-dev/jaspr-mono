import { ComponentStory, ComponentMeta } from '@storybook/react';
import Hamburger from './';

export default {
    title: 'Components/Hamburger',
    component: Hamburger,
    argTypes: {},
    docs: { inlineStories: false },
} as ComponentMeta<typeof Hamburger>;

const Template: ComponentStory<typeof Hamburger> = (args) => (
    <div style={{ position: 'relative' }}>
        <Hamburger {...args} />
    </div>
);

export const Patient = Template.bind({});

Patient.parameters = {
    initialState: {
        ...Patient.parameters,
        user: {
            firstName: 'John',
            lastName: 'Doe',
            userType: 'patient',
            dateOfBirth: '1985-10-11',
            mrn: '123456',
            inEr: true,
            tourComplete: true,
            sessionLocked: false,
        },
    },
};

export const PatientTourUnfinished = Template.bind({});
PatientTourUnfinished.parameters = {
    initialState: {
        ...Patient.parameters,
        user: {
            firstName: 'John',
            lastName: 'Doe',
            userType: 'patient',
            dateOfBirth: '1985-10-11',
            mrn: '123456',
            inEr: true,
            tourComplete: false,
            sessionLocked: false,
        },
    },
};

export const PatientSessionLocked = Template.bind({});
PatientSessionLocked.parameters = {
    initialState: {
        ...Patient.parameters,
        user: {
            firstName: 'John',
            lastName: 'Doe',
            userType: 'patient',
            dateOfBirth: '1985-10-11',
            mrn: '123456',
            inEr: true,
            tourComplete: true,
            sessionLocked: true,
        },
    },
};

export const Technician = Template.bind({});
Technician.parameters = {
    initialState: {
        ...Patient.parameters,
        user: {
            userType: 'technician',
            inEr: false,
        },
    },
};
