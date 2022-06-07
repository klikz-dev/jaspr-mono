import { action } from '@storybook/addon-actions';
import MockAdapter from 'axios-mock-adapter';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import AxiosMock from 'tests/mocks';
import ListRank from '.';
import config from 'config';

export default {
    title: 'ConversationalUi/ListRank',
    component: ListRank,
    argTypes: {},
} as ComponentMeta<typeof ListRank>;

const Template: ComponentStory<typeof ListRank> = (args) => {
    const setAnswered = action('setAnswered');
    const mock = (apiMock: MockAdapter) => {
        apiMock.onPatch(`${config.apiRoot}/patient/answers`).reply(200, {});
    };
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
                width: '100%',
            }}
        >
            <AxiosMock mock={mock}>
                <ListRank {...args} answerKey="reasonsLive" setAnswered={setAnswered} />
            </AxiosMock>
        </div>
    );
};

export const Default = Template.bind({});
Default.args = {
    answerKey: 'reasonsLive',
};

Default.parameters = {
    initialState: {
        ...Default.parameters,
        assessment: {
            answers: {
                reasonsLive: ['My Dog', 'My Cat', 'My Friends'],
            },
        },
    },
};
