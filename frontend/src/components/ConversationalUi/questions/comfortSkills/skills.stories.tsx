import { ComponentStory, ComponentMeta } from '@storybook/react';
import ComfortSkills from '.';

export default {
    title: 'ConversationalUi/ComfortSkills',
    component: ComfortSkills,
    argTypes: {},
} as ComponentMeta<typeof ComfortSkills>;

const Template: ComponentStory<typeof ComfortSkills> = (args) => {
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
            }}
        >
            <ComfortSkills />
        </div>
    );
};

export const Default = Template.bind({});

Default.parameters = {
    initialState: {
        ...Default.parameters,
        skills: [
            {
                id: 4,
                name: 'Crackling Fireplace',
                video: {
                    id: 17,
                    name: 'Crackling Fireplace',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/fireplace.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/fireplacePoster.png',
                    thumbnail: null,
                    fpm4Transcode: 'https://media.jaspr-development.com/fireplace/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/fireplace/jaspr_720p_fireplace.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist: 'https://media.jaspr-development.com/fireplace/index.m3u8',
                    dashPlaylist: 'https://media.jaspr-development.com/fireplace/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/fireplace2x.jpg',
                targetUrl: '',
                labelColor: '#ae4a2e',
                order: 3,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 2,
                name: 'Puppies',
                video: {
                    id: 18,
                    name: 'Puppies',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/puppies.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/puppiesPOster.png',
                    thumbnail: null,
                    fpm4Transcode: 'https://media.jaspr-development.com/puppies/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/puppies/jaspr_720p_puppies.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist: 'https://media.jaspr-development.com/puppies/index.m3u8',
                    dashPlaylist: 'https://media.jaspr-development.com/puppies/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/puppies2x.jpg',
                targetUrl: '',
                labelColor: '#442b1a',
                order: 5,
                patientActivity: 1,
                rating: null,
                saveForLater: true,
                viewed: null,
            },
            {
                id: 8,
                name: 'Distract: Name Things',
                video: {
                    id: 24,
                    name: 'Distract: Name Things',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Topher_-_Skills_-_Naming_Things.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Topher_-_Skills_-_Naming_Things/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Topher_-_Skills_-_Naming_Things/jaspr_720p_Topher_-_Skills_-_Naming_Things.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Topher_-_Skills_-_Naming_Things/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Topher_-_Skills_-_Naming_Things/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/Distract-_Name_Things2x.jpg',
                targetUrl: '',
                labelColor: '#214d46',
                order: 7,
                patientActivity: 4,
                rating: null,
                saveForLater: true,
                viewed: null,
            },
            {
                id: 9,
                name: 'Distract: Survey the Room',
                video: {
                    id: 23,
                    name: 'Distract: Survey the Room',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/PLE-G5-R12_Kelechi_-_Skill_-_Mindfullness_survey_room.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/distract_surveyTheRoomPoster.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/PLE-G5-R12_Kelechi_-_Skill_-_Mindfullness_survey_room/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/PLE-G5-R12_Kelechi_-_Skill_-_Mindfullness_survey_room/jaspr_720p_PLE-G5-R12_Kelechi_-_Skill_-_Mindfullness_survey_room.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/PLE-G5-R12_Kelechi_-_Skill_-_Mindfullness_survey_room/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/PLE-G5-R12_Kelechi_-_Skill_-_Mindfullness_survey_room/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage:
                    'https://media.jaspr-development.com/Distract-_Survey_the_Room2x.jpg',
                targetUrl: '',
                labelColor: '#262121',
                order: 6,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 11,
                name: 'Inside Outside for Difficult Moments',
                video: {
                    id: 25,
                    name: 'Inside Outside for Difficult Moments',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Charles_-_Skills_-_Inside_Outside.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Charles_-_Skills_-_Inside_Outside/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Charles_-_Skills_-_Inside_Outside/jaspr_720p_Charles_-_Skills_-_Inside_Outside.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Charles_-_Skills_-_Inside_Outside/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Charles_-_Skills_-_Inside_Outside/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage:
                    'https://media.jaspr-development.com/insideOutsideForDifficultMoments2x.jpg',
                targetUrl: '',
                labelColor: '#ab0000',
                order: 8,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 14,
                name: 'Mindfulness of the Senses for Distress',
                video: {
                    id: 26,
                    name: 'Mindfulness of the Senses for Distress',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/PLE-G5-R20_Diana_-_Skills_-_Mindfulness_in_ED_with_Sensesv2.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster:
                        'https://media.jaspr-development.com/mindfulnessOfTheSensesForDistress_poster.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/PLE-G5-R20_Diana_-_Skills_-_Mindfulness_in_ED_with_Sensesv2/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/PLE-G5-R20_Diana_-_Skills_-_Mindfulness_in_ED_with_Sensesv2/jaspr_720p_PLE-G5-R20_Diana_-_Skills_-_Mindfulness_in_ED_with_Sensesv2.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/PLE-G5-R20_Diana_-_Skills_-_Mindfulness_in_ED_with_Sensesv2/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/PLE-G5-R20_Diana_-_Skills_-_Mindfulness_in_ED_with_Sensesv2/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage:
                    'https://media.jaspr-development.com/mindfulnessOfTheSensesOfDistress2x.jpg',
                targetUrl: '',
                labelColor: '#7200da',
                order: 9,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 12,
                name: 'Leaning on People You Trust',
                video: {
                    id: 27,
                    name: 'Leaning on People You Trust',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Beth_-_Skills_-_Leaning_on_People_you_Trust.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Beth_-_Skills_-_Leaning_on_People_you_Trust/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Beth_-_Skills_-_Leaning_on_People_you_Trust/jaspr_720p_Beth_-_Skills_-_Leaning_on_People_you_Trust.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Beth_-_Skills_-_Leaning_on_People_you_Trust/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Beth_-_Skills_-_Leaning_on_People_you_Trust/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/leaningOnPeopleYouTrust2x.jpg',
                targetUrl: '',
                labelColor: '#7e6663',
                order: 10,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 10,
                name: 'Getting Through Hardest Moments - Topher',
                video: {
                    id: 28,
                    name: 'Getting Through Hardest Moments - Topher',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Topher_-_Skills_-_Getting_Through_Hardest_Moments.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster:
                        'https://media.jaspr-development.com/gettingThroughHardestMoments_poster.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Topher_-_Skills_-_Getting_Through_Hardest_Moments/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Topher_-_Skills_-_Getting_Through_Hardest_Moments/jaspr_720p_Topher_-_Skills_-_Getting_Through_Hardest_Moments.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Topher_-_Skills_-_Getting_Through_Hardest_Moments/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Topher_-_Skills_-_Getting_Through_Hardest_Moments/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage:
                    'https://media.jaspr-development.com/gettingThroughHardestMomentsSkillfully2x.jpg',
                targetUrl: '',
                labelColor: '#2e3137',
                order: 11,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 5,
                name: 'Ocean Life',
                video: {
                    id: 16,
                    name: 'Ocean Life',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/sea_creatures.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/oceanLifePoster.png',
                    thumbnail: null,
                    fpm4Transcode: 'https://media.jaspr-development.com/sea_creatures/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/sea_creatures/jaspr_720p_sea_creatures.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist: 'https://media.jaspr-development.com/sea_creatures/index.m3u8',
                    dashPlaylist: 'https://media.jaspr-development.com/sea_creatures/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/aquarium2x.jpg',
                targetUrl: '',
                labelColor: '#3b480d',
                order: 0,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 24,
                name: 'Opposite Action: Changing Emotions',
                video: {
                    id: 29,
                    name: 'Opposite Action: Changing Emotions',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Opposite_Action_-_Marsha.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster:
                        'https://media.jaspr-development.com/OppositeActionchangeingEmotions_poster.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Opposite_Action_-_Marsha/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Opposite_Action_-_Marsha/jaspr_720p_Opposite_Action_-_Marsha.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Opposite_Action_-_Marsha/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Opposite_Action_-_Marsha/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/hiEmmaTest1.jpg',
                targetUrl: '',
                labelColor: '#374054',
                order: 14,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 25,
                name: 'Thought Replacement Skill',
                video: {
                    id: 30,
                    name: 'Thought Replacement Skill',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/PLE-G5-R13_Charles_-_Skill_-_Thought_Replacement.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster:
                        'https://media.jaspr-development.com/thoughtReplacementSkill_poster.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/PLE-G5-R13_Charles_-_Skill_-_Thought_Replacement/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/PLE-G5-R13_Charles_-_Skill_-_Thought_Replacement/jaspr_720p_PLE-G5-R13_Charles_-_Skill_-_Thought_Replacement.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/PLE-G5-R13_Charles_-_Skill_-_Thought_Replacement/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/PLE-G5-R13_Charles_-_Skill_-_Thought_Replacement/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/thoughReplacementSkill2x.jpg',
                targetUrl: '',
                labelColor: '#2a2a2a',
                order: 16,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 22,
                name: 'Mindfulness Part 1: What and How',
                video: {
                    id: 31,
                    name: 'Mindfulness: What and How (1 of 8)',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Mindfulness_Part_1__What_and_How_Skills.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/mindfulness1_poster.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Mindfulness_Part_1__What_and_How_Skills/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Mindfulness_Part_1__What_and_How_Skills/jaspr_720p_Mindfulness_Part_1__What_and_How_Skills.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Mindfulness_Part_1__What_and_How_Skills/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Mindfulness_Part_1__What_and_How_Skills/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/mindfulness.whatAndHow2x.jpg',
                targetUrl: '',
                labelColor: '#302220',
                order: 17,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 15,
                name: 'Mindfulness Part 2: Observe',
                video: {
                    id: 32,
                    name: 'Mindfulness: Observe (2 of 8)',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Mindfulness_Part_2__WHAT_Observe_.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/mindfulness2_poster.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Mindfulness_Part_2__WHAT_Observe_/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Mindfulness_Part_2__WHAT_Observe_/jaspr_720p_Mindfulness_Part_2__WHAT_Observe_.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Mindfulness_Part_2__WHAT_Observe_/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Mindfulness_Part_2__WHAT_Observe_/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/mindfulness.observe2.82x.jpg',
                targetUrl: '',
                labelColor: '#195d6f',
                order: 18,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 16,
                name: 'Mindfulness Part 3: Describe',
                video: {
                    id: 33,
                    name: 'Mindfulness: Describe (3 of 8)',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Mindfulness_Part_3__WHAT_Describe.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/mindfulness3_poster.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Mindfulness_Part_3__WHAT_Describe/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Mindfulness_Part_3__WHAT_Describe/jaspr_720p_Mindfulness_Part_3__WHAT_Describe.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Mindfulness_Part_3__WHAT_Describe/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Mindfulness_Part_3__WHAT_Describe/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/mindfulness-3of82x.jpg',
                targetUrl: '',
                labelColor: '#032e34',
                order: 19,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 20,
                name: 'Mindfulness Part 4: Participate',
                video: {
                    id: 34,
                    name: 'Mindfulness: Participate (4 of 8)',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Mindfulness_Part_4__WHAT_Participate_1.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/mindfulness4_poster.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Mindfulness_Part_4__WHAT_Participate_1/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Mindfulness_Part_4__WHAT_Participate_1/jaspr_720p_Mindfulness_Part_4__WHAT_Participate_1.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Mindfulness_Part_4__WHAT_Participate_1/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Mindfulness_Part_4__WHAT_Participate_1/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage:
                    'https://media.jaspr-development.com/mindfulness.participate4.82x.jpg',
                targetUrl: '',
                labelColor: '#000000',
                order: 20,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 17,
                name: 'Mindfulness Part 5: Effectiveness',
                video: {
                    id: 35,
                    name: 'Mindfulness: Effectiveness (5 of 8)',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Mindfulness_Part_5__HOW_Effectively_1.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/mindfulness5_poster.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Mindfulness_Part_5__HOW_Effectively_1/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Mindfulness_Part_5__HOW_Effectively_1/jaspr_720p_Mindfulness_Part_5__HOW_Effectively_1.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Mindfulness_Part_5__HOW_Effectively_1/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Mindfulness_Part_5__HOW_Effectively_1/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage:
                    'https://media.jaspr-development.com/mindfulness.effectiveness5.82x.jpg',
                targetUrl: '',
                labelColor: '#1c1c1c',
                order: 21,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 18,
                name: 'Mindfulness Part 6: Nonjudgementally',
                video: {
                    id: 36,
                    name: 'Mindfulness: Nonjudgmentally (6 of 8)',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Mindfulness_Part_6__HOW_Nonjudgmentally_1.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/mindfulness6_poster.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Mindfulness_Part_6__HOW_Nonjudgmentally_1/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Mindfulness_Part_6__HOW_Nonjudgmentally_1/jaspr_720p_Mindfulness_Part_6__HOW_Nonjudgmentally_1.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Mindfulness_Part_6__HOW_Nonjudgmentally_1/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Mindfulness_Part_6__HOW_Nonjudgmentally_1/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage:
                    'https://media.jaspr-development.com/mindfulness.nonjudgementally6.82x.jpg',
                targetUrl: '',
                labelColor: '#45344b',
                order: 22,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 19,
                name: 'Mindfulness Part 7: One-Mindfully',
                video: {
                    id: 37,
                    name: 'Mindfulness: One-Mindfully (7 of 8)',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Mindfulness_Part_7___HOW_One_Mindfully_1.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/mindfulness7_poster.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Mindfulness_Part_7___HOW_One_Mindfully_1/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Mindfulness_Part_7___HOW_One_Mindfully_1/jaspr_720p_Mindfulness_Part_7___HOW_One_Mindfully_1.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Mindfulness_Part_7___HOW_One_Mindfully_1/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Mindfulness_Part_7___HOW_One_Mindfully_1/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/minfulness.oneMindfully2x.jpg',
                targetUrl: '',
                labelColor: '#002534',
                order: 23,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 21,
                name: 'Mindfulness Part 8: Practice Together',
                video: {
                    id: 38,
                    name: 'Mindfulness: Practice Together (8 of 8)',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Mindfulness_Part_8__WHAT_Practicing_Together.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/mindfulness8_poster.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Mindfulness_Part_8__WHAT_Practicing_Together/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Mindfulness_Part_8__WHAT_Practicing_Together/jaspr_720p_Mindfulness_Part_8__WHAT_Practicing_Together.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Mindfulness_Part_8__WHAT_Practicing_Together/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Mindfulness_Part_8__WHAT_Practicing_Together/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage:
                    'https://media.jaspr-development.com/mindfulness.practiceTogether8.82x.jpg',
                targetUrl: '',
                labelColor: '#5a4839',
                order: 24,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 13,
                name: 'Mindfulness of Current Emotion',
                video: {
                    id: 39,
                    name: 'Mindfulness of Current Emotion',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/NMN_-_Mindfulness_of_Current_Emotion_-_Marsha.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster:
                        'https://media.jaspr-development.com/mindfulnessOfCurrentEmotion_poster.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/NMN_-_Mindfulness_of_Current_Emotion_-_Marsha/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/NMN_-_Mindfulness_of_Current_Emotion_-_Marsha/jaspr_720p_NMN_-_Mindfulness_of_Current_Emotion_-_Marsha.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/NMN_-_Mindfulness_of_Current_Emotion_-_Marsha/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/NMN_-_Mindfulness_of_Current_Emotion_-_Marsha/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage:
                    'https://media.jaspr-development.com/mindfulnessOfCurrentEmotion_thumbnail2x.jpg',
                targetUrl: '',
                labelColor: '#527689',
                order: 25,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 23,
                name: 'Opposite Action in Use',
                video: {
                    id: 40,
                    name: 'Opposite Action in Use',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/PLE-G5-R19_Diana-_Skills_-_Opposite_Action_v2.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/oppositeActionInUse_poster.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/PLE-G5-R19_Diana-_Skills_-_Opposite_Action_v2/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/PLE-G5-R19_Diana-_Skills_-_Opposite_Action_v2/jaspr_720p_PLE-G5-R19_Diana-_Skills_-_Opposite_Action_v2.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/PLE-G5-R19_Diana-_Skills_-_Opposite_Action_v2/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/PLE-G5-R19_Diana-_Skills_-_Opposite_Action_v2/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/oppositeActionInUse2x.jpg',
                targetUrl: '',
                labelColor: '#2e1c0d',
                order: 15,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 3,
                name: 'Relaxing Music',
                video: {
                    id: 165,
                    name: 'Relaxing Music Video',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Relaxing_Music_Video.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/relaxingMusicPOster.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Relaxing_Music_Video/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Relaxing_Music_Video/jaspr_720p_Relaxing_Music_Video.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Relaxing_Music_Video/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Relaxing_Music_Video/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/relaxingMusic2x.jpg',
                targetUrl: '',
                labelColor: '#1f5a87',
                order: 4,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 6,
                name: 'Good Vibes Music',
                video: {
                    id: 166,
                    name: 'Good Vibes Music Video',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Good_Vibes_Music_Video.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/feelGoodPOster.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Good_Vibes_Music_Video/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Good_Vibes_Music_Video/jaspr_720p_Good_Vibes_Music_Video.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Good_Vibes_Music_Video/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Good_Vibes_Music_Video/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/goodVibes2x.jpg',
                targetUrl: '',
                labelColor: '#262121',
                order: 2,
                patientActivity: 3,
                rating: null,
                saveForLater: true,
                viewed: null,
            },
            {
                id: 26,
                name: 'Getting Through Hardest Moments - Emmy',
                video: {
                    id: 183,
                    name: 'Getting Through Hardest Moments - Emmy',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Emmy_-_Coping_with_Hardest_Moments.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Emmy_-_Coping_with_Hardest_Moments/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Emmy_-_Coping_with_Hardest_Moments/jaspr_720p_Emmy_-_Coping_with_Hardest_Moments.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Emmy_-_Coping_with_Hardest_Moments/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Emmy_-_Coping_with_Hardest_Moments/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage:
                    'https://media.jaspr-development.com/gettingThroughHardest-Emmy2x.jpg',
                targetUrl: '',
                labelColor: '#2c4069',
                order: 13,
                patientActivity: 2,
                rating: null,
                saveForLater: true,
                viewed: null,
            },
            {
                id: 27,
                name: 'Getting Through Hardest Moments - Thai',
                video: {
                    id: 184,
                    name: 'Getting Through Hardest Moments - Thai',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Thai_-_Skills_-_Hardest_Moments.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Thai_-_Skills_-_Hardest_Moments/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Thai_-_Skills_-_Hardest_Moments/jaspr_720p_Thai_-_Skills_-_Hardest_Moments.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Thai_-_Skills_-_Hardest_Moments/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Thai_-_Skills_-_Hardest_Moments/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: 'https://media.jaspr-development.com/gettingThroughHardest-Thai.png',
                thumbnailImage:
                    'https://media.jaspr-development.com/gettingThroughHardest-Thai2x.jpg',
                targetUrl: '',
                labelColor: '#363e36',
                order: 12,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 28,
                name: "Loved Ones: You're Not Alone",
                video: {
                    id: 188,
                    name: "Loved Ones: You're Not Alone",
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Huynh_-_You_are_Not_Alone.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/notAlone.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Huynh_-_You_are_Not_Alone/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Huynh_-_You_are_Not_Alone/jaspr_720p_Huynh_-_You_are_Not_Alone.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Huynh_-_You_are_Not_Alone/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Huynh_-_You_are_Not_Alone/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/youNotAlone2x.jpg',
                targetUrl: '',
                labelColor: '#66332b',
                order: 26,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 29,
                name: 'Loved Ones: Helping the Care Team',
                video: {
                    id: 189,
                    name: 'Loved Ones: Helping the Care Team',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Huynh_-_We_Need_Your_Insight.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/helpingCareTeam.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Huynh_-_We_Need_Your_Insight/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Huynh_-_We_Need_Your_Insight/jaspr_720p_Huynh_-_We_Need_Your_Insight.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Huynh_-_We_Need_Your_Insight/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Huynh_-_We_Need_Your_Insight/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage:
                    'https://media.jaspr-development.com/helpingCareTeam_thumbnail2x.jpg',
                targetUrl: '',
                labelColor: '#595f61',
                order: 27,
                saveForLater: false,
                patientActivity: null,
            },
            {
                id: 31,
                name: 'Loved Ones: Inpatient Units',
                video: {
                    id: 190,
                    name: 'Loved Ones: Inpatient Units',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Huynh_-_Understanding_Inpatient.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/inpatientUnits.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Huynh_-_Understanding_Inpatient/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Huynh_-_Understanding_Inpatient/jaspr_720p_Huynh_-_Understanding_Inpatient.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Huynh_-_Understanding_Inpatient/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Huynh_-_Understanding_Inpatient/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/inpatientUnit_thumbnail2x.jpg',
                targetUrl: '',
                labelColor: '#6e8ea3',
                order: 29,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 33,
                name: 'Loved Ones: First 72 Hours Post ER',
                video: {
                    id: 192,
                    name: 'Loved Ones: First 72 Hours Post ER',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Julia_-_First_72_Hours.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/first72hours_poster.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Julia_-_First_72_Hours/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Julia_-_First_72_Hours/jaspr_720p_Julia_-_First_72_Hours.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Julia_-_First_72_Hours/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Julia_-_First_72_Hours/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/first72hours_thumbnail2x.jpg',
                targetUrl: '',
                labelColor: '#513c26',
                order: 31,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 30,
                name: 'Loved Ones: Levels of Care',
                video: {
                    id: 193,
                    name: 'Loved Ones: Levels of Care',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Huynh_-_Understanding_Levels_of_Care.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/levelsOfCare.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Huynh_-_Understanding_Levels_of_Care/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Huynh_-_Understanding_Levels_of_Care/jaspr_720p_Huynh_-_Understanding_Levels_of_Care.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Huynh_-_Understanding_Levels_of_Care/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Huynh_-_Understanding_Levels_of_Care/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/levelsOfCare_thumbnail2x.jpg',
                targetUrl: '',
                labelColor: '#44669c',
                order: 28,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 32,
                name: 'Loved Ones: Returning Home',
                video: {
                    id: 191,
                    name: 'Loved Ones: Returning Home',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Huynh_-_Taking_Your_Loved_One_Home_from_the_ER.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: 'https://media.jaspr-development.com/returningHome.png',
                    thumbnail: null,
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Huynh_-_Taking_Your_Loved_One_Home_from_the_ER/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Huynh_-_Taking_Your_Loved_One_Home_from_the_ER/jaspr_720p_Huynh_-_Taking_Your_Loved_One_Home_from_the_ER.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Huynh_-_Taking_Your_Loved_One_Home_from_the_ER/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Huynh_-_Taking_Your_Loved_One_Home_from_the_ER/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/returningHome_thumbnail2x.jpg',
                targetUrl: '',
                labelColor: '#32634a',
                order: 30,
                patientActivity: null,
                saveForLater: false,
            },
            {
                id: 7,
                name: 'Paced Breathing',
                video: null,
                mainPageImage: null,
                thumbnailImage: 'https://media.jaspr-development.com/pacedBreathing2x.jpg',
                targetUrl: '/breathe',
                labelColor: '#3c3431',
                order: 1,
                patientActivity: null,
                saveForLater: false,
            },
        ],
    },
};
