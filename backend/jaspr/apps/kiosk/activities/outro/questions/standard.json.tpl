[
    {
        "uid": "rateDistress1",
        "guide": [
            "I'd like to check in with you about how you're feeling after thinking all this through.",
            "How would you rate your distress?"
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "max": 10,
                "min": 1,
                "type": "scalebuttons",
                "maxLabel": "High Distress",
                "minLabel": "Low Distress",
                "answerKey": "distress1"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "rateFrustration1",
        "guide": ["How frustrated and agitated are you right now?"],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "max": 10,
                "min": 1,
                "type": "scalebuttons",
                "maxLabel": "Very frustrated / agitated",
                "minLabel": "Very Calm",
                "answerKey": "frustration1"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "jasprRating",
        "guide": [
            "Thank you for letting me know how you're feeling.",
            "I hope I've been helpful",
            "How would you rate the Jaspr app on a scale of 0 to 100, with 0 being the worst and 100 being the best."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "max": 100,
                "min": 0,
                "step": 1,
                "type": "slider",
                "maxLabel": "",
                "minLabel": "",
                "answerKey": "jasprRating"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "jasprRecommend",
        "guide": ["Would you recommend the Jaspr app to other people in your situation?"],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "jasprRecommend"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "overallErCare",
        "guide": ["How would you rate your overall experience in the emergency room?"],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "max": 5,
                "min": 1,
                "type": "scalebuttons",
                "maxLabel": "Very good",
                "minLabel": "Very poor",
                "answerKey": "overallErCare"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    }

{% if csp_assigned and not jah_consented %}

    ,{
        "uid": "giveConsent",
        "guide": [
            "Thanks for the feedback!",
            "Would you like your own access to your crisis plan and notes from today, by creating a Jaspr Health account?",
            "By selecting yes, Jaspr Health will keep a secure copy of your information, that you can access from your mobile phone. In future visits, you can also choose to share this information with your doctor or other healthcare providers. Your data is always in your control.\n\nBy selecting no, you will not be able to access your information in the future on your mobile device or at other healthcare providers."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "give-consent",
                "options": [
                    {
                        "label": "Yes",
                        "value": true,
                        "sublable": "Save my entries so I can access them later."
                    },
                    { "label": "No", "value": false, "sublable": "Do not save my information." }
                ],
                "answerKey": "giveConsent"
            }
        ]
    }

{% endif %}
    ,{
        "uid": "assessmentLock",
        "guide": ["I'll let your provider know you are done with the interview, okay?"],
        "actions": [
            {
                "type": "assessment-lock",
                "options": [
                    { "label": "I'm done", "value": true }
                ]
            }
        ]
    }
]