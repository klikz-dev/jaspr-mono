import { Questions } from 'components/ConversationalUi/questions';

interface BaselineQuestions {
    default: Questions;
    path3: Questions;
}

const questions: BaselineQuestions = {
    path3: [
        {
            uid: 'welcome',
            guide: [
                "Hi, I'm Jaz, an automated assistant.",
                "In times of distress, watching comforting videos or listening to people's stories who may be able to relate can be helpful.",
                'We’d like to share them with you.',
            ],
            actions: [
                {
                    type: 'buttons',
                    buttons: [{ label: 'Okay' }],
                },
            ],
        },
        {
            uid: 'setSecurityImage',
            guide: ['To protect your privacy, let’s set a password. First pick a secret image.'],
            actions: [
                {
                    type: 'security-image',
                },
                {
                    type: 'buttons',
                    validation: true,
                    buttons: [{ label: 'Done' }],
                },
            ],
        },
        {
            uid: 'setSecurityQuestion',
            guide: ['Now pick a security question and answer.'],
            actions: [
                {
                    type: 'security-question',
                },
                {
                    type: 'buttons',
                    validation: false,
                    orientation: 'horizontal',
                    buttons: [
                        {
                            label: 'Done',
                            action: 'navigate',
                            path: '/',
                        },
                    ],
                },
            ],
        },
    ],
    default: [
        {
            uid: 'welcome',
            guide: [
                "Hi, I'm Jaz, an automated assistant.",
                "I'm happy to show you around.  But first, may I ask how long have you been here?",
            ],
            actions: [
                {
                    type: 'buttons',
                    answerKey: 'timeHere',
                    buttons: [
                        { label: 'Just got here' },
                        { label: 'At least a few hours, less than 24 hours' },
                        { label: 'More than 24 hours' },
                    ],
                },
            ],
        },
        {
            uid: 'rateDistress',
            guide: [
                'How are you doing emotionally right now?',
                'How would you rate your distress? 1, not at all distressed, to 10, the highest distress you have ever felt?',
            ],
            actions: [
                {
                    type: 'scalebuttons',
                    min: 1,
                    max: 10,
                    minLabel: 'Low Distress',
                    maxLabel: 'High Distress',
                    answerKey: 'distress0',
                },
                {
                    type: 'buttons',
                    buttons: [{ label: 'Done' }],
                },
            ],
        },
        {
            uid: 'rateFrustration',
            guide: ['How frustrated and agitated are you right now?'],
            actions: [
                {
                    type: 'scalebuttons',
                    min: 1,
                    max: 10,
                    minLabel: 'Very Calm',
                    maxLabel: 'High agitation / frustration',
                    answerKey: 'frustration0',
                },
                {
                    type: 'buttons',
                    buttons: [{ label: 'Done' }],
                },
            ],
        },
        {
            uid: 'setSecurityImage',
            guide: [
                "It's really likely you will get interrupted while you're using Jaspr.",
                "Let's set a secret image — like a password — so you can open and close the app as you need.",
                'If you forget, a staff member can help you, too.',
            ],
            actions: [
                {
                    type: 'security-image',
                },
                {
                    type: 'buttons',
                    validation: true,
                    buttons: [{ label: 'Done' }],
                },
            ],
        },
        {
            uid: 'setSecurityQuestion',
            guide: [
                'In addition to a secret image, pick a security question and provide the answer.',
                "This way, no one else can access the app while you're using it.",
            ],
            actions: [
                {
                    type: 'security-question',
                },
                {
                    type: 'buttons',
                    validation: true,
                    buttons: [
                        {
                            label: 'Done',
                            action: 'navigate',
                            path: '/question',
                            params: '?completeTour=true',
                            analyticsAction: 'EXPLORE',
                        },
                    ],
                },
            ],
        },
    ],
};

export default questions;
