[
    {
        "uid": "makeHomeStart",
        "guide": ["I'd like to work with you now on something that might save your life."],
        "actions": [
            {
                "type": "buttons",
                "buttons": [{ "label": "Let's keep going" }]
            }
        ]
    },
    {
        "uid": "desireToHarm",
        "guide": [
            "When people feel extremely upset or hopeless, they sometimes do things they wouldn't usually do.",
            "Sometimes the desire to harm yourself can change and go up very fast."
        ],
        "actions": [
            {
                "type": "buttons",
                "buttons": [{ "label": "Yeah" }]
            }
        ]
    },
    {
        "uid": "skipLethalMeans",
        "guide": [
            "That can make it dangerous to have easy access to things you'd use to harm yourself.",
            "In your situation, might it be good to think through steps you could take to protect yourself during crises?"
        ],
        "actions": [
            {
                "type": "buttons",
                "answerKey": "skipLethalMeans",
                "buttons": [
                    { "label": "Yes, I'll think with you", "goto": ["meansDescribeReview", "meansDescribeReviewEdit"] },
                    { "label": "Skip for now", "goto": ["skipReason"] }
                ]
            }
        ]
    },

    {
        "uid": "skipReason",
        "guide": ["What makes you skip for now, may I ask?"],
        "actions": [
            {
                "type": "buttons",
                "answerKey": "skipReason",
                "buttons": [
                    { "label": "Too tired", "goto": ["reasonTooTired"] },
                    { "label": "Too private", "goto": ["reasonTooPrivate"] },
                    {
                        "label": "I'm worried people will overreact",
                        "goto": ["reasonPeopleWillOverreact"]
                    },
                    {
                        "label": "I'm not sure I want to talk about it",
                        "goto": ["reasonDontWantToTalk"]
                    },
                    { "label": "It's too shameful", "goto": ["lethalMeansTooShameful"] },
                    { "label": "I don't need to do this", "goto": ["lethalMeansDontNeed"] },
                    { "label": "Cannot get rid of means", "goto": ["lethalMeansGetRid"] },
                    { "label": "Not sure I want to be stable", "goto": ["lethalMeansNotStable"] },
                    { "label": "I want to keep my means", "goto": ["lethalMeansWantToKeep"] },
                    {
                        "label": "I'm afraid this will keep me in the hospital",
                        "goto": ["lethalMeansAfraidHospital"]
                    },
                    {
                        "label": "I feel too depressed or overwhelmed",
                        "goto": ["lethalMeansTooDepressed"]
                    }
                ]
            }
        ]
    },
    {
        "uid": "reasonTooTired",
        "showIf": ["skipReason", "Too tired"],
        "guide": [
            "Okay, it's totally fine if you want to rest now. Maybe you could even get a little sleep. I can wait. I'll be ready when you are."
        ],
        "actions": [
            {
                "type": "buttons",
                "buttons": [
                    { "label": "Okay, I'm ready to keep going", "goto": ["meansDescribeReview"] }
                ]
            }
        ]
    },
    {
        "uid": "reasonTooPrivate",
        "showIf": ["skipReason", "Too private"],
        "guide": [
            "I understand wanting to be private.",
            "I know your providers will ask you about steps you'd be willing to take to protect yourself during a crisis.",
            "It might be helpful if you and me prepared a little, so you know what you are and are not willing to do.",
            "I wonder if this is a time it might be good to work together even if it's a little uncomfortable?",
            "It might help to share what's truly troubling you. But of course, it's important you decide what's right for you."
        ],
        "actions": [
            {
                "type": "buttons",
                "answerKey": "tooPrivateDec",
                "buttons": [
                    { "label": "Yes, I'll think with you", "goto": ["meansDescribeReview"] },
                    { "label": "Skip for now", "goto": ["crisisDesc"] }
                ]
            }
        ]
    },
    {
        "uid": "reasonPeopleWillOverreact",
        "showIf": ["skipReason", "I'm worried people will overreact"],
        "guide": [
            "Yes, I know what you mean. Is there something specific you're afraid will happen?"
        ],
        "actions": [
            {
                "type": "buttons",
                "answerKey": "overreactSpecific",
                "buttons": [
                    {
                        "label": "Take away means",
                        "goto": ["reasonPeopleWillOverreactTakeAwayMeans"]
                    },
                    {
                        "label": "Keep me in hospital against my will",
                        "goto": ["reasonPeopleWillOverreactKeepAgainstWill"]
                    }
                ]
            }
        ]
    },
    {
        "uid": "reasonPeopleWillOverreactTakeAwayMeans",
        "showIf": ["overreactSpecific", "Take away means"],
        "guide": [
            "It's really normal to feel mixed about this. This is a common enough experience that actually I have a video about this topic in case you want to take a look.",
            "Talking about means can be hard. If it helps, remember that these changes are not necessarily permanent. It's just a plan for how to protect yourself during times of intense emotion. Would you be willing to continue?"
        ],
        "actions": [
            {
                "type": "buttons",
                "answerKey": "overreactTakeAwayDec",
                "buttons": [
                    { "label": "Yes, I'll think with you", "goto": ["meansDescribeReview"] },
                    { "label": "Skip for now" }
                ]
            }
        ]
    },

    {
        "uid": "reasonPeopleWillOverreactTakeAwayMeansSkip",
        "showIf": ["overreactTakeAwayDec", "Skip for now"],
        "guide": ["Okay, I understand. Maybe you can talk to your provider about this later."],
        "actions": [
            {
                "type": "buttons",
                "buttons": [{ "label": "I'll consider that", "goto": ["crisisDesc"] }]
            }
        ]
    },

    {
        "uid": "reasonPeopleWillOverreactKeepAgainstWill",
        "showIf": ["overreactSpecific", "Keep me in hospital against my will"],
        "guide": [
            "I understand that worry. The best way to make sure you have a say in what happens next is to be clear about what actions you are and are not willing to take to protect yourself.",
            "If we go through some of the ideas that have worked for other people, you may spot some things that would work for you.",
            "Would you be willing to look at some ideas that might fit your situation?"
        ],
        "actions": [
            {
                "type": "buttons",
                "answerKey": "overreactKeepMeDec",
                "buttons": [
                    { "label": "Yes, I'll think with you", "goto": ["meansDescribeReview"] },
                    { "label": "Skip for now" }
                ]
            }
        ]
    },

    {
        "uid": "reasonPeopleWillOverreactKeepAgainstWillSkip",
        "showIf": ["overreactKeepMeDec", "Skip for now"],
        "guide": ["Okay, I understand. Maybe you can talk to your provider about this later."],
        "actions": [
            {
                "type": "buttons",
                "buttons": [{ "label": "I'll consider that", "goto": ["crisisDesc"] }]
            }
        ]
    },

    {
        "uid": "reasonDontWantToTalk",
        "showIf": ["skipReason", "I'm not sure I want to talk about it"],
        "guide": ["Okay. What do you worry will happen if you talk about it?"],
        "actions": [
            {
                "type": "buttons",
                "answerKey": "reasonNotSureTalk",
                "buttons": [
                    { "label": "I'll be forced to do something I don't want to do" },
                    { "label": "I'm undecided if I want to kill myself" },
                    { "label": "I want to kill myself and don't want to be blocked" },
                    { "label": "I don't want my answers about this recorded" },
                    { "label": "I'm mixed about reducing access" },
                    { "label": "Having access is comforting - I have a way out" }
                ]
            }
        ]
    },

    {
        "uid": "reasonDontWantToTalkAll",
        "showIf": ["skipReason", "I'm not sure I want to talk about it"],
        "guide": [
            "It's totally normal to feel mixed. We can look at ideas together without you committing to do any of them.",
            "These ideas are things that other people in your situation had said are helpful.",
            "We could start the process and you can see how you feel.",
            "Would you be willing to look at some ideas that might fit your situation?"
        ],
        "actions": [
            {
                "type": "buttons",
                "answerKey": "notSureTalkDec",
                "buttons": [
                    { "label": "Yes, I'll think with you", "goto": ["meansDescribeReview"] },
                    { "label": "Skip for now" }
                ]
            }
        ]
    },

    {
        "uid": "reasonDontWantToTalkAllSkip",
        "showIf": ["notSureTalkDec", "Skip for now"],
        "guide": ["Okay, I understand. Maybe you can talk to your provider about this later."],
        "actions": [
            {
                "type": "buttons",
                "buttons": [{ "label": "I'll consider that", "goto": ["crisisDesc"] }]
            }
        ]
    },

    {
        "uid": "lethalMeansTooShameful",
        "showIf": ["skipReason", "It's too shameful"],
        "guide": [
            "Almost everybody wants to feel like they can do things on their own. It can feel humiliating to have other people know what's going on. As hard as it might be, would you consider allowing me to think with you about steps to protect your life?",
            "Are you willing to start this section and see how it goes?",
            "It can be really helpful to think about this as taking control of the things that will hurt you ultimately. And that's something you can take pride in."
        ],
        "actions": [
            {
                "type": "buttons",
                "answerKey": "tooShamefulDec",
                "buttons": [
                    { "label": "Yes, I'll think with you", "goto": ["meansDescribeReview"] },
                    { "label": "Skip for now", "goto": ["crisisDesc"] }
                ]
            }
        ]
    },
    {
        "uid": "lethalMeansDontNeed",
        "showIf": ["skipReason", "I don't need to do this"],
        "guide": [
            "You may well be able to do this on your own. When you're in a lot of pain, however, it's easy to slip away from your best judgment. Because of this, it's really important to have a plan around means. You just never know when you're in the moment. Are you willing to start this section and see how it goes?"
        ],
        "actions": [
            {
                "type": "buttons",
                "answerKey": "doNotNeedDec",
                "buttons": [
                    { "label": "Yes, I'll think with you", "goto": ["meansDescribeReview"] },
                    { "label": "Skip for now", "goto": ["crisisDesc"] }
                ]
            }
        ]
    },
    {
        "uid": "lethalMeansGetRid",
        "showIf": ["skipReason", "Cannot get rid of means"],
        "guide": [
            "There are definitely situations where you can't completely remove access to means. I have a few ideas about how to protect yourself, even in that situation, that you can look at.",
            "Are you willing to start this section and see how it goes?"
        ],
        "actions": [
            {
                "type": "buttons",
                "answerKey": "cannotRidMeansDec",
                "buttons": [
                    { "label": "Yes, I'll think with you", "goto": ["meansDescribeReview"] },
                    { "label": "Skip for now", "goto": ["crisisDesc"] }
                ]
            }
        ]
    },
    {
        "uid": "lethalMeansNotStable",
        "showIf": ["skipReason", "Not sure I want to be stable"],
        "guide": [
            "I understand.",
            "A lot goes into deciding to stay alive. At this point, maybe we can look at ideas together, without you having to commit to anything?"
        ],
        "actions": [
            {
                "type": "buttons",
                "answerKey": "stableDec",
                "buttons": [
                    { "label": "Yes, I'll think with you", "goto": ["meansDescribeReview"] },
                    { "label": "Skip for now", "goto": ["crisisDesc"] }
                ]
            }
        ]
    },
    {
        "uid": "lethalMeansWantToKeep",
        "showIf": ["skipReason", "I want to keep my means"],
        "guide": [
            "Right. Many people feel more comfortable keeping access to means.",
            "The thing about overwhelming urges to hurt yourself is they come on really quickly. People can feel impulsive when those urges hit. Maybe we could look at ways where you make your means less easy to access, just to protect yourself through this crisis?",
            "Are you willing to start this section and see how it goes?"
        ],
        "actions": [
            {
                "type": "buttons",
                "answerKey": "keepMeansDec",
                "buttons": [
                    { "label": "Yes, I'll think with you", "goto": ["meansDescribeReview"] },
                    { "label": "Skip for now", "goto": ["crisisDesc"] }
                ]
            }
        ]
    },
    {
        "uid": "lethalMeansAfraidHospital",
        "showIf": ["skipReason", "I'm afraid this will keep me in the hospital"],
        "guide": [
            "I understand this fear. I can't say how long you'll stay in the hospital. However, not having a plan for reducing access to means can increase the risk of being hospitalized. Providers often feel more comfortable letting you go home knowing you have a realistic plan to protect yourself.",
            "Are you willing to start this section and see how it goes?"
        ],
        "actions": [
            {
                "type": "buttons",
                "answerKey": "keepInHospitalDec",
                "buttons": [
                    { "label": "Yes, I'll think with you", "goto": ["meansDescribeReview"] },
                    { "label": "Skip for now", "goto": ["crisisDesc"] }
                ]
            }
        ]
    },
    {
        "uid": "lethalMeansTooDepressed",
        "showIf": ["skipReason", "I feel too depressed or overwhelmed"],
        "guide": [
            "I'm really glad you decided to come here and get help. What you're going through is hard.",
            "We can do small parts together - you can take a break and go at your own pace.",
            "Are you willing to start and see how it goes?"
        ],
        "actions": [
            {
                "type": "buttons",
                "answerKey": "feelDepressedDec",
                "buttons": [
                    { "label": "Yes, I'll think with you", "goto": ["meansDescribeReview"] },
                    { "label": "Skip for now", "goto": ["crisisDesc", "assessmentLock"] }
                ]
            }
        ]
    },
    {
        "uid": "sectionChangeMakingHomeSafe",
        "guide": [],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Make Home Safer",
        "provider_order": 33,
        "actions": [
            {
                "type": "section-change",
                "label": "Make Home Safer",
                "section": "csp"
            }
        ]
    },

    {% if not means_yes_no_answered %}

    {
        "uid": "meansDescribeReview",
        "guide": [],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "question": "Do you have access to the means to take your life?",
                "subtitle": "(e.g. stash of pills, guns, or any other method)",
                "answerKey": "meansYesNo"
            },
            { "type": "text", "label": "Describe:", "answerKey": "meansYesNoDescribe" },
            { "type": "buttons", "buttons": [{ "label": "Next" }] }
        ]
    },

    {% else %}
    {
        "uid": "meansDescribeReviewEdit",
        "guide": ["Here is what you told me so far. You can add more details, if you like."],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "question": "Do you have access to the means to take your life?",
                "subtitle": "(e.g. stash of pills, guns, or any other method)",
                "answerKey": "meansYesNo"
            },
            { "type": "text", "label": "Describe:", "answerKey": "meansYesNoDescribe" },
            { "type": "buttons", "buttons": [{ "label": "Next" }] }
        ]
    },

    {% endif %}
    
    {
        "uid": "considerReducingAccess",
        "guide": [
            "For some people it's difficult to consider reducing easy access to things you'd use to harm yourself. Access can be comforting.",
            "But removing or reducing easy access to lethal means is the most important step you can take to save your life."
        ],
        "actions": [
            {
                "type": "buttons",
                "buttons": [{ "label": "Okay, I'll think about steps I could take" }]
            }
        ]
    },
    {
        "uid": "strategiesGeneral",
        "guide": [
            "Here are ways other people have used to protect themselves during a crisis. Can you pick strategies that might work for you?"
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Dispose of method", "value": "Dispose of method" },
                    { "label": "Store with trusted person", "value": "Store with trusted person" },
                    {
                        "label": "Store in a lock box, give key to a trusted person",
                        "value": "Store in a lock box, give key to a trusted person"
                    },
                    {
                        "label": "Plan how to avoid the method (i.e. not go to dangerous location)",
                        "value": "Plan how to avoid the method (i.e. not go to dangerous location)"
                    }
                ],
                "multiple": true,
                "vertical": true,
                "answerKey": "strategiesGeneral"
            },
            { "type": "buttons", "buttons": [{ "label": "Next" }] }
        ]
    },
    {
        "uid": "additionalStrategies",
        "guide": [
            "It might help to think in detail - would any of these ideas fit your situation?"
        ],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Selected strategies to protect yourself during a crisis (lethal means safety):",
        "provider_order": 34,
        "actions": [
            {
                "type": "tab-choice",
                "groups": [
                    {
                        "label": "Firearm",
                        "options": [
                            {
                                "label": "Family, friend, or neighbor",
                                "value": "Family, friend, or neighbor"
                            },
                            { "label": "Gun dealers", "value": "Gun dealers" },
                            { "label": "Shooting range", "value": "Shooting range" },
                            {
                                "label": "Commercial storage facility",
                                "value": "Commercial storage facility"
                            },
                            { "label": "Pawn shop", "value": "Pawn shop" },
                            { "label": "Police/sheriff", "value": "Police/sheriff" },
                            { "label": "Lock box", "value": "Lock box" },
                            { "label": "Gun safe", "value": "Gun safe" },
                            { "label": "Locking device", "value": "Locking device" },
                            { "label": "Disassemble ", "value": "Disassemble " }
                        ],
                        "answerKey": "strategiesFirearm"
                    },
                    {
                        "label": "Medicine",
                        "options": [
                            { "label": "Disposal", "value": "Disposal" },
                            { "label": "Locked up at home", "value": "Locked up at home" },
                            {
                                "label": "Stored with a trusted person",
                                "value": "Stored with a trusted person"
                            }
                        ],
                        "answerKey": "strategiesMedicine"
                    },
                    {
                        "label": "Dangerous Places",
                        "options": [{ "label": "Avoid location", "value": "Avoid location" }],
                        "answerKey": "strategiesPlaces"
                    },
                    {
                        "label": "Other Hazards",
                        "options": [
                            {
                                "label": "Limit access when and where it is possible",
                                "value": "Limit access when and where it is possible"
                            },
                            {
                                "label": "Have list of emergency response and lifelines available",
                                "value": "Have list of emergency response and lifelines available"
                            }
                        ],
                        "answerKey": "strategiesOther"
                    }
                ]
            },
            { "type": "buttons", "buttons": [{ "label": "Next" }] }
        ]
    },
    {
        "uid": "meansCustom",
        "guide": [
            "Okay, here are the ideas you picked.",
            "This is a possible plan to talk over with your provider.",
            "How does it look? You can add more ideas if you want."
        ],
        "showIf": [],
        "hideIf": [],
        "actions": [
            {
                "type": "means-custom",
                "answerKey": "strategiesCustom",
                "reviewKeys": [
                    { "label": "General", "answerKey": "strategiesGeneral" },
                    { "label": "Firearm", "answerKey": "strategiesFirearm" },
                    { "label": "Medicine", "answerKey": "strategiesMedicine" },
                    { "label": "Dangerous Places", "answerKey": "strategiesPlaces" },
                    { "label": "Other Hazards", "answerKey": "strategiesOther" }
                ]
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "meansSupport",
        "guide": ["In your situation, can someone help you take these steps?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "Can someone help you take these steps?",
        "provider_order": 35,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Yes", "value": true },
                    { "label": "No", "value": false }
                ],
                "answerKey": "meansSupportYesNo"
            },
            { "type": "text", "label": "Who:", "answerKey": "meansSupportWho" },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    {
        "uid": "meansWilling",
        "guide": ["How willing are you to secure your means with the steps you just identified?"],
        "showIf": [],
        "hideIf": [],
        "provider_label": "How willing are you to secure your means with the steps you identified?",
        "provider_order": 36,
        "actions": [
            {
                "type": "choice",
                "options": [
                    { "label": "Not willing", "value": "Not willing" },
                    { "label": "Mixed/Unsure", "value": "Mixed/Unsure" },
                    { "label": "Very willing", "value": "Very willing" }
                ],
                "answerKey": "meansWilling"
            },
            { "type": "buttons", "buttons": [{ "label": "Done" }] }
        ]
    },
    
    {
        "uid": "thankYouMeans",
        "guide": ["I appreciate that you thought about it with me. It can be a hard topic."],
        "showIf": [],
        "hideIf": [],
        "actions": [{ "type": "buttons", "buttons": [{ "label": "Done" }] }]
    }
]