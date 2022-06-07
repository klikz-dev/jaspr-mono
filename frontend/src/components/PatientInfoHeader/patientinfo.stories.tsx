import { ComponentStory, ComponentMeta } from '@storybook/react';
import PatientInfoHeader from '.';

export default {
    title: 'Components/PatientInfoHeader',
    component: PatientInfoHeader,
    argTypes: {},
} as ComponentMeta<typeof PatientInfoHeader>;

const Template: ComponentStory<typeof PatientInfoHeader> = (args) => (
    <div style={{ position: 'relative', width: '100%' }}>
        <PatientInfoHeader {...args} />
    </div>
);

export const MRN = Template.bind({});
MRN.args = {
    dateOfBirth: '1985-10-11',
    mrn: '123498765',
    ssid: '',
    firstName: 'John',
    lastName: 'Doe',
    answers: {
        created: '2021-10-22T17:00:49.338541Z',
        modified: '2021-10-22T17:01:54.528219Z',
    },
};

export const SSID = Template.bind({});
SSID.args = {
    dateOfBirth: '',
    mrn: '',
    ssid: 'ABC123',
    firstName: '',
    lastName: '',
    answers: {
        created: '2021-10-22T17:00:49.338541Z',
        modified: '2021-10-22T17:01:54.528219Z',
    },
};
