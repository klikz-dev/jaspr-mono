import React from 'react';
//import { action } from '@storybook/addon-actions';
import { Button } from '@storybook/react/demo';
import CUIButtons from 'components/conversational-ui/questions/buttons';
import CUIBulletPoint from 'components/conversational-ui/questions/bulletPoint';
import CUIChoice from 'components/conversational-ui/questions/choice';
import CUIComfortSkills from 'components/conversational-ui/questions/comfortSkills';
import CUICopingStrategies from 'components/conversational-ui/questions/copingStrategies';
import CUICounter from 'components/conversational-ui/questions/counter';
import CUIList from 'components/conversational-ui/questions/list';
import CUILoading from 'components/conversational-ui/questions/loading';
//import CUIMessage from 'components/conversational-ui/questions/message';

const Story = {
    title: 'Conversational UI',
    component: Button,
};

export default Story;

export const Buttons = () => (
    <CUIButtons
        answered={false}
        buttons={[{ label: 'Done' }]}
        next={() => {}}
        setAnswered={() => {}}
        setShowValidation={() => {}}
        answerKey="storybook-key"
        orientation="horizontal"
        isValid={true}
    />
);

export const BulletPoint = () => <CUIBulletPoint point="This is a bullet point" />;

export const Choice = () => (
    <CUIChoice
        options={[
            {
                label: 'I need to take care of my obligations',
                value: 'I need to take care of my obligations',
            },
            { label: 'I feel better and calmer', value: 'I feel better and calmer' },
            { label: 'I feel ready to cope', value: 'I feel ready to cope' },
            { label: 'My urge has gone down', value: 'My urge has gone down' },
            {
                label: 'This was a misunderstanding',
                value: 'This was a misunderstanding',
            },
            { label: "I'm frustrated", value: "I'm frustrated" },
            {
                label: 'People who support me understand how serious I am',
                value: 'People who support me understand how serious I am',
            },
            {
                label: 'My circumstances have changed',
                value: 'My circumstances have changed',
            },
        ]}
        answerKey="readinessYesReasons"
        answered={false}
        setAnswered={() => {}}
        multiple={true}
        vertical={true}
    />
);

export const ComfortSkils = () => <CUIComfortSkills />;

export const CopingStrategies = () => (
    <CUICopingStrategies
        answerKey="copingBody"
        choices={[
            'Cold shower',
            'Hot bath',
            'Hold ice',
            'Intense exercise',
            'Climb stairs',
            'Squats',
            'Paced breathing',
        ]}
        allowCustom={true}
    />
);

export const Counter = () => (
    <CUICounter
        answerKey="suicidalFreq|suicidalFreqUnits"
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
);

export const List = () => (
    <CUIList question="Reasons for living" maxLength={10000} rows={5} answerKey="reasonsLive" />
);

// ListRank

export const Loading = () => <CUILoading />;

// MeansCustom

// Message

// Rank

// Rank Top

// ScaleButtons

// SecurityImage

// SecurityQuestion

// SharedStories

// Slider

// Slideshow

// SortEdit

// StabilityCard

// SupportivePeople

// TabChoice

// Text

// Video
