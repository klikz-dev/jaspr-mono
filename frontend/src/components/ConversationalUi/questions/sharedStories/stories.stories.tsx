import { ComponentStory, ComponentMeta } from '@storybook/react';
import SharedStories from '.';

export default {
    title: 'ConversationalUi/SharedStories',
    component: SharedStories,
    argTypes: {},
} as ComponentMeta<typeof SharedStories>;

const Template: ComponentStory<typeof SharedStories> = (args) => {
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
            }}
        >
            <SharedStories />
        </div>
    );
};

export const Default = Template.bind({});

Default.parameters = {
    initialState: {
        ...Default.parameters,
        stories: {
            people: [
                {
                    id: 1,
                    name: 'Ashley',
                    labelColor: '',
                    order: 10,
                    thumbnail: 'https://media.jaspr-development.com/Ashley3x.png',
                    videos: [
                        {
                            id: 14,
                            name: 'Ashley - My Story',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Ashley_-_My_Story_uploaded.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_My_Story_uploaded/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_My_Story_uploaded/jaspr_720p_Ashley_-_My_Story_uploaded.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_My_Story_uploaded/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_My_Story_uploaded/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 13,
                            name: 'Ashley - My Wish For You',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Ashley_-_My_Wish_for_You.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_My_Wish_for_You/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_My_Wish_for_You/jaspr_720p_Ashley_-_My_Wish_for_You.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_My_Wish_for_You/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_My_Wish_for_You/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 169,
                            name: 'Ashley - Relationship to Suicide',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Ashley_-_Relationship_to_Suicide.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_Relationship_to_Suicide/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_Relationship_to_Suicide/jaspr_720p_Ashley_-_Relationship_to_Suicide.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_Relationship_to_Suicide/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_Relationship_to_Suicide/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 49,
                            name: 'Ashley - My ER Experience',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Ashley_-_My_ER_Experience.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_My_ER_Experience/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_My_ER_Experience/jaspr_720p_Ashley_-_My_ER_Experience.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_My_ER_Experience/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_My_ER_Experience/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 48,
                            name: 'Ashley - Surviving the ER',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Ashley_-_Surviving_the_ER.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_Surviving_the_ER/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_Surviving_the_ER/jaspr_720p_Ashley_-_Surviving_the_ER.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_Surviving_the_ER/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_Surviving_the_ER/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 170,
                            name: 'Ashley - Going Home',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Ashley_-_Going_HomeV2.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_Going_HomeV2/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_Going_HomeV2/jaspr_720p_Ashley_-_Going_HomeV2.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_Going_HomeV2/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_Going_HomeV2/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 10,
                            name: 'Ashley - What I Do to Stay Well',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Ashley_-_What_I_Do_to_Stay_Well.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_What_I_Do_to_Stay_Well/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_What_I_Do_to_Stay_Well/jaspr_720p_Ashley_-_What_I_Do_to_Stay_Well.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_What_I_Do_to_Stay_Well/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_What_I_Do_to_Stay_Well/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
                {
                    id: 2,
                    name: 'Kelechi',
                    labelColor: '',
                    order: 20,
                    thumbnail: 'https://media.jaspr-development.com/Kelechi3x.png',
                    videos: [
                        {
                            id: 9,
                            name: 'Kelechi - My Story',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Kelechi_-_My_StoryV2.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_My_StoryV2/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_My_StoryV2/jaspr_720p_Kelechi_-_My_StoryV2.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_My_StoryV2/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_My_StoryV2/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 12,
                            name: 'Kelechi - My Wish For You',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Kelechi_-_My_Wish_for_Youv2.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_My_Wish_for_Youv2/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_My_Wish_for_Youv2/jaspr_720p_Kelechi_-_My_Wish_for_Youv2.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_My_Wish_for_Youv2/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_My_Wish_for_Youv2/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 7,
                            name: 'Kelechi - Relationship to Suicide',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Kelechi_-_Relationship_to_Suicidev2.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_Relationship_to_Suicidev2/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_Relationship_to_Suicidev2/jaspr_720p_Kelechi_-_Relationship_to_Suicidev2.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_Relationship_to_Suicidev2/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_Relationship_to_Suicidev2/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 43,
                            name: 'Kelechi - My ER Experience',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Kelechi_-_My_ER_ExperienceV2.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_My_ER_ExperienceV2/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_My_ER_ExperienceV2/jaspr_720p_Kelechi_-_My_ER_ExperienceV2.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_My_ER_ExperienceV2/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_My_ER_ExperienceV2/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 6,
                            name: 'Kelechi - Going Home',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Kelechi_-_Going_HomeV2.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_Going_HomeV2/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_Going_HomeV2/jaspr_720p_Kelechi_-_Going_HomeV2.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_Going_HomeV2/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_Going_HomeV2/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
                {
                    id: 3,
                    name: 'Topher',
                    labelColor: '',
                    order: 30,
                    thumbnail: 'https://media.jaspr-development.com/Topher3x.png',
                    videos: [
                        {
                            id: 15,
                            name: 'Topher - My Story',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Topher_-_My_Story.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Topher_-_My_Story/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Topher_-_My_Story/jaspr_720p_Topher_-_My_Story.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Topher_-_My_Story/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Topher_-_My_Story/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 45,
                            name: 'Topher - My Wish For You',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Topher_-_My_Wish_for_You.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Topher_-_My_Wish_for_You/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Topher_-_My_Wish_for_You/jaspr_720p_Topher_-_My_Wish_for_You.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Topher_-_My_Wish_for_You/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Topher_-_My_Wish_for_You/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 8,
                            name: 'Topher - Relationship to Suicide',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Topher_-_Relationship_to_Suicide_Now.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Topher_-_Relationship_to_Suicide_Now/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Topher_-_Relationship_to_Suicide_Now/jaspr_720p_Topher_-_Relationship_to_Suicide_Now.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Topher_-_Relationship_to_Suicide_Now/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Topher_-_Relationship_to_Suicide_Now/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 54,
                            name: 'Topher - My ER Experience',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Topher_-_My_ER_Experience.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Topher_-_My_ER_Experience/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Topher_-_My_ER_Experience/jaspr_720p_Topher_-_My_ER_Experience.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Topher_-_My_ER_Experience/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Topher_-_My_ER_Experience/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 50,
                            name: 'Topher - Surviving the ER',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Topher_-_Surviving_the_ER.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Topher_-_Surviving_the_ER/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Topher_-_Surviving_the_ER/jaspr_720p_Topher_-_Surviving_the_ER.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Topher_-_Surviving_the_ER/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Topher_-_Surviving_the_ER/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 204,
                            name: 'Topher - Supportive People',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster:
                                'https://media.jaspr-development.com/Screen_Shot_2020-06-05_at_11.21.18_AM.png',
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story/kiosk_720p_Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 11,
                            name: 'Topher - What I Do to Stay Well',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Topher_-_What_I_Do_to_Stay_Well.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Topher_-_What_I_Do_to_Stay_Well/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Topher_-_What_I_Do_to_Stay_Well/jaspr_720p_Topher_-_What_I_Do_to_Stay_Well.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Topher_-_What_I_Do_to_Stay_Well/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Topher_-_What_I_Do_to_Stay_Well/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
                {
                    id: 4,
                    name: 'Beth',
                    labelColor: '',
                    order: 40,
                    thumbnail: 'https://media.jaspr-development.com/Beth3x.png',
                    videos: [
                        {
                            id: 174,
                            name: 'Beth - My Story',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Beth_-_My_Story.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Beth_-_My_Story/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Beth_-_My_Story/jaspr_720p_Beth_-_My_Story.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Beth_-_My_Story/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Beth_-_My_Story/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 52,
                            name: 'Beth - Relationship to Suicide',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Beth_-_Relationship_to_Suicide_Nov25.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Beth_-_Relationship_to_Suicide_Nov25/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Beth_-_Relationship_to_Suicide_Nov25/jaspr_720p_Beth_-_Relationship_to_Suicide_Nov25.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Beth_-_Relationship_to_Suicide_Nov25/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Beth_-_Relationship_to_Suicide_Nov25/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 47,
                            name: 'Beth - Surviving the ER',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Beth_-_Surviving_the_ER_1.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Beth_-_Surviving_the_ER_1/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Beth_-_Surviving_the_ER_1/jaspr_720p_Beth_-_Surviving_the_ER_1.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Beth_-_Surviving_the_ER_1/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Beth_-_Surviving_the_ER_1/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 163,
                            name: 'Beth - What I Do to Stay Well',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Beth_-_What_I_Do_to_Stay_WellNov25.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Beth_-_What_I_Do_to_Stay_WellNov25/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Beth_-_What_I_Do_to_Stay_WellNov25/jaspr_720p_Beth_-_What_I_Do_to_Stay_WellNov25.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Beth_-_What_I_Do_to_Stay_WellNov25/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Beth_-_What_I_Do_to_Stay_WellNov25/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
                {
                    id: 5,
                    name: 'Jim',
                    labelColor: '',
                    order: 50,
                    thumbnail: 'https://media.jaspr-development.com/Jim3x.png',
                    videos: [
                        {
                            id: 180,
                            name: 'Jim - My Story',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Jim_-_My_Story.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Jim_-_My_Story/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Jim_-_My_Story/jaspr_720p_Jim_-_My_Story.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Jim_-_My_Story/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Jim_-_My_Story/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 181,
                            name: 'Jim - My Wish For You',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Jim_-_My_Wish_for_You.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Jim_-_My_Wish_for_You/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Jim_-_My_Wish_for_You/jaspr_720p_Jim_-_My_Wish_for_You.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Jim_-_My_Wish_for_You/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Jim_-_My_Wish_for_You/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 178,
                            name: 'Jim - Coping with Shame',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Jim_-_Coping_with_Shame.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Jim_-_Coping_with_Shame/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Jim_-_Coping_with_Shame/jaspr_720p_Jim_-_Coping_with_Shame.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Jim_-_Coping_with_Shame/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Jim_-_Coping_with_Shame/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 179,
                            name: 'Jim - Going Home',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Jim_-_Going_Home.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Jim_-_Going_Home/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Jim_-_Going_Home/jaspr_720p_Jim_-_Going_Home.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Jim_-_Going_Home/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Jim_-_Going_Home/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 182,
                            name: 'Jim - What I Do to Stay Well',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Jim_-_What_I_do_to_Stay_Well.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Jim_-_What_I_do_to_Stay_Well/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Jim_-_What_I_do_to_Stay_Well/jaspr_720p_Jim_-_What_I_do_to_Stay_Well.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Jim_-_What_I_do_to_Stay_Well/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Jim_-_What_I_do_to_Stay_Well/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
                {
                    id: 6,
                    name: 'Emmy',
                    labelColor: '',
                    order: 60,
                    thumbnail: 'https://media.jaspr-development.com/Emmy3x.png',
                    videos: [
                        {
                            id: 162,
                            name: 'Emmy - My Story',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Emmy_-_My_Story.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_My_Story/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_My_Story/jaspr_720p_Emmy_-_My_Story.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_My_Story/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_My_Story/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 160,
                            name: 'Emmy - My Wish For You',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Emmy_-_My_Wish_for_You.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_My_Wish_for_You/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_My_Wish_for_You/jaspr_720p_Emmy_-_My_Wish_for_You.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_My_Wish_for_You/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_My_Wish_for_You/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 158,
                            name: 'Emmy - Relationship to Suicide',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Emmy_-_Relationship_to_Suicide.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_Relationship_to_Suicide/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_Relationship_to_Suicide/jaspr_720p_Emmy_-_Relationship_to_Suicide.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_Relationship_to_Suicide/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_Relationship_to_Suicide/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 164,
                            name: 'Emmy - Coping with Shame',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Emmy_-_Coping_with_ShameNov25.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_Coping_with_ShameNov25/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_Coping_with_ShameNov25/jaspr_720p_Emmy_-_Coping_with_ShameNov25.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_Coping_with_ShameNov25/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_Coping_with_ShameNov25/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 155,
                            name: 'Emmy - Going Home',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Emmy_-_Going_Home.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_Going_Home/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_Going_Home/jaspr_720p_Emmy_-_Going_Home.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_Going_Home/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_Going_Home/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 171,
                            name: 'Emmy - What I Do to Stay Well',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Emmy_-_What_I_do_to_Stay_Well.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_What_I_do_to_Stay_Well/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_What_I_do_to_Stay_Well/jaspr_720p_Emmy_-_What_I_do_to_Stay_Well.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_What_I_do_to_Stay_Well/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_What_I_do_to_Stay_Well/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
                {
                    id: 7,
                    name: 'Thai',
                    labelColor: '',
                    order: 70,
                    thumbnail: 'https://media.jaspr-development.com/Thai3x.png',
                    videos: [
                        {
                            id: 173,
                            name: 'Thai - My Story',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Thai_-_My_Story.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Thai_-_My_Story/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Thai_-_My_Story/jaspr_720p_Thai_-_My_Story.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Thai_-_My_Story/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Thai_-_My_Story/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 159,
                            name: 'Thai - My Wish For You',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Thai_-_My_Wish_for_You.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Thai_-_My_Wish_for_You/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Thai_-_My_Wish_for_You/jaspr_720p_Thai_-_My_Wish_for_You.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Thai_-_My_Wish_for_You/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Thai_-_My_Wish_for_You/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 156,
                            name: 'Thai - Relationship to Suicide',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Thai_-_Relationship_to_Suicide.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Thai_-_Relationship_to_Suicide/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Thai_-_Relationship_to_Suicide/jaspr_720p_Thai_-_Relationship_to_Suicide.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Thai_-_Relationship_to_Suicide/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Thai_-_Relationship_to_Suicide/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 157,
                            name: 'Thai - Coping with Shame',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Thai_-_Coping_with_Shame.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Thai_-_Coping_with_Shame/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Thai_-_Coping_with_Shame/jaspr_720p_Thai_-_Coping_with_Shame.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Thai_-_Coping_with_Shame/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Thai_-_Coping_with_Shame/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 172,
                            name: 'Thai - Surviving the ER',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Thai_-_Surviving_the_ER.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Thai_-_Surviving_the_ER/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Thai_-_Surviving_the_ER/jaspr_720p_Thai_-_Surviving_the_ER.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Thai_-_Surviving_the_ER/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Thai_-_Surviving_the_ER/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 167,
                            name: 'Thai - What I Do to Stay Well',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Thai_-_What_I_Do_to_Stay_Well.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Thai_-_What_I_Do_to_Stay_Well/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Thai_-_What_I_Do_to_Stay_Well/jaspr_720p_Thai_-_What_I_Do_to_Stay_Well.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Thai_-_What_I_Do_to_Stay_Well/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Thai_-_What_I_Do_to_Stay_Well/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
                {
                    id: 8,
                    name: 'Charles',
                    labelColor: '',
                    order: 80,
                    thumbnail: 'https://media.jaspr-development.com/Charles3x.png',
                    videos: [
                        {
                            id: 175,
                            name: 'Charles - My Wish For You',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Charles_-_My_Wish_for_You.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Charles_-_My_Wish_for_You/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Charles_-_My_Wish_for_You/jaspr_720p_Charles_-_My_Wish_for_You.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Charles_-_My_Wish_for_You/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Charles_-_My_Wish_for_You/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
                {
                    id: 9,
                    name: 'Diana',
                    labelColor: '',
                    order: 90,
                    thumbnail: 'https://media.jaspr-development.com/Diana3x.png',
                    videos: [
                        {
                            id: 168,
                            name: 'Diana - My Story',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Diana_-_My_Story.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Diana_-_My_Story/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Diana_-_My_Story/jaspr_720p_Diana_-_My_Story.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Diana_-_My_Story/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Diana_-_My_Story/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 46,
                            name: 'Diana - Relationship to Suicide',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Diana_-_Relationship_to_Suicide.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Diana_-_Relationship_to_Suicide/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Diana_-_Relationship_to_Suicide/jaspr_720p_Diana_-_Relationship_to_Suicide.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Diana_-_Relationship_to_Suicide/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Diana_-_Relationship_to_Suicide/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 177,
                            name: 'Diana - My ER Experience',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Diana_-_My_ER_Experience.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Diana_-_My_ER_Experience/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Diana_-_My_ER_Experience/jaspr_720p_Diana_-_My_ER_Experience.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Diana_-_My_ER_Experience/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Diana_-_My_ER_Experience/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 44,
                            name: 'Diana - Going Home',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Diana_-_Going_Home.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Diana_-_Going_Home/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Diana_-_Going_Home/jaspr_720p_Diana_-_Going_Home.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Diana_-_Going_Home/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Diana_-_Going_Home/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 53,
                            name: 'Diana - What I Do to Stay Well',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Diana_-_What_I_do_to_Stay_Well.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Diana_-_What_I_do_to_Stay_Well/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Diana_-_What_I_do_to_Stay_Well/jaspr_720p_Diana_-_What_I_do_to_Stay_Well.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Diana_-_What_I_do_to_Stay_Well/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Diana_-_What_I_do_to_Stay_Well/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
                {
                    id: 11,
                    name: 'Ursula',
                    labelColor: '',
                    order: 100,
                    thumbnail: 'https://media.jaspr-development.com/Ursula3x.png',
                    videos: [
                        {
                            id: 176,
                            name: 'Ursula - Coping with Shame',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Ursula_-_Coping_with_Shame.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Ursula_-_Coping_with_Shame/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Ursula_-_Coping_with_Shame/jaspr_720p_Ursula_-_Coping_with_Shame.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Ursula_-_Coping_with_Shame/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Ursula_-_Coping_with_Shame/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 185,
                            name: 'Ursula - Going Home',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Ursula_-_Lethal_Means.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Ursula_-_Lethal_Means/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Ursula_-_Lethal_Means/jaspr_720p_Ursula_-_Lethal_Means.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Ursula_-_Lethal_Means/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Ursula_-_Lethal_Means/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
                {
                    id: 10,
                    name: 'Lisa',
                    labelColor: '',
                    order: 110,
                    thumbnail: 'https://media.jaspr-development.com/Lisa3x.png',
                    videos: [
                        {
                            id: 51,
                            name: 'Lisa - Going Home',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Lisa_-_Going_Home.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Lisa_-_Going_Home/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Lisa_-_Going_Home/jaspr_720p_Lisa_-_Going_Home.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Lisa_-_Going_Home/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Lisa_-_Going_Home/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
            ],
            topics: [
                {
                    id: 1,
                    name: 'My Story',
                    labelColor: '',
                    order: 10,
                    videos: [
                        {
                            id: 173,
                            name: 'Thai - My Story',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Thai_-_My_Story.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Thai_-_My_Story/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Thai_-_My_Story/jaspr_720p_Thai_-_My_Story.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Thai_-_My_Story/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Thai_-_My_Story/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 162,
                            name: 'Emmy - My Story',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Emmy_-_My_Story.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_My_Story/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_My_Story/jaspr_720p_Emmy_-_My_Story.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_My_Story/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_My_Story/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 180,
                            name: 'Jim - My Story',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Jim_-_My_Story.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Jim_-_My_Story/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Jim_-_My_Story/jaspr_720p_Jim_-_My_Story.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Jim_-_My_Story/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Jim_-_My_Story/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 14,
                            name: 'Ashley - My Story',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Ashley_-_My_Story_uploaded.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_My_Story_uploaded/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_My_Story_uploaded/jaspr_720p_Ashley_-_My_Story_uploaded.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_My_Story_uploaded/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_My_Story_uploaded/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 15,
                            name: 'Topher - My Story',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Topher_-_My_Story.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Topher_-_My_Story/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Topher_-_My_Story/jaspr_720p_Topher_-_My_Story.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Topher_-_My_Story/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Topher_-_My_Story/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 174,
                            name: 'Beth - My Story',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Beth_-_My_Story.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Beth_-_My_Story/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Beth_-_My_Story/jaspr_720p_Beth_-_My_Story.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Beth_-_My_Story/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Beth_-_My_Story/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 9,
                            name: 'Kelechi - My Story',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Kelechi_-_My_StoryV2.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_My_StoryV2/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_My_StoryV2/jaspr_720p_Kelechi_-_My_StoryV2.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_My_StoryV2/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_My_StoryV2/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 168,
                            name: 'Diana - My Story',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Diana_-_My_Story.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Diana_-_My_Story/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Diana_-_My_Story/jaspr_720p_Diana_-_My_Story.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Diana_-_My_Story/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Diana_-_My_Story/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
                {
                    id: 9,
                    name: 'Supportive People',
                    labelColor: '',
                    order: 15,
                    videos: [
                        {
                            id: 204,
                            name: 'Topher - Supportive People',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster:
                                'https://media.jaspr-development.com/Screen_Shot_2020-06-05_at_11.21.18_AM.png',
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story/kiosk_720p_Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
                {
                    id: 2,
                    name: 'My Wish for You',
                    labelColor: '',
                    order: 20,
                    videos: [
                        {
                            id: 181,
                            name: 'Jim - My Wish For You',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Jim_-_My_Wish_for_You.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Jim_-_My_Wish_for_You/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Jim_-_My_Wish_for_You/jaspr_720p_Jim_-_My_Wish_for_You.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Jim_-_My_Wish_for_You/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Jim_-_My_Wish_for_You/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 175,
                            name: 'Charles - My Wish For You',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Charles_-_My_Wish_for_You.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Charles_-_My_Wish_for_You/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Charles_-_My_Wish_for_You/jaspr_720p_Charles_-_My_Wish_for_You.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Charles_-_My_Wish_for_You/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Charles_-_My_Wish_for_You/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 160,
                            name: 'Emmy - My Wish For You',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Emmy_-_My_Wish_for_You.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_My_Wish_for_You/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_My_Wish_for_You/jaspr_720p_Emmy_-_My_Wish_for_You.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_My_Wish_for_You/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_My_Wish_for_You/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 45,
                            name: 'Topher - My Wish For You',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Topher_-_My_Wish_for_You.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Topher_-_My_Wish_for_You/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Topher_-_My_Wish_for_You/jaspr_720p_Topher_-_My_Wish_for_You.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Topher_-_My_Wish_for_You/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Topher_-_My_Wish_for_You/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 159,
                            name: 'Thai - My Wish For You',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Thai_-_My_Wish_for_You.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Thai_-_My_Wish_for_You/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Thai_-_My_Wish_for_You/jaspr_720p_Thai_-_My_Wish_for_You.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Thai_-_My_Wish_for_You/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Thai_-_My_Wish_for_You/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 12,
                            name: 'Kelechi - My Wish For You',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Kelechi_-_My_Wish_for_Youv2.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_My_Wish_for_Youv2/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_My_Wish_for_Youv2/jaspr_720p_Kelechi_-_My_Wish_for_Youv2.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_My_Wish_for_Youv2/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_My_Wish_for_Youv2/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 13,
                            name: 'Ashley - My Wish For You',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Ashley_-_My_Wish_for_You.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_My_Wish_for_You/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_My_Wish_for_You/jaspr_720p_Ashley_-_My_Wish_for_You.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_My_Wish_for_You/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_My_Wish_for_You/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
                {
                    id: 6,
                    name: 'Relationship to Suicide',
                    labelColor: '',
                    order: 30,
                    videos: [
                        {
                            id: 158,
                            name: 'Emmy - Relationship to Suicide',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Emmy_-_Relationship_to_Suicide.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_Relationship_to_Suicide/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_Relationship_to_Suicide/jaspr_720p_Emmy_-_Relationship_to_Suicide.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_Relationship_to_Suicide/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_Relationship_to_Suicide/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 7,
                            name: 'Kelechi - Relationship to Suicide',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Kelechi_-_Relationship_to_Suicidev2.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_Relationship_to_Suicidev2/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_Relationship_to_Suicidev2/jaspr_720p_Kelechi_-_Relationship_to_Suicidev2.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_Relationship_to_Suicidev2/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_Relationship_to_Suicidev2/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 8,
                            name: 'Topher - Relationship to Suicide',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Topher_-_Relationship_to_Suicide_Now.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Topher_-_Relationship_to_Suicide_Now/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Topher_-_Relationship_to_Suicide_Now/jaspr_720p_Topher_-_Relationship_to_Suicide_Now.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Topher_-_Relationship_to_Suicide_Now/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Topher_-_Relationship_to_Suicide_Now/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 46,
                            name: 'Diana - Relationship to Suicide',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Diana_-_Relationship_to_Suicide.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Diana_-_Relationship_to_Suicide/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Diana_-_Relationship_to_Suicide/jaspr_720p_Diana_-_Relationship_to_Suicide.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Diana_-_Relationship_to_Suicide/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Diana_-_Relationship_to_Suicide/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 169,
                            name: 'Ashley - Relationship to Suicide',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Ashley_-_Relationship_to_Suicide.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_Relationship_to_Suicide/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_Relationship_to_Suicide/jaspr_720p_Ashley_-_Relationship_to_Suicide.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_Relationship_to_Suicide/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_Relationship_to_Suicide/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 52,
                            name: 'Beth - Relationship to Suicide',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Beth_-_Relationship_to_Suicide_Nov25.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Beth_-_Relationship_to_Suicide_Nov25/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Beth_-_Relationship_to_Suicide_Nov25/jaspr_720p_Beth_-_Relationship_to_Suicide_Nov25.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Beth_-_Relationship_to_Suicide_Nov25/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Beth_-_Relationship_to_Suicide_Nov25/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 156,
                            name: 'Thai - Relationship to Suicide',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Thai_-_Relationship_to_Suicide.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Thai_-_Relationship_to_Suicide/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Thai_-_Relationship_to_Suicide/jaspr_720p_Thai_-_Relationship_to_Suicide.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Thai_-_Relationship_to_Suicide/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Thai_-_Relationship_to_Suicide/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
                {
                    id: 8,
                    name: 'Coping with Shame',
                    labelColor: '',
                    order: 40,
                    videos: [
                        {
                            id: 178,
                            name: 'Jim - Coping with Shame',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Jim_-_Coping_with_Shame.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Jim_-_Coping_with_Shame/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Jim_-_Coping_with_Shame/jaspr_720p_Jim_-_Coping_with_Shame.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Jim_-_Coping_with_Shame/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Jim_-_Coping_with_Shame/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 157,
                            name: 'Thai - Coping with Shame',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Thai_-_Coping_with_Shame.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Thai_-_Coping_with_Shame/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Thai_-_Coping_with_Shame/jaspr_720p_Thai_-_Coping_with_Shame.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Thai_-_Coping_with_Shame/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Thai_-_Coping_with_Shame/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 164,
                            name: 'Emmy - Coping with Shame',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Emmy_-_Coping_with_ShameNov25.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_Coping_with_ShameNov25/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_Coping_with_ShameNov25/jaspr_720p_Emmy_-_Coping_with_ShameNov25.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_Coping_with_ShameNov25/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_Coping_with_ShameNov25/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 176,
                            name: 'Ursula - Coping with Shame',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Ursula_-_Coping_with_Shame.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Ursula_-_Coping_with_Shame/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Ursula_-_Coping_with_Shame/jaspr_720p_Ursula_-_Coping_with_Shame.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Ursula_-_Coping_with_Shame/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Ursula_-_Coping_with_Shame/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
                {
                    id: 5,
                    name: 'My ER Experience',
                    labelColor: '',
                    order: 50,
                    videos: [
                        {
                            id: 43,
                            name: 'Kelechi - My ER Experience',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Kelechi_-_My_ER_ExperienceV2.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_My_ER_ExperienceV2/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_My_ER_ExperienceV2/jaspr_720p_Kelechi_-_My_ER_ExperienceV2.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_My_ER_ExperienceV2/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_My_ER_ExperienceV2/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 49,
                            name: 'Ashley - My ER Experience',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Ashley_-_My_ER_Experience.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_My_ER_Experience/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_My_ER_Experience/jaspr_720p_Ashley_-_My_ER_Experience.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_My_ER_Experience/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_My_ER_Experience/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 54,
                            name: 'Topher - My ER Experience',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Topher_-_My_ER_Experience.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Topher_-_My_ER_Experience/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Topher_-_My_ER_Experience/jaspr_720p_Topher_-_My_ER_Experience.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Topher_-_My_ER_Experience/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Topher_-_My_ER_Experience/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 177,
                            name: 'Diana - My ER Experience',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Diana_-_My_ER_Experience.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Diana_-_My_ER_Experience/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Diana_-_My_ER_Experience/jaspr_720p_Diana_-_My_ER_Experience.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Diana_-_My_ER_Experience/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Diana_-_My_ER_Experience/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
                {
                    id: 4,
                    name: 'Surviving the ER',
                    labelColor: '',
                    order: 60,
                    videos: [
                        {
                            id: 47,
                            name: 'Beth - Surviving the ER',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Beth_-_Surviving_the_ER_1.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Beth_-_Surviving_the_ER_1/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Beth_-_Surviving_the_ER_1/jaspr_720p_Beth_-_Surviving_the_ER_1.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Beth_-_Surviving_the_ER_1/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Beth_-_Surviving_the_ER_1/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 50,
                            name: 'Topher - Surviving the ER',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Topher_-_Surviving_the_ER.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Topher_-_Surviving_the_ER/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Topher_-_Surviving_the_ER/jaspr_720p_Topher_-_Surviving_the_ER.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Topher_-_Surviving_the_ER/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Topher_-_Surviving_the_ER/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 172,
                            name: 'Thai - Surviving the ER',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Thai_-_Surviving_the_ER.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Thai_-_Surviving_the_ER/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Thai_-_Surviving_the_ER/jaspr_720p_Thai_-_Surviving_the_ER.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Thai_-_Surviving_the_ER/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Thai_-_Surviving_the_ER/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 48,
                            name: 'Ashley - Surviving the ER',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Ashley_-_Surviving_the_ER.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_Surviving_the_ER/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_Surviving_the_ER/jaspr_720p_Ashley_-_Surviving_the_ER.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_Surviving_the_ER/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_Surviving_the_ER/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
                {
                    id: 7,
                    name: 'Going Home',
                    labelColor: '',
                    order: 70,
                    videos: [
                        {
                            id: 179,
                            name: 'Jim - Going Home',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Jim_-_Going_Home.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Jim_-_Going_Home/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Jim_-_Going_Home/jaspr_720p_Jim_-_Going_Home.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Jim_-_Going_Home/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Jim_-_Going_Home/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 44,
                            name: 'Diana - Going Home',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Diana_-_Going_Home.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Diana_-_Going_Home/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Diana_-_Going_Home/jaspr_720p_Diana_-_Going_Home.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Diana_-_Going_Home/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Diana_-_Going_Home/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 185,
                            name: 'Ursula - Going Home',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Ursula_-_Lethal_Means.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Ursula_-_Lethal_Means/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Ursula_-_Lethal_Means/jaspr_720p_Ursula_-_Lethal_Means.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Ursula_-_Lethal_Means/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Ursula_-_Lethal_Means/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 155,
                            name: 'Emmy - Going Home',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Emmy_-_Going_Home.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_Going_Home/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_Going_Home/jaspr_720p_Emmy_-_Going_Home.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_Going_Home/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_Going_Home/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 170,
                            name: 'Ashley - Going Home',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Ashley_-_Going_HomeV2.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_Going_HomeV2/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_Going_HomeV2/jaspr_720p_Ashley_-_Going_HomeV2.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_Going_HomeV2/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_Going_HomeV2/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 6,
                            name: 'Kelechi - Going Home',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Kelechi_-_Going_HomeV2.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_Going_HomeV2/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Kelechi_-_Going_HomeV2/jaspr_720p_Kelechi_-_Going_HomeV2.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_Going_HomeV2/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Kelechi_-_Going_HomeV2/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 51,
                            name: 'Lisa - Going Home',
                            description: '',
                            fileField: 'https://media.jaspr-development.com/Lisa_-_Going_Home.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Lisa_-_Going_Home/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Lisa_-_Going_Home/jaspr_720p_Lisa_-_Going_Home.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Lisa_-_Going_Home/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Lisa_-_Going_Home/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
                {
                    id: 3,
                    name: 'What I Do to Stay Well',
                    labelColor: '',
                    order: 80,
                    videos: [
                        {
                            id: 163,
                            name: 'Beth - What I Do to Stay Well',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Beth_-_What_I_Do_to_Stay_WellNov25.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Beth_-_What_I_Do_to_Stay_WellNov25/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Beth_-_What_I_Do_to_Stay_WellNov25/jaspr_720p_Beth_-_What_I_Do_to_Stay_WellNov25.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Beth_-_What_I_Do_to_Stay_WellNov25/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Beth_-_What_I_Do_to_Stay_WellNov25/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 182,
                            name: 'Jim - What I Do to Stay Well',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Jim_-_What_I_do_to_Stay_Well.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Jim_-_What_I_do_to_Stay_Well/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Jim_-_What_I_do_to_Stay_Well/jaspr_720p_Jim_-_What_I_do_to_Stay_Well.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Jim_-_What_I_do_to_Stay_Well/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Jim_-_What_I_do_to_Stay_Well/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 53,
                            name: 'Diana - What I Do to Stay Well',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Diana_-_What_I_do_to_Stay_Well.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Diana_-_What_I_do_to_Stay_Well/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Diana_-_What_I_do_to_Stay_Well/jaspr_720p_Diana_-_What_I_do_to_Stay_Well.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Diana_-_What_I_do_to_Stay_Well/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Diana_-_What_I_do_to_Stay_Well/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 171,
                            name: 'Emmy - What I Do to Stay Well',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Emmy_-_What_I_do_to_Stay_Well.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_What_I_do_to_Stay_Well/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Emmy_-_What_I_do_to_Stay_Well/jaspr_720p_Emmy_-_What_I_do_to_Stay_Well.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_What_I_do_to_Stay_Well/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Emmy_-_What_I_do_to_Stay_Well/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 11,
                            name: 'Topher - What I Do to Stay Well',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Topher_-_What_I_Do_to_Stay_Well.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Topher_-_What_I_Do_to_Stay_Well/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Topher_-_What_I_Do_to_Stay_Well/jaspr_720p_Topher_-_What_I_Do_to_Stay_Well.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Topher_-_What_I_Do_to_Stay_Well/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Topher_-_What_I_Do_to_Stay_Well/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 10,
                            name: 'Ashley - What I Do to Stay Well',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Ashley_-_What_I_Do_to_Stay_Well.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_What_I_Do_to_Stay_Well/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Ashley_-_What_I_Do_to_Stay_Well/jaspr_720p_Ashley_-_What_I_Do_to_Stay_Well.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_What_I_Do_to_Stay_Well/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Ashley_-_What_I_Do_to_Stay_Well/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                        {
                            id: 167,
                            name: 'Thai - What I Do to Stay Well',
                            description: '',
                            fileField:
                                'https://media.jaspr-development.com/Thai_-_What_I_Do_to_Stay_Well.mp4',
                            subtitleFile: null,
                            transcript: '',
                            poster: null,
                            thumbnail: null,
                            fpm4Transcode:
                                'https://media.jaspr-development.com/Thai_-_What_I_Do_to_Stay_Well/index.mpd',
                            mp4Transcode:
                                'https://media.jaspr-development.com/Thai_-_What_I_Do_to_Stay_Well/jaspr_720p_Thai_-_What_I_Do_to_Stay_Well.mp4',
                            mp3Transcode: null,
                            tips: '',
                            completionTime: null,
                            hlsPlaylist:
                                'https://media.jaspr-development.com/Thai_-_What_I_Do_to_Stay_Well/index.m3u8',
                            dashPlaylist:
                                'https://media.jaspr-development.com/Thai_-_What_I_Do_to_Stay_Well/index.mpd',
                            duration: null,
                            fileType: 'video',
                            tags: [],
                        },
                    ],
                },
            ],
            videos: [
                {
                    id: 173,
                    name: 'Thai - My Story',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Thai_-_My_Story.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Thai3x.png',
                    fpm4Transcode: 'https://media.jaspr-development.com/Thai_-_My_Story/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Thai_-_My_Story/jaspr_720p_Thai_-_My_Story.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist: 'https://media.jaspr-development.com/Thai_-_My_Story/index.m3u8',
                    dashPlaylist: 'https://media.jaspr-development.com/Thai_-_My_Story/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 162,
                    name: 'Emmy - My Story',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Emmy_-_My_Story.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Emmy3x.png',
                    fpm4Transcode: 'https://media.jaspr-development.com/Emmy_-_My_Story/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Emmy_-_My_Story/jaspr_720p_Emmy_-_My_Story.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist: 'https://media.jaspr-development.com/Emmy_-_My_Story/index.m3u8',
                    dashPlaylist: 'https://media.jaspr-development.com/Emmy_-_My_Story/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 180,
                    name: 'Jim - My Story',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Jim_-_My_Story.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Jim3x.png',
                    fpm4Transcode: 'https://media.jaspr-development.com/Jim_-_My_Story/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Jim_-_My_Story/jaspr_720p_Jim_-_My_Story.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist: 'https://media.jaspr-development.com/Jim_-_My_Story/index.m3u8',
                    dashPlaylist: 'https://media.jaspr-development.com/Jim_-_My_Story/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 14,
                    name: 'Ashley - My Story',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Ashley_-_My_Story_uploaded.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Ashley3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Ashley_-_My_Story_uploaded/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Ashley_-_My_Story_uploaded/jaspr_720p_Ashley_-_My_Story_uploaded.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Ashley_-_My_Story_uploaded/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Ashley_-_My_Story_uploaded/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 15,
                    name: 'Topher - My Story',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Topher_-_My_Story.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Topher3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Topher_-_My_Story/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Topher_-_My_Story/jaspr_720p_Topher_-_My_Story.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist: 'https://media.jaspr-development.com/Topher_-_My_Story/index.m3u8',
                    dashPlaylist: 'https://media.jaspr-development.com/Topher_-_My_Story/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 174,
                    name: 'Beth - My Story',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Beth_-_My_Story.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Beth3x.png',
                    fpm4Transcode: 'https://media.jaspr-development.com/Beth_-_My_Story/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Beth_-_My_Story/jaspr_720p_Beth_-_My_Story.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist: 'https://media.jaspr-development.com/Beth_-_My_Story/index.m3u8',
                    dashPlaylist: 'https://media.jaspr-development.com/Beth_-_My_Story/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 9,
                    name: 'Kelechi - My Story',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Kelechi_-_My_StoryV2.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Kelechi3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Kelechi_-_My_StoryV2/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Kelechi_-_My_StoryV2/jaspr_720p_Kelechi_-_My_StoryV2.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Kelechi_-_My_StoryV2/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Kelechi_-_My_StoryV2/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 168,
                    name: 'Diana - My Story',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Diana_-_My_Story.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Diana3x.png',
                    fpm4Transcode: 'https://media.jaspr-development.com/Diana_-_My_Story/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Diana_-_My_Story/jaspr_720p_Diana_-_My_Story.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist: 'https://media.jaspr-development.com/Diana_-_My_Story/index.m3u8',
                    dashPlaylist: 'https://media.jaspr-development.com/Diana_-_My_Story/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 181,
                    name: 'Jim - My Wish For You',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Jim_-_My_Wish_for_You.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Jim3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Jim_-_My_Wish_for_You/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Jim_-_My_Wish_for_You/jaspr_720p_Jim_-_My_Wish_for_You.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Jim_-_My_Wish_for_You/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Jim_-_My_Wish_for_You/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 175,
                    name: 'Charles - My Wish For You',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Charles_-_My_Wish_for_You.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Charles3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Charles_-_My_Wish_for_You/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Charles_-_My_Wish_for_You/jaspr_720p_Charles_-_My_Wish_for_You.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Charles_-_My_Wish_for_You/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Charles_-_My_Wish_for_You/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 160,
                    name: 'Emmy - My Wish For You',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Emmy_-_My_Wish_for_You.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Emmy3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Emmy_-_My_Wish_for_You/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Emmy_-_My_Wish_for_You/jaspr_720p_Emmy_-_My_Wish_for_You.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Emmy_-_My_Wish_for_You/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Emmy_-_My_Wish_for_You/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 45,
                    name: 'Topher - My Wish For You',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Topher_-_My_Wish_for_You.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Topher3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Topher_-_My_Wish_for_You/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Topher_-_My_Wish_for_You/jaspr_720p_Topher_-_My_Wish_for_You.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Topher_-_My_Wish_for_You/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Topher_-_My_Wish_for_You/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 159,
                    name: 'Thai - My Wish For You',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Thai_-_My_Wish_for_You.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Thai3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Thai_-_My_Wish_for_You/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Thai_-_My_Wish_for_You/jaspr_720p_Thai_-_My_Wish_for_You.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Thai_-_My_Wish_for_You/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Thai_-_My_Wish_for_You/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 12,
                    name: 'Kelechi - My Wish For You',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Kelechi_-_My_Wish_for_Youv2.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Kelechi3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Kelechi_-_My_Wish_for_Youv2/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Kelechi_-_My_Wish_for_Youv2/jaspr_720p_Kelechi_-_My_Wish_for_Youv2.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Kelechi_-_My_Wish_for_Youv2/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Kelechi_-_My_Wish_for_Youv2/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 13,
                    name: 'Ashley - My Wish For You',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Ashley_-_My_Wish_for_You.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Ashley3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Ashley_-_My_Wish_for_You/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Ashley_-_My_Wish_for_You/jaspr_720p_Ashley_-_My_Wish_for_You.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Ashley_-_My_Wish_for_You/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Ashley_-_My_Wish_for_You/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 158,
                    name: 'Emmy - Relationship to Suicide',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Emmy_-_Relationship_to_Suicide.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Emmy3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Emmy_-_Relationship_to_Suicide/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Emmy_-_Relationship_to_Suicide/jaspr_720p_Emmy_-_Relationship_to_Suicide.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Emmy_-_Relationship_to_Suicide/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Emmy_-_Relationship_to_Suicide/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 7,
                    name: 'Kelechi - Relationship to Suicide',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Kelechi_-_Relationship_to_Suicidev2.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Kelechi3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Kelechi_-_Relationship_to_Suicidev2/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Kelechi_-_Relationship_to_Suicidev2/jaspr_720p_Kelechi_-_Relationship_to_Suicidev2.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Kelechi_-_Relationship_to_Suicidev2/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Kelechi_-_Relationship_to_Suicidev2/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 8,
                    name: 'Topher - Relationship to Suicide',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Topher_-_Relationship_to_Suicide_Now.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Topher3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Topher_-_Relationship_to_Suicide_Now/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Topher_-_Relationship_to_Suicide_Now/jaspr_720p_Topher_-_Relationship_to_Suicide_Now.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Topher_-_Relationship_to_Suicide_Now/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Topher_-_Relationship_to_Suicide_Now/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 46,
                    name: 'Diana - Relationship to Suicide',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Diana_-_Relationship_to_Suicide.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Diana3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Diana_-_Relationship_to_Suicide/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Diana_-_Relationship_to_Suicide/jaspr_720p_Diana_-_Relationship_to_Suicide.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Diana_-_Relationship_to_Suicide/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Diana_-_Relationship_to_Suicide/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 169,
                    name: 'Ashley - Relationship to Suicide',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Ashley_-_Relationship_to_Suicide.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Ashley3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Ashley_-_Relationship_to_Suicide/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Ashley_-_Relationship_to_Suicide/jaspr_720p_Ashley_-_Relationship_to_Suicide.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Ashley_-_Relationship_to_Suicide/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Ashley_-_Relationship_to_Suicide/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 52,
                    name: 'Beth - Relationship to Suicide',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Beth_-_Relationship_to_Suicide_Nov25.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Beth3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Beth_-_Relationship_to_Suicide_Nov25/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Beth_-_Relationship_to_Suicide_Nov25/jaspr_720p_Beth_-_Relationship_to_Suicide_Nov25.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Beth_-_Relationship_to_Suicide_Nov25/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Beth_-_Relationship_to_Suicide_Nov25/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 156,
                    name: 'Thai - Relationship to Suicide',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Thai_-_Relationship_to_Suicide.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Thai3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Thai_-_Relationship_to_Suicide/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Thai_-_Relationship_to_Suicide/jaspr_720p_Thai_-_Relationship_to_Suicide.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Thai_-_Relationship_to_Suicide/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Thai_-_Relationship_to_Suicide/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 178,
                    name: 'Jim - Coping with Shame',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Jim_-_Coping_with_Shame.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Jim3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Jim_-_Coping_with_Shame/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Jim_-_Coping_with_Shame/jaspr_720p_Jim_-_Coping_with_Shame.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Jim_-_Coping_with_Shame/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Jim_-_Coping_with_Shame/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 157,
                    name: 'Thai - Coping with Shame',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Thai_-_Coping_with_Shame.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Thai3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Thai_-_Coping_with_Shame/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Thai_-_Coping_with_Shame/jaspr_720p_Thai_-_Coping_with_Shame.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Thai_-_Coping_with_Shame/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Thai_-_Coping_with_Shame/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 164,
                    name: 'Emmy - Coping with Shame',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Emmy_-_Coping_with_ShameNov25.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Emmy3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Emmy_-_Coping_with_ShameNov25/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Emmy_-_Coping_with_ShameNov25/jaspr_720p_Emmy_-_Coping_with_ShameNov25.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Emmy_-_Coping_with_ShameNov25/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Emmy_-_Coping_with_ShameNov25/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 176,
                    name: 'Ursula - Coping with Shame',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Ursula_-_Coping_with_Shame.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Ursula3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Ursula_-_Coping_with_Shame/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Ursula_-_Coping_with_Shame/jaspr_720p_Ursula_-_Coping_with_Shame.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Ursula_-_Coping_with_Shame/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Ursula_-_Coping_with_Shame/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 43,
                    name: 'Kelechi - My ER Experience',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Kelechi_-_My_ER_ExperienceV2.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Kelechi3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Kelechi_-_My_ER_ExperienceV2/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Kelechi_-_My_ER_ExperienceV2/jaspr_720p_Kelechi_-_My_ER_ExperienceV2.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Kelechi_-_My_ER_ExperienceV2/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Kelechi_-_My_ER_ExperienceV2/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 49,
                    name: 'Ashley - My ER Experience',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Ashley_-_My_ER_Experience.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Ashley3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Ashley_-_My_ER_Experience/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Ashley_-_My_ER_Experience/jaspr_720p_Ashley_-_My_ER_Experience.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Ashley_-_My_ER_Experience/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Ashley_-_My_ER_Experience/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 54,
                    name: 'Topher - My ER Experience',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Topher_-_My_ER_Experience.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Topher3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Topher_-_My_ER_Experience/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Topher_-_My_ER_Experience/jaspr_720p_Topher_-_My_ER_Experience.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Topher_-_My_ER_Experience/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Topher_-_My_ER_Experience/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 177,
                    name: 'Diana - My ER Experience',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Diana_-_My_ER_Experience.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Diana3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Diana_-_My_ER_Experience/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Diana_-_My_ER_Experience/jaspr_720p_Diana_-_My_ER_Experience.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Diana_-_My_ER_Experience/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Diana_-_My_ER_Experience/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 47,
                    name: 'Beth - Surviving the ER',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Beth_-_Surviving_the_ER_1.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Beth3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Beth_-_Surviving_the_ER_1/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Beth_-_Surviving_the_ER_1/jaspr_720p_Beth_-_Surviving_the_ER_1.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Beth_-_Surviving_the_ER_1/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Beth_-_Surviving_the_ER_1/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 50,
                    name: 'Topher - Surviving the ER',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Topher_-_Surviving_the_ER.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Topher3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Topher_-_Surviving_the_ER/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Topher_-_Surviving_the_ER/jaspr_720p_Topher_-_Surviving_the_ER.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Topher_-_Surviving_the_ER/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Topher_-_Surviving_the_ER/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 172,
                    name: 'Thai - Surviving the ER',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Thai_-_Surviving_the_ER.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Thai3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Thai_-_Surviving_the_ER/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Thai_-_Surviving_the_ER/jaspr_720p_Thai_-_Surviving_the_ER.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Thai_-_Surviving_the_ER/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Thai_-_Surviving_the_ER/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 48,
                    name: 'Ashley - Surviving the ER',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Ashley_-_Surviving_the_ER.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Ashley3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Ashley_-_Surviving_the_ER/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Ashley_-_Surviving_the_ER/jaspr_720p_Ashley_-_Surviving_the_ER.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Ashley_-_Surviving_the_ER/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Ashley_-_Surviving_the_ER/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 204,
                    name: 'Topher - Supportive People',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster:
                        'https://media.jaspr-development.com/Screen_Shot_2020-06-05_at_11.21.18_AM.png',
                    thumbnail: 'https://media.jaspr-development.com/Topher3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story/kiosk_720p_Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 179,
                    name: 'Jim - Going Home',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Jim_-_Going_Home.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Jim3x.png',
                    fpm4Transcode: 'https://media.jaspr-development.com/Jim_-_Going_Home/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Jim_-_Going_Home/jaspr_720p_Jim_-_Going_Home.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist: 'https://media.jaspr-development.com/Jim_-_Going_Home/index.m3u8',
                    dashPlaylist: 'https://media.jaspr-development.com/Jim_-_Going_Home/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 44,
                    name: 'Diana - Going Home',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Diana_-_Going_Home.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Diana3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Diana_-_Going_Home/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Diana_-_Going_Home/jaspr_720p_Diana_-_Going_Home.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Diana_-_Going_Home/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Diana_-_Going_Home/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 185,
                    name: 'Ursula - Going Home',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Ursula_-_Lethal_Means.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Ursula3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Ursula_-_Lethal_Means/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Ursula_-_Lethal_Means/jaspr_720p_Ursula_-_Lethal_Means.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Ursula_-_Lethal_Means/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Ursula_-_Lethal_Means/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 155,
                    name: 'Emmy - Going Home',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Emmy_-_Going_Home.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Emmy3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Emmy_-_Going_Home/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Emmy_-_Going_Home/jaspr_720p_Emmy_-_Going_Home.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist: 'https://media.jaspr-development.com/Emmy_-_Going_Home/index.m3u8',
                    dashPlaylist: 'https://media.jaspr-development.com/Emmy_-_Going_Home/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 170,
                    name: 'Ashley - Going Home',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Ashley_-_Going_HomeV2.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Ashley3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Ashley_-_Going_HomeV2/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Ashley_-_Going_HomeV2/jaspr_720p_Ashley_-_Going_HomeV2.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Ashley_-_Going_HomeV2/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Ashley_-_Going_HomeV2/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 6,
                    name: 'Kelechi - Going Home',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Kelechi_-_Going_HomeV2.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Kelechi3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Kelechi_-_Going_HomeV2/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Kelechi_-_Going_HomeV2/jaspr_720p_Kelechi_-_Going_HomeV2.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Kelechi_-_Going_HomeV2/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Kelechi_-_Going_HomeV2/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 51,
                    name: 'Lisa - Going Home',
                    description: '',
                    fileField: 'https://media.jaspr-development.com/Lisa_-_Going_Home.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Lisa3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Lisa_-_Going_Home/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Lisa_-_Going_Home/jaspr_720p_Lisa_-_Going_Home.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist: 'https://media.jaspr-development.com/Lisa_-_Going_Home/index.m3u8',
                    dashPlaylist: 'https://media.jaspr-development.com/Lisa_-_Going_Home/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 163,
                    name: 'Beth - What I Do to Stay Well',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Beth_-_What_I_Do_to_Stay_WellNov25.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Beth3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Beth_-_What_I_Do_to_Stay_WellNov25/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Beth_-_What_I_Do_to_Stay_WellNov25/jaspr_720p_Beth_-_What_I_Do_to_Stay_WellNov25.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Beth_-_What_I_Do_to_Stay_WellNov25/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Beth_-_What_I_Do_to_Stay_WellNov25/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 182,
                    name: 'Jim - What I Do to Stay Well',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Jim_-_What_I_do_to_Stay_Well.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Jim3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Jim_-_What_I_do_to_Stay_Well/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Jim_-_What_I_do_to_Stay_Well/jaspr_720p_Jim_-_What_I_do_to_Stay_Well.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Jim_-_What_I_do_to_Stay_Well/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Jim_-_What_I_do_to_Stay_Well/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 53,
                    name: 'Diana - What I Do to Stay Well',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Diana_-_What_I_do_to_Stay_Well.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Diana3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Diana_-_What_I_do_to_Stay_Well/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Diana_-_What_I_do_to_Stay_Well/jaspr_720p_Diana_-_What_I_do_to_Stay_Well.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Diana_-_What_I_do_to_Stay_Well/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Diana_-_What_I_do_to_Stay_Well/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 171,
                    name: 'Emmy - What I Do to Stay Well',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Emmy_-_What_I_do_to_Stay_Well.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Emmy3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Emmy_-_What_I_do_to_Stay_Well/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Emmy_-_What_I_do_to_Stay_Well/jaspr_720p_Emmy_-_What_I_do_to_Stay_Well.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Emmy_-_What_I_do_to_Stay_Well/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Emmy_-_What_I_do_to_Stay_Well/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 11,
                    name: 'Topher - What I Do to Stay Well',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Topher_-_What_I_Do_to_Stay_Well.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Topher3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Topher_-_What_I_Do_to_Stay_Well/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Topher_-_What_I_Do_to_Stay_Well/jaspr_720p_Topher_-_What_I_Do_to_Stay_Well.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Topher_-_What_I_Do_to_Stay_Well/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Topher_-_What_I_Do_to_Stay_Well/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 10,
                    name: 'Ashley - What I Do to Stay Well',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Ashley_-_What_I_Do_to_Stay_Well.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Ashley3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Ashley_-_What_I_Do_to_Stay_Well/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Ashley_-_What_I_Do_to_Stay_Well/jaspr_720p_Ashley_-_What_I_Do_to_Stay_Well.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Ashley_-_What_I_Do_to_Stay_Well/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Ashley_-_What_I_Do_to_Stay_Well/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
                {
                    id: 167,
                    name: 'Thai - What I Do to Stay Well',
                    description: '',
                    fileField:
                        'https://media.jaspr-development.com/Thai_-_What_I_Do_to_Stay_Well.mp4',
                    subtitleFile: null,
                    transcript: '',
                    poster: null,
                    thumbnail: 'https://media.jaspr-development.com/Thai3x.png',
                    fpm4Transcode:
                        'https://media.jaspr-development.com/Thai_-_What_I_Do_to_Stay_Well/index.mpd',
                    mp4Transcode:
                        'https://media.jaspr-development.com/Thai_-_What_I_Do_to_Stay_Well/jaspr_720p_Thai_-_What_I_Do_to_Stay_Well.mp4',
                    mp3Transcode: null,
                    tips: '',
                    completionTime: null,
                    hlsPlaylist:
                        'https://media.jaspr-development.com/Thai_-_What_I_Do_to_Stay_Well/index.m3u8',
                    dashPlaylist:
                        'https://media.jaspr-development.com/Thai_-_What_I_Do_to_Stay_Well/index.mpd',
                    duration: null,
                    fileType: 'video',
                    tags: [],
                },
            ],
            tags: {},
            storiesFetched: true,
            ratingsFetched: false,
            videoRatings: [],
        },
    },
};
