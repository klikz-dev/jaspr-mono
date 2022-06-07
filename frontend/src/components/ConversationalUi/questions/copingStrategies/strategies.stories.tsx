import { action } from '@storybook/addon-actions';
import MockAdapter from 'axios-mock-adapter';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import AxiosMock from 'tests/mocks';
import CopingStrategies from '.';
import config from 'config';

export default {
    title: 'ConversationalUi/CopingStrategies',
    component: CopingStrategies,
    argTypes: {},
} as ComponentMeta<typeof CopingStrategies>;

const Template: ComponentStory<typeof CopingStrategies> = (args) => {
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
                <CopingStrategies
                    {...args}
                    setAnswered={setAnswered}
                    validate={{ current: async () => {} }}
                    questions={[
                        {
                            uid: 'copingBody',
                            guide: [
                                'Here are ways to calm your body chemistry. Select any of what seems good to you or add your own.',
                            ],
                            actions: [
                                {
                                    type: 'coping-strategy',
                                    answerKey: 'copingBody',
                                    choices: [
                                        'Cold shower',
                                        'Hot bath',
                                        'Hold ice',
                                        'Intense exercise',
                                        'Climb stairs',
                                        'Squats',
                                        'Paced breathing',
                                    ],
                                    allowCustom: true,
                                },
                                {
                                    type: 'buttons',
                                    buttons: [{ label: 'Done' }],
                                },
                            ],
                        },
                    ]}
                />
            </AxiosMock>
        </div>
    );
};

export const Default = Template.bind({});
Default.args = {
    answerKey: 'copingBody',
    choices: ['one', 'two', 'red', 'blue'],
};

Default.parameters = {
    initialState: {
        ...Default.parameters,
        assessment: {
            answers: {},
        },
    },
};
