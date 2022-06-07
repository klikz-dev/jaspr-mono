import MockAdapter from 'axios-mock-adapter';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import AxiosMock from 'tests/mocks';
import MaintenanceNotice from '.';

export default {
    title: 'Components/MaintenanceNotice',
    component: MaintenanceNotice,
    argTypes: {},
} as ComponentMeta<typeof MaintenanceNotice>;

const Template: ComponentStory<typeof MaintenanceNotice> = (args) => {
    const mock = (apiMock: MockAdapter) => {
        apiMock.onGet('http://localhost:6006/maintenance.json').reply(200, {});
    };
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
            }}
        >
            <AxiosMock mock={mock}>
                <MaintenanceNotice {...args} />
            </AxiosMock>
        </div>
    );
};

export const Default = Template.bind({});
