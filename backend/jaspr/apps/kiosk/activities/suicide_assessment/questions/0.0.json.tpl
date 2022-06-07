[
    {
        "uid": "sectionChangeSpecificRisk",
        "guide": [],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Specific Risk & Protective Factors",
        "provider_order": 0,
        "actions": [
            {
                "type": "section-change",
                "label": "Specific Risk & Protective Factors",
                "section": "specific_risk"
            }
        ]
    },
    {
        "uid": "start",
        "guide": [
            "I'd love to work with you now to gather information so your treatment team can get you the best help."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [{ "type": "buttons", "buttons": [{ "label": "Start" }] }]
    },
    {
        "uid": "drivers",
        "guide": [
            "This interview is about drivers - the kinds of things that may directly cause many people to feel suicidal.",
            "I know this is really private, but the more detail you can share the better your providers will be able to help you."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [{ "type": "buttons", "buttons": [{ "label": "Okay, I'll do my best" }] }]
    },
    {
        "uid": "ratePsych",
        "guide": [
            "How would you rate your psychological pain?",
            "This is emotional pain, like anguish or misery, not physical pain or stress. Tap the number that best says how you feel right now."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "max": 5,
                "min": 1,
                "type": "scalebuttons",
                "maxLabel": "High pain",
                "minLabel": "Low pain",
                "answerKey": "ratePsych"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "ratePsychText",
        "guide": ["In this part, you fill in the blank to say what you find most painful."],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "text",
                "label": "What I find most painful is...",
                "answerKey": "mostPainful",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "rateStress",
        "guide": [
            "Okay, thank you. The next question asks about stress.",
            "When you think about how you have been feeling, how would you rate your stress?",
            "In other words how overwhelmed or pressured do you feel right now. Tap the number that best says how you feel right now."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "max": 5,
                "min": 1,
                "type": "scalebuttons",
                "maxLabel": "High stress",
                "minLabel": "Low stress",
                "answerKey": "rateStress"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "rateStressText",
        "guide": ["In the blank, please write what you are finding most stressful."],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "text",
                "label": "What I find most stressful is...",
                "answerKey": "mostStress",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "rateAgitation",
        "guide": [
            "Okay, the next is about agitation.",
            "How would you rate your agitation?",
            "This is emotional urgency, the feeling that you need to take action. This is not irritation or annoyance."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "max": 5,
                "min": 1,
                "type": "scalebuttons",
                "maxLabel": "High agitation",
                "minLabel": "Low agitation",
                "answerKey": "rateAgitation"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "rateAgitationText",
        "guide": [
            "Okay, thank you.",
            "When do you most need to take action as a result of feeling agitated?"
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "text",
                "label": "I most need to take action when...",
                "answerKey": "causesAgitation",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "rateHopeless",
        "guide": [
            "How would you rate your hopelessness?",
            "This is your expectation that things will not get better no matter what you do."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "max": 5,
                "min": 1,
                "type": "scalebuttons",
                "maxLabel": "High hopelessness",
                "minLabel": "Low hopelessness",
                "answerKey": "rateHopeless"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "rateHopelessText",
        "guide": ["What do you feel most hopeless about?"],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "text",
                "label": "I am most hopeless about...",
                "answerKey": "mostHopeless",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "rateSelfHate",
        "guide": [
            "How would you rate your self-hate?",
            "This is your general feeling of disliking yourself; having no self-esteem; having no self-respect."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "max": 5,
                "min": 1,
                "type": "scalebuttons",
                "maxLabel": "High self-hate",
                "minLabel": "Low self-hate",
                "answerKey": "rateSelfHate"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "rateSelfHateText",
        "guide": ["What do you hate most about yourself?"],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "text",
                "label": "What I hate most about myself is...",
                "answerKey": "mostHate",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "rankFeelings",
        "guide": [
            "Here are your responses to the last questions.",
            "Can you please drag these to show the order of what's important to you (1=most important to 5=least important)?"
        ],
        "showIf": [],
        "hideIf": [],
        "provider_label": "",
        "provider_order": 1,
        "actions": [
            {
                "type": "rank",
                "options": [
                    {
                        "title": "PSYCHOLOGICAL PAIN: ${ratePsych || '[-]'} out of 5",
                        "question": "Psychological pain",
                        "subtitle": "What I find most painful is ${mostPainful || '[-]'}",
                        "answerKey": "ratePsych|mostPainful"
                    },
                    {
                        "title": "STRESS: ${rateStress || '[-]'} out of 5",
                        "question": "Stress",
                        "subtitle": "What I find most stressful is ${mostStress || '[-]'}",
                        "answerKey": "rateStress|mostStress"
                    },
                    {
                        "title": "AGITATION: ${rateAgitation || '[-]'} out of 5",
                        "question": "Agitation",
                        "subtitle": "I most need to take action when ${causesAgitation || '[-]'}",
                        "answerKey": "rateAgitation|causesAgitation"
                    },
                    {
                        "title": "HOPELESSNESS: ${rateHopeless || '[-]'} out of 5",
                        "question": "Hopelessness",
                        "subtitle": "I feel most hopeless when ${mostHopeless || '[-]'}",
                        "answerKey": "rateHopeless|mostHopeless"
                    },
                    {
                        "title": "SELF-HATE: ${rateSelfHate || '[-]'} out of 5",
                        "question": "Self-hate",
                        "subtitle": "What I hate most about myself is ${mostHate || '[-]'}",
                        "answerKey": "rateSelfHate|mostHate"
                    }
                ],
                "maxLabel": "MOST IMPORTANT",
                "minLabel": "LEAST IMPORTANT",
                "answerKey": "rankFeelings"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "suicideRisk",
        "guide": [
            "How would you rate your overall risk of suicide?",
            "This question means how much you want to take your life right now. ",
            "I would like to know how you honestly feel, not what you think you are supposed to say.",
            "With 5 being you are going to take your life and 1 being you are not going to take your life, where are you right now?"
        ],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Overall Risk of Suicide (1-5)",
        "provider_order": 2,
        "actions": [
            {
                "max": 5,
                "min": 1,
                "type": "scalebuttons",
                "maxLabel": "Extremely high risk (will kill self)",
                "minLabel": "Extremely low risk (will not kill self)",
                "answerKey": "suicideRisk"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "suicidalAboutYourself",
        "guide": ["How much is being suicidal related to thoughts and feelings about yourself?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Suicide related to thoughts about yourself (1-5)",
        "provider_order": 3,
        "actions": [
            {
                "max": 5,
                "min": 1,
                "type": "scalebuttons",
                "maxLabel": "Completely",
                "minLabel": "Not at all",
                "answerKey": "suicidalYourself"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "suicidalAboutOthers",
        "guide": ["How much is being suicidal related to thoughts and feelings about others?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Suicide related to thoughts about others (1-5)",
        "provider_order": 4,
        "actions": [
            {
                "max": 5,
                "min": 1,
                "type": "scalebuttons",
                "maxLabel": "Completely",
                "minLabel": "Not at all",
                "answerKey": "suicidalOthers"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "reasonsLiveDie",
        "guide": [
            "Usually people who are suicidal have reasons for living and they also have reasons for dying. They can have both. Feeling mixed is very common.",
            "What are your reasons for living and dying?",
            "Write down what's important. Click done when you're finished."
        ],
        "showIf": [],
        "hideIf": [],
        "provider_label": "",
        "provider_order": 5,
        "actions": [
            {
                "rows": 5,
                "type": "list",
                "question": "Reasons for living",
                "answerKey": "reasonsLive",
                "maxLength": 10000
            },
            {
                "rows": 5,
                "type": "list",
                "question": "Reasons for dying",
                "answerKey": "reasonsDie",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "rankReasonsLive",
        "guide": [
            "So I can understand, can you rank these by importance?",
            "Sometimes it can feel hard to put a number. Go with your gut feeling. When you think of your most important reason for living, which comes to mind first? Rank that first, then continue through until they are rank ordered."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "list-rank",
                "maxLabel": "MOST IMPORTANT",
                "minLabel": "LEAST IMPORTANT",
                "answerKey": "reasonsLive"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "rankReasonsDie",
        "guide": [
            "Okay, now let's rank your reasons for dying.",
            "Drag them to show what's most important at the top and then order the rest."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "list-rank",
                "maxLabel": "MOST IMPORTANT",
                "minLabel": "LEAST IMPORTANT",
                "answerKey": "reasonsDie"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "wishLive",
        "guide": [
            "It's very common to have both a wish to live and a wish to die at the same time. It really helps to understand how strong each is.",
            "Please rate the strength of your wish to live, 0 is not at all and 8 is very much wish to live."
        ],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Wish to live to the following extent (0-8)",
        "provider_order": 6,
        "actions": [
            {
                "max": 8,
                "min": 0,
                "type": "scalebuttons",
                "maxLabel": "Very much",
                "minLabel": "Not at all",
                "answerKey": "wishLive"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "wishDie",
        "guide": [
            "Please rate the strength of your wish to die where 0 is not at all and 8 is very much wish to die."
        ],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Wish to die to the following extent (0-8)",
        "provider_order": 7,
        "actions": [
            {
                "max": 8,
                "min": 0,
                "type": "scalebuttons",
                "maxLabel": "Very much",
                "minLabel": "Not at all",
                "answerKey": "wishDie"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "oneThing",
        "guide": [
            "Now, I'd like to understand what is the one thing that could really help make you no longer feel suicidal?",
            "By this it means one change that if it happened would really help you no longer feel suicidal. Again, use your gut - if there were one thing that would make you no longer feel suicidal what would that be?"
        ],
        "showIf": [],
        "hideIf": [],
        "provider_label": "If there were one thing that would make you no longer feel suicidal, what would that be?",
        "provider_order": 8,
        "actions": [
            { "type": "text", "label": "", "answerKey": "oneThing", "maxLength": 10000 },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "ssfAReview",
        "guide": [
            "Thank you for telling me how you are feeling. I know it can be hard to talk about it all.",
            "This information really helps your providers get you the best treatment.",
            "In the next part of the interview, I will ask you questions from a questionnaire that everybody completes.",
            "So some of it might not apply to you. That's okay. Just answer the best you can."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [{ "type": "buttons", "buttons": [{ "label": "Okay, I'll start on it" }] }]
    },
    {
        "uid": "sectionChangeGeneralRisk",
        "guide": [],
        "showIf": [],
        "hideIf": [],
        "provider_label": "General Risk Factors",
        "provider_order": 9,
        "actions": [
            { "type": "section-change", "label": "General Risk Factors", "section": "general_risk" }
        ]
    },
    {
        "uid": "suicidalDescribe",
        "guide": ["Do you have suicidal thoughts?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Do you have suicidal thoughts?",
        "provider_order": 10,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "suicidalYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "suicidalYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "suicidalFreq",
        "guide": ["How frequently do you think about suicide?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "How frequently do you think about suicide?",
        "provider_order": 11,
        "actions": [
            {
                "type": "counter",
                "options": [
                    { "label": "Day", "value": "day" },
                    { "label": "Week", "value": "week" },
                    { "label": "Month", "value": "month" }
                ],
                "answerKey": "suicidalFreq|suicidalFreqUnits",
                "answerKeyUnit": "suicidalFreqUnits",
                "answerKeyCount": "suicidalFreq"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "suicidalLength",
        "guide": ["When you think about suicide, how long do the thoughts last?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "When you think about suicide, how long do the thoughts last?",
        "provider_order": 12,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Seconds", "value": "seconds" },
                    { "label": "Minutes", "value": "minutes" },
                    { "label": "Hours", "value": "hours" }
                ],
                "answerKey": "lengthSuicidalThought"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "worseDescribe",
        "guide": ["Are these thoughts about killing yourself new or worse than usual for you?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Are these thoughts about killing yourself new or worse than usual for you?",
        "provider_order": 13,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "worseYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "worseYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "plansDescribe",
        "guide": ["Do you have a plan or plans of how you would end your life?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Do you have a plan or plans of how you would end your life?",
        "provider_order": 14,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "planYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "planYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "meansDescribe",
        "guide": [
            "Do you have access to the means to take your life? (e.g. stash of pills, guns, or any other method)"
        ],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Do you have access to the means to take your life?",
        "provider_order": 15,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "meansYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "meansYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "firearmDescribe",
        "guide": ["Do you have access to a firearm?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Do you have access to a firearm?",
        "provider_order": 16,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "firearmsYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "firearmsYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "stepsDescribe",
        "guide": [
            "Have you taken any steps to prepare to take your life?",
            "(e.g. put your affairs in order, written a suicide note, or other steps)"
        ],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Have you taken any steps to prepare to take your life?",
        "provider_order": 17,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "stepsYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "stepsYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "practicedDescribe",
        "guide": ["Have you practiced (rehearsed) how you would take your life?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Have you practiced how you would take your life?",
        "provider_order": 18,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "practicedYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "practicedYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "currentDescribe",
        "guide": ["Are you here today because of a current suicide attempt?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Are you here today because of a current suicide attempt?",
        "provider_order": 20,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "currentYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "currentYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "intentDescribe",
        "guide": ["Have you ever made an attempt to kill yourself with the intent to die?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Have you ever made an attempt to kill yourself with the intent to die?",
        "provider_order": 19,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "intentYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "intentYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "timesTriedDescribe",
        "guide": ["How many suicide attempts have you made in your lifetime?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "How many suicide attempts have you made in your lifetime?",
        "provider_order": 21,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "No attempts", "value": "no attempts" },
                    { "label": "Single attempt", "value": "once" },
                    { "label": "Multiple attempts (2 or more)", "value": "many" }
                ],
                "answerKey": "timesTried"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "timesTriedDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "nssiDescribe",
        "guide": [
            "Have you ever intentionally injured yourself without intending to kill yourself?"
        ],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Have you ever intentionally injured yourself without intending to kill yourself?",
        "provider_order": 22,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "nssiYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "nssiYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "hospitalizedDescribe",
        "guide": ["Have you ever been hospitalized for a mental health or substance use problem?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Have you ever been hospitalized for a mental health or substance use problem?",
        "provider_order": 23,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "hospitalizedYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "hospitalizedYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "impulsiveDescribe",
        "guide": ["Do you or others think you are impulsive?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Do you or others think you are impulsive?",
        "provider_order": 24,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "impulsiveYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "impulsiveYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "abuseDescribe",
        "guide": ["Do you or others think you have an alcohol or drug abuse problem?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Do you or others think you have an alcohol or drug abuse problem?",
        "provider_order": 25,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "abuseYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "abuseYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "lossesDescribe",
        "guide": ["Have you experienced a death, the loss of a job, or other losses?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Have you experienced death, the loss of a job, or other losses?",
        "provider_order": 26,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "lossesYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "lossesYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "relationshipDescribe",
        "guide": ["Are you having romantic and/or relationship problems?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Are you having romantic and/or relationship problems?",
        "provider_order": 27,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "relationshipYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "relationshipYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "burdenDescribe",
        "guide": ["Do you feel that others will be better off without you?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Do you feel that others will be better off without you?",
        "provider_order": 28,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "burdenOnOthersYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "burdenOnOthersYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "healthDescribe",
        "guide": ["Are you having any health or physical pain problems?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Are you having health or physical pain problems?",
        "provider_order": 29,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "healthYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "healthYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "sleepDescribe",
        "guide": ["Are you having problems falling asleep, staying asleep, or sleeping too much?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Are you having problems falling asleep, staying asleep, or sleeping too much?",
        "provider_order": 30,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "sleepYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "sleepYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "legalDescribe",
        "guide": ["Are you having any legal or financial problems?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Are you having any legal or financial problems?",
        "provider_order": 31,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "legalYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "legalYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "shameDescribe",
        "guide": [
            "Are you experiencing shame about anything in your history or your current life?"
        ],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Are you experiencing shame about anything in your history or your current life?",
        "provider_order": 32,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "shameYesNo"
            },
            {
                "type": "text",
                "label": "Describe:",
                "answerKey": "shameYesNoDescribe",
                "maxLength": 10000
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "ssfaFinish",
        "guide": ["Thank you for sharing the things that have been impacting you."],
        "showIf": [],
        "hideIf": [],
        "actions": [
            { "type": "buttons", "buttons": [{ "label": "Okay, I'm ready for the next part" }] }
        ]
    }
]
