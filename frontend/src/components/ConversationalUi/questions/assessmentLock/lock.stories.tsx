import { action } from '@storybook/addon-actions';
import MockAdapter from 'axios-mock-adapter';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import AxiosMock from 'tests/mocks';
import AssessmentLock from '.';
import config from 'config';

export default {
    title: 'ConversationalUi/AssessmentLock',
    component: AssessmentLock,
    argTypes: {},
} as ComponentMeta<typeof AssessmentLock>;

const Template: ComponentStory<typeof AssessmentLock> = (args) => {
    const next = action('next');
    const mock = (apiMock: MockAdapter) => {
        apiMock.onPatch(`${config.apiRoot}/me`).reply(200, {});
    };
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
            }}
        >
            <AxiosMock mock={mock}>
                <AssessmentLock {...args} next={next} />
            </AxiosMock>
        </div>
    );
};

export const Lock = Template.bind({});
