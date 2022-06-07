import React from 'react';
import Styled from 'styled-components/native';
import VideoPlayer from 'components/Videos/Player';
import ListContainer from 'components/ListContainer';

const Container = Styled.View`flex: 1;`;

interface VideoListContainerProps {
    mp4Transcode: string;
    hlsPlaylist: string;
    dashPlaylist: string;
    items: { label: string; link: string }[];
    poster: string;
    label?: string;
}

const VideoListContainer = ({
    mp4Transcode,
    hlsPlaylist,
    dashPlaylist,
    items,
    poster,
    label = '',
}: VideoListContainerProps) => {
    return (
        <Container>
            <VideoPlayer
                mp4Transcode={mp4Transcode}
                hlsPlaylist={hlsPlaylist}
                fpm4Transcode={dashPlaylist}
                poster={poster}
                name={label}
            />
            <ListContainer fill items={items} />
        </Container>
    );
};

export default VideoListContainer;
