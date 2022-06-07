import { action } from '@storybook/addon-actions';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import TabChoice from '.';

export default {
    title: 'ConversationalUi/TabChoice',
    component: TabChoice,
    argTypes: {},
} as ComponentMeta<typeof TabChoice>;

const Template: ComponentStory<typeof TabChoice> = (args) => {
    const setAnswered = action('setAnswered');
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
                width: '100%',
            }}
        >
            <TabChoice
                uid="uid"
                setAnswered={setAnswered}
                answered={false}
                groups={[
                    {
                        answerKey: 'strategiesFirearm',
                        label: 'Firearm',
                        options: [
                            {
                                label: 'Family, friend, or neighbor',
                                value: 'Family, friend, or neighbor',
                            },
                            { label: 'Gun dealers', value: 'Gun dealers' },
                            { label: 'Shooting range', value: 'Shooting range' },
                            {
                                label: 'Commercial storage facility',
                                value: 'Commercial storage facility',
                            },
                            { label: 'Pawn shop', value: 'Pawn shop' },
                            { label: 'Police/sheriff', value: 'Police/sheriff' },
                            { label: 'Lock box', value: 'Lock box' },
                            { label: 'Gun safe', value: 'Gun safe' },
                            { label: 'Locking device', value: 'Locking device' },
                            { label: 'Disassemble ', value: 'Disassemble ' },
                        ],
                    },

                    {
                        answerKey: 'strategiesMedicine',
                        label: 'Medicine',
                        options: [
                            { label: 'Disposal', value: 'Disposal' },
                            { label: 'Locked up at home', value: 'Locked up at home' },
                            {
                                label: 'Stored with a trusted person',
                                value: 'Stored with a trusted person',
                            },
                        ],
                    },
                    {
                        answerKey: 'strategiesPlaces',
                        label: 'Dangerous Places',
                        options: [{ label: 'Avoid location', value: 'Avoid location' }],
                    },
                    {
                        answerKey: 'strategiesOther',
                        label: 'Other Hazards',
                        options: [
                            {
                                label: 'Limit access when and where it is possible',
                                value: 'Limit access when and where it is possible',
                            },
                            {
                                label: 'Have list of emergency response and lifelines available',
                                value: 'Have list of emergency response and lifelines available',
                            },
                        ],
                    },
                ]}
            />
        </div>
    );
};

export const Default = Template.bind({});
