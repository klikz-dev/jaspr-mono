import { action } from '@storybook/addon-actions';
import MockAdapter from 'axios-mock-adapter';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import AxiosMock from 'tests/mocks';
import List from '.';
import config from 'config';

export default {
    title: 'ConversationalUi/List',
    component: List,
    argTypes: {},
} as ComponentMeta<typeof List>;

const Template: ComponentStory<typeof List> = (args) => {
    const setAnswered = action('setAnswered');
    const mock = (apiMock: MockAdapter) => {
        apiMock.onPatch(`${config.apiRoot}/patient/answers`).reply(200, {});
    };
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
            }}
        >
            <AxiosMock mock={mock}>
                <List
                    {...args}
                    answerKey="reasonsLive"
                    rows={5}
                    question="Customizable Question"
                    maxLength={1000}
                    setAnswered={setAnswered}
                />
            </AxiosMock>
        </div>
    );
};

export const Default = Template.bind({});
