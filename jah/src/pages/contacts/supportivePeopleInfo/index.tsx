import React, { useContext, useEffect } from 'react';
import VideoListContainer from 'components/VideoListContainer';
import StoreContext from 'state/context/store';
import { addAction, actionNames } from 'state/actions/analytics';
import Menu from 'components/Menu';
import TitleMenu from 'components/TitleMenu';

const HotlineInfo = () => {
    const [store] = useContext(StoreContext);
    const { media } = store.media;
    const { supportivePeople } = media;
    const { hls, dash, poster, video } = supportivePeople;

    useEffect(() => {
        addAction(actionNames.JAH_ARRIVE_PEOPLE_MORE);
    }, []);

    return (
        <>
            <TitleMenu label="More: Supportive People" />
            <VideoListContainer
                poster={poster}
                dashPlaylist={dash}
                hlsPlaylist={hls}
                mp4Transcode={video}
                label="Learn more about getting help from supportive people"
                items={[
                    { label: 'Conversation Starters', link: '/jah-conversation-starters' },
                    {
                        label: 'Shared Stories: Supportive People',
                        link: '/jah-contacts/shared-stories',
                    },
                ]}
            />
            <Menu selected="contacts" />
        </>
    );
};

export default HotlineInfo;
