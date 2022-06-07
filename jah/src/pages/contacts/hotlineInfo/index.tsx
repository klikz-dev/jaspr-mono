import React, { useContext } from 'react';
import VideoListContainer from 'components/VideoListContainer';
import Menu from 'components/Menu';
import TitleMenu from 'components/TitleMenu';
import StoreContext from 'state/context/store';

const HotlineInfo = () => {
    const [store] = useContext(StoreContext);
    const { media } = store.media;
    const { nationalHotline } = media;
    const { hls, dash, poster, video } = nationalHotline;

    return (
        <>
            <TitleMenu label="More: National Hotline" />
            <VideoListContainer
                poster={poster}
                hlsPlaylist={hls}
                dashPlaylist={dash}
                mp4Transcode={video}
                items={[
                    { label: 'What to Expect', link: '/jah-contacts/hotline-info/what-to-expect' },
                    {
                        label: 'Common Concerns',
                        link: '/jah-contacts/hotline-info/common-concerns',
                    },
                    {
                        label: 'Shared Stories: Crisis Lines',
                        link: '/jah-contacts/hotline-info/crisis-lines',
                    },
                ]}
            />
            <Menu selected="contacts" />
        </>
    );
};

export default HotlineInfo;
