[
     {
        "uid": "sectionChangeStabilityPlan",
        "guide": [],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Patient {{ stability_plan_label }}",
        "provider_order": 36,
        "actions": [
            {
                "type": "section-change",
                "label": "Patient {{ stability_plan_label }}",
                "section": "csp"
            }
        ]
    },
    {
        "uid": "survivingMakesSense",
        "guide": [
            "Surviving a crisis of intense urges to take your life is like surviving other emergencies."
        ],
        "actions": [
            {
                "type": "buttons",
                "buttons": [{ "label": "Makes sense" }]
            }
        ]
    },


    {
        "uid": "iCanHelp",
        "guide": [
            "I want to help you start a plan to get through the hardest crisis times when you have intense urges to take your life."
        ],
        "actions": [
            {
                "type": "buttons",
                "buttons": [{ "label": "Okay" }]
            }
        ]
    },
{% if not csa_assigned %}
    {
        "uid": "SsiIntroVideo",
        "guide": [],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "name": "Crisis Stability Plan Intro",
                "type": "video",
                "poster": "{{media_root_url}}crisis-stability-plan-intro-a95f480c2e177b63844af0d09a6eb5bd.png",
                "hlsPlaylist": "{{media_root_url}}Crisis_Stability_Plan_-_Jaspr_Health-d516889d75fd23f91f3e7f53ebeb4e26/index.m3u8",
                "dashPlaylist": "{{media_root_url}}Crisis_Stability_Plan_-_Jaspr_Health-d516889d75fd23f91f3e7f53ebeb4e26/index.mpd",
                "mp4Transcode": "{{media_root_url}}Crisis_Stability_Plan_-_Jaspr_Health-d516889d75fd23f91f3e7f53ebeb4e26/kiosk_720p_Crisis_Stability_Plan_-_Jaspr_Health-d516889d75fd23f91f3e7f53ebeb4e26.mp4"
            }
        ]
    },
{% endif %}

    {
        "uid": "crisisDesc",
        "guide": [
            "You might know this, but the highest urges to harm or kill yourself may last for 24-48 hours, then usually go down or go away. But in some situations, strong urges may come back.",
            "What made your urges to harm yourself go up?"
        ],
        "showIf": [],
        "hideIf": [],
        "provider_label": "When you think about what brought you here today, what made the urges to harm yourself go up?",
        "provider_order": 37,
        "actions": [
            { "type": "text", "label": "", "answerKey": "crisisDesc" },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "getHelp",
        "guide": [
            "It's important to get help with the actual problems that drive feeling suicidal. That can take time."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [{ "type": "buttons", "buttons": [{ "label": "Okay" }] }]
    },
    {
        "uid": "okReady",
        "guide": [
            "I'd like to walk you through some strategies for bearing the pain and surviving painful situations when you can't make things better right away.",
            "That way you can have a plan to survive the worst moments and help you regain stability."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [{ "type": "buttons", "buttons": [{ "label": "Okay, ready" }] }]
    },
    {
        "uid": "comfortAndSkills",
        "guide": [
            "To make the strongest plan, let's find a mix of things that could help when you find yourself in intense painful emotions and situations.",
            "Let's start with the Comfort & Skills videos, activities, and music.",
            "I definitely recommend the Paced Breathing. It's really good in a crisis.",
            "Click on any activity you are interested in to open it. If you like something, click the heart, and I will save it for you."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            { "type": "comfort-skills" },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "sharedStories",
        "guide": ["Now take a look at the Shared Stories. When you put a heart, I'll save it."],
        "showIf": [],
        "hideIf": [],
        "actions": [
            { "type": "shared-stories" },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "viewCard1",
        "guide": [
            "Here's where I've started saving the things you liked. It will print as a card to take with you. Everything will be in the Takeaway Kit for you."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            { "type": "stability-card", "empty": true },
            { "type": "buttons", "buttons": [{ "label": "Okay" }] }
        ]
    },
    {
        "uid": "whenThingsGetHard",
        "guide": [
            "So, when things get hard, one thing to do is watch your Jaspr videos.",
            "Another strategy that helps a lot of people is to directly calm the body."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [{ "type": "buttons", "buttons": [{ "label": "Tell me more about that" }] }]
    },
    {
        "uid": "copingBody",
        "guide": [
            "Here are ways to calm your body chemistry. Select any of what seems good to you or add your own."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "coping-strategy",
                "choices": [
                    "Cold shower",
                    "Hot bath",
                    "Hold ice",
                    "Intense exercise",
                    "Climb stairs",
                    "Squats",
                    "Paced breathing"
                ],
                "answerKey": "copingBody",
                "allowCustom": true
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "copingDistract",
        "guide": [
            "Sometimes it helps to get even a small mental break. What helps you distract?",
            "Could you do an activity that holds your attention and might create positive emotions?"
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "coping-strategy",
                "choices": [
                    "Go for a walk",
                    "Meet a friend",
                    "Go to a place of worship",
                    "Clean my space",
                    "Go to gym",
                    "Go to a library",
                    "Video games",
                    "Call a friend",
                    "Watch an inspiring movie",
                    "Go to a cafe"
                ],
                "answerKey": "copingDistract",
                "allowCustom": true
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "copingHelpOthers",
        "guide": [
            "Could you do something that contributes or that helps someone else as a way to help yourself?"
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "coping-strategy",
                "choices": [
                    "Do something kind",
                    "Give a compliment",
                    "Offer encouragement",
                    "Volunteer",
                    "Clean a shared space",
                    "Help someone",
                    "Make a small gift"
                ],
                "answerKey": "copingHelpOthers",
                "allowCustom": true
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "copingCourage",
        "guide": [
            "Sometimes the best way to cope is to do things to help you find courage to survive and connect to your values."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "coping-strategy",
                "choices": [
                    "Pray",
                    "Call a supportive person",
                    "Encourage myself",
                    "Practice mindfulness"
                ],
                "answerKey": "copingCourage",
                "allowCustom": true
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "copingSenses",
        "guide": [
            "Sometimes in intense pain it can help to offer self-soothing and comfort through the 5 senses of seeing, smelling, hearing, touching, and tasting."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "coping-strategy",
                "choices": [
                    "Look at beautiful images",
                    "Be in nature",
                    "Enjoy a hot drink",
                    "Wear favorite clothing",
                    "Listen to soothing music",
                    "Eat a favorite food",
                    "Use scented soap or lotion",
                    "Light a candle"
                ],
                "answerKey": "copingSenses",
                "allowCustom": true
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "supportivePeople",
        "guide": [
            "If possible, it's good to have a mix that includes people. Are there people who help you feel better when you're upset or who help you take your mind off things?",
            "You don't have to tell the person you're in a crisis - sometimes just talking helps.",
            "You can also add professionals who can help when things are bad."
        ],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Supportive People",
        "provider_order": 39,
        "actions": [
            { "type": "supportive-people", "answerKey": "supportivePeople" },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "copingTop",
        "guide": [
            "Here are your ideas. In a crisis moment, which could you really do? Add the ones that would be the best strategies for you to remember to use."
        ],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Coping Strategies",
        "provider_order": 38,
        "actions": [
            {
                "type": "rank-top",
                "lists": [
                    "copingBody",
                    "copingDistract",
                    "copingHelpOthers",
                    "copingCourage",
                    "copingSenses",
                    "supportivePeople"
                ],
                "labels": ["Body", "Distract", "Help Others", "Courage", "Senses", "*hide*"],
                "answerKey": "copingTop",
                "dropTitle": "Coping Strategies",
                "targetCount": 7
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "viewCard2",
        "guide": [
            "I've pulled all our work together.  I added the national lifeline because you can call or text them. It's confidential. They are 24/7 and really good."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            { "type": "stability-card" },
            { "type": "buttons", "buttons": [{ "label": "Okay" }] }
        ]
    },
    {
        "uid": "reasonsLive",
        "guide": [
            "Reviewing your reasons for living can really help in a crisis. Would you like to update your reasons for living now?"
            {% if not csa_assigned and not reasons_live_answered %}
                ,"Write down what's important. Click done when you're finished."
            {% endif %}
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
        {% if csa_assigned and reasons_live_answered %}
            { "type": "sort-edit", "answerKey": "reasonsLive" },
        {% else %}
            {
                "rows": 5,
                "type": "list",
                "question": "Reasons for living",
                "answerKey": "reasonsLive",
                "maxLength": 10000
            },
        {% endif %}
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {% if not csa_assigned %}
    {
        "uid": "ReasonsLiveRank",
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
    {% endif %}
    {
        "uid": "viewCard3",
        "guide": [
            "Okay, last piece! Like smoke is an early sign of fire, what cues tell you that it's time to put your plan into action?"
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            { "type": "stability-card" },
            { "type": "buttons", "buttons": [{ "label": "Okay" }] }
        ]
    },
    {
        "uid": "warningStressors",
        "guide": [
            "Are there stressors and situations you might face that could increase feeling suicidal? Here's a list of common ones. Add your own too."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "coping-strategy",
                "choices": ["Conflict in relationship", "Conflict with family or friend"],
                "answerKey": "wsStressors",
                "allowCustom": true
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "warningThoughts",
        "guide": [
            "Are there any internal signals that you're getting into a dangerous time?",
            "Are certain thoughts like these a signal for you?"
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "coping-strategy",
                "choices": ["This will never end", "I can't take it anymore"],
                "answerKey": "wsThoughts",
                "allowCustom": true
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "warningFeelings",
        "guide": ["Do any sensations or emotions signal that you're heading into a crisis?"],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "coping-strategy",
                "choices": [
                    "Feeling on edge",
                    "Restless",
                    "Shaking/trembling",
                    "Nausea",
                    "Panicky",
                    "Physical pain",
                    "Guilt",
                    "Anger",
                    "Worry",
                    "Shame",
                    "Sadness"
                ],
                "answerKey": "wsFeelings",
                "allowCustom": true
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "warningActions",
        "guide": [
            "How about actions - things you do that signal you are heading into a suicide crisis?",
            "Here are common ones or add your own."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "coping-strategy",
                "choices": [
                    "Problems sleeping",
                    "Avoiding people",
                    "Pacing",
                    "Harming myself",
                    "Practicing/rehearsing suicide attempt",
                    "Crying",
                    "Yelling/screaming",
                    "Getting ready for suicide attempt"
                ],
                "answerKey": "wsActions",
                "allowCustom": true
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "wsTop",
        "guide": [
            "Of these, which 3 are the best signals that you are in trouble and should use your plan?"
        ],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Warning Signs",
        "provider_order": 40,
        "actions": [
            {
                "type": "rank-top",
                "lists": ["wsStressors", "wsThoughts", "wsFeelings", "wsActions"],
                "labels": ["Stressors", "Thoughts", "Feelings", "Actions"],
                "answerKey": "wsTop",
                "dropTitle": "Warning Signs",
                "targetCount": 3
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "viewCard4",
        "guide": ["Nice work. Look it over."],
        "showIf": [],
        "hideIf": [],
        "actions": [
            { "type": "stability-card" },
            { "type": "buttons", "buttons": [{ "label": "Okay, I've looked it over" }] }
        ]
    },
    {
        "uid": "stabilityRehearsal",
        "guide": [
            "What matters is that you feel confident the things on the plan could help you survive in the worst moment.",
            "Try saying in your own words the main points of your plan.",
            "For example, \"When I see warning signs like (list your top 3 signals), I will _______\" (list the things you will do to protect yourself and survive the crisis)."
        ],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Your plan to survive the worst moments in your own words:",
        "provider_order": 41,
        "actions": [
            { "type": "text", "label": "", "answerKey": "stabilityRehearsal", "maxLength": 10000 },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "stabilityConfidence",
        "guide": ["How confident are you in your ability to use the strategies you selected?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "How confident are you in your ability to use the strategies you selected?",
        "provider_order": 42,
        "actions": [
            {
                "max": 100,
                "min": 0,
                "step": 1,
                "type": "slider",
                "maxLabel": "Very\nconfident",
                "minLabel": "Not at all\nconfident",
                "answerKey": "stabilityConfidence"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "talkItThrough",
        "guide": [
            "Okay, I'll put this in the Summaries.",
            "After you talk this through with your providers, I hope that you could share it with friends or family, if you're willing."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "buttons",
                "buttons": [
                    { "label": "Yes, I'm good with that" },
                    { "label": "No, just provider" }
                ],
                "answerKey": "willingToTalk"
            }
        ]
    },
    {
        "uid": "readiness",
        "guide": [
            "People become ready to leave the emergency room in different ways and for different reasons.",
            "How ready to leave the emergency room are you feeling?"
        ],
        "showIf": [],
        "hideIf": [],
        "provider_label": "How ready to leave the emergency room are you feeling?",
        "provider_order": 43,
        "actions": [
            {
                "type": "buttons",
                "buttons": [
                    { "label": "Not at all ready" },
                    { "label": "Somewhat ready" },
                    { "label": "Very ready" }
                ],
                "answerKey": "readiness"
            }
        ]
    },
    {
        "uid": "readinessNo",
        "guide": ["What would make you feel more ready?"],
        "showIf": [],
        "hideIf": ["readiness", "Very ready"],
        "provider_label": "What would make you feel more ready?",
        "provider_order": 44,
        "actions": [
            { "type": "text", "label": "", "answerKey": "readinessNo", "maxLength": 10000 },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "readinessYesReasons",
        "guide": ["What makes you feel very ready? Check all that apply."],
        "showIf": ["readiness", "Very ready"],
        "hideIf": [],
        "provider_label": "What makes you feel very ready? Check all that apply.",
        "provider_order": 45,
        "actions": [
            {
                "type": "choice",
                "options": [
                    {
                        "label": "I need to take care of my obligations",
                        "value": "I need to take care of my obligations"
                    },
                    { "label": "I feel better and calmer", "value": "I feel better and calmer" },
                    { "label": "I feel ready to cope", "value": "I feel ready to cope" },
                    { "label": "My urge has gone down", "value": "My urge has gone down" },
                    {
                        "label": "This was a misunderstanding",
                        "value": "This was a misunderstanding"
                    },
                    { "label": "I'm frustrated", "value": "I'm frustrated" },
                    {
                        "label": "People who support me understand how serious I am",
                        "value": "People who support me understand how serious I am"
                    },
                    { "label": "My circumstances have changed", "value": "My circumstances have changed" }
                ],
                "multiple": true,
                "vertical": true,
                "answerKey": "readinessYesReasons"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "readinessYesChanged",
        "guide": ["What has changed since you arrived at the emergency room?"],
        "showIf": ["readiness", "Very ready"],
        "hideIf": [],
        "provider_label": "What has changed since you arrived at the emergency room?",
        "provider_order": 46,
        "actions": [
            { "type": "text", "label": "", "answerKey": "readinessYesChanged", "maxLength": 10000 },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "thanksPlanToCope",
        "guide": [
            "Thanks for working through this with me.",
            "You can view your responses anytime in the 'Summaries' section at the bottom of this page."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [{ "type": "buttons", "buttons": [{ "label": "Okay" }] }]
    },
    {
        "uid": "walkThrough",
        "guide": [
            "That way, you can walk through them with your provider, or make edits if you need to."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "buttons",
                "buttons": [{ "label": "Got it" }, { "label": "Sounds good" }],
                "answerKey": "walkThrough"
            }
        ]
    }
]