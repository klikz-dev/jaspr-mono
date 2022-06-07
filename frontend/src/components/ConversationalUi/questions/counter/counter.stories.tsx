import { action } from '@storybook/addon-actions';
import MockAdapter from 'axios-mock-adapter';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import AxiosMock from 'tests/mocks';
import Counter from '.';
import config from 'config';

export default {
    title: 'ConversationalUi/Counter',
    component: Counter,
    argTypes: {},
} as ComponentMeta<typeof Counter>;

const Template: ComponentStory<typeof Counter> = (args) => {
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
                <Counter
                    {...args}
                    setAnswered={setAnswered}
                    answerKeyCount="suicidalFreq"
                    answerKeyUnit="suicidalFreqUnits"
                    options={[
                        {
                            value: 'day',
                            label: 'Day',
                        },
                        {
                            value: 'week',
                            label: 'Week',
                        },
                        {
                            value: 'month',
                            label: 'Month',
                        },
                    ]}
                />
            </AxiosMock>
        </div>
    );
};

export const Default = Template.bind({});
