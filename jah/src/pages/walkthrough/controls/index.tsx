import React from 'react';
import Styled from 'styled-components/native';
import { useHistory } from 'lib/router';
import TopShadow from 'components/TopShadow';
import playlistIcon from 'assets/playlist.png';

const ControlRow = Styled.View`
    width: 100%;
    padding-bottom: 15px;
    padding-top: 20px;
    flex-direction: row;
    justify-content: space-between;
    background-color: #2F344F;
`;
const NextButton = Styled.TouchableOpacity`
    flex-direction: row;
    align-items: center;
    padding-right: 26px;
`;
const PlaylistButton = Styled.TouchableOpacity`padding-left: 26px;`;
const PlaylistIcon = Styled.Image``;

const NextText = Styled.Text`
    color: #8F97CE;
    font-size: 24px;
    letter-spacing: 0;
`;
const NextChevron = Styled.Text`
    margin-left: 17px;
    margin-top: -2px;
    color: #8F97CE;
    font-size: 35px;
`;

interface ControlsProps {
    setStepIdx: (state: (prevState: number) => number) => void;
    lastStep?: boolean;
    setShowMenu: (show: boolean) => void;
}

const Controls = ({ setStepIdx, lastStep, setShowMenu }: ControlsProps) => {
    const history = useHistory();
    return (
        <ControlRow>
            <TopShadow />
            <PlaylistButton onPress={() => setShowMenu(true)}>
                <PlaylistIcon source={playlistIcon} />
            </PlaylistButton>
            <NextButton
                onPress={
                    lastStep
                        ? () => history.goBack()
                        : () => setStepIdx((currentIdx) => currentIdx + 1)
                }
            >
                <NextText>Next</NextText>
                <NextChevron>›</NextChevron>
            </NextButton>
        </ControlRow>
    );
};

export default Controls;
