[
    {
        "uid": "welcome",
        "guide": [
            "Hi, I'm Jaz, an automated assistant.",
            "In times of distress, watching comforting videos or listening to people's stories who may be able to relate can be helpful.",
            "We'd like to share them with you."
        ],
        "actions": [
            {
                "type": "buttons",
                "buttons": [{ "label": "Okay" }]
            }
        ]
    },
    {
        "uid": "setSecurityImage",
        "guide": ["To protect your privacy, let's set a password. First pick a secret image."],
        "actions": [
            {
                "type": "security-image"
            },
            {
                "type": "buttons",
                "validation": true,
                "buttons": [{ "label": "Done" }]
            }
        ]
    },
    {
        "uid": "setSecurityQuestion",
        "guide": ["Now pick a security question and answer."],
        "actions": [
            {
                "type": "security-question"
            },
            {
                "type": "buttons",
                "validation": false,
                "orientation": "horizontal",
                "buttons": [
                    {
                        "label": "Done",
                        "action": "navigate",
                        "path": "/"
                    }
                ]
            }
        ]
    }
]
