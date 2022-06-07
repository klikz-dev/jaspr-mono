import { action } from '@storybook/addon-actions';
import MockAdapter from 'axios-mock-adapter';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import AxiosMock from 'tests/mocks';
import Choice from '.';
import config from 'config';

export default {
    title: 'ConversationalUi/Choice',
    component: Choice,
    argTypes: {},
} as ComponentMeta<typeof Choice>;

const Template: ComponentStory<typeof Choice> = (args) => {
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
                <Choice {...args} setAnswered={setAnswered} />
            </AxiosMock>
        </div>
    );
};

export const Horizontal = Template.bind({});
Horizontal.args = {
    question: 'This is the question',
    subtitle: 'This is the subtitle',
    options: [
        { label: 'Choice 1', value: '1' },
        { label: 'Choice 2', value: '2' },
        { label: 'Choice 3', value: '3' },
    ],
    multiple: false,
    vertical: false,
};

export const Vertical = Template.bind({});
Vertical.args = {
    question: 'This is the question',
    subtitle: 'This is the subtitle',
    options: [
        { label: 'Choice 1', value: '1' },
        { label: 'Choice 2', value: '2' },
        { label: 'Choice 3', value: '3' },
    ],
    multiple: false,
    vertical: true,
};

export const MultipleAnswer = Template.bind({});
MultipleAnswer.args = {
    question: 'This is the question',
    subtitle: 'This is the subtitle',
    options: [
        { label: 'Choice 1', value: '1' },
        { label: 'Choice 2', value: '2' },
        { label: 'Choice 3', value: '3' },
    ],
    multiple: true,
    vertical: false,
};
