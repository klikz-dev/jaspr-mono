import { action } from '@storybook/addon-actions';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import Video from '.';

export default {
    title: 'ConversationalUi/Video',
    component: Video,
    argTypes: {},
} as ComponentMeta<typeof Video>;

const Template: ComponentStory<typeof Video> = (args) => {
    const setAnswered = action('setAnswered');
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
                width: '100%',
            }}
        >
            <Video
                answered={false}
                next={() => action('Next')}
                setAnswered={setAnswered}
                name="Distract: Name Things"
                poster="https://media.jaspr-development.com/helpingCareTeam.png"
                mp4Transcode="https://media.jaspr-development.com/Topher_-_Skills_-_Naming_Things/jaspr_720p_Topher_-_Skills_-_Naming_Things.mp4"
                hlsPlaylist="https://media.jaspr-development.com/Topher_-_Skills_-_Naming_Things/index.m3u8"
                dashPlaylist="https://media.jaspr-development.com/Topher_-_Skills_-_Naming_Things/index.mpd"
            />
        </div>
    );
};

export const Default = Template.bind({});
