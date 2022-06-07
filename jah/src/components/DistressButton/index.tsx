import React from 'react';
import { useHistory } from 'lib/router';
import Styled from 'styled-components/native';
import HeartSource from 'assets/heartplus.png';

const MoreButton = Styled.TouchableOpacity`
    height: 56px;
    flex-direction: row;
    align-items: center;
    background-color: #171A27;
`;
const MoreText = Styled.Text`
    color: #FFFEFE;
    font-size: 16px;
    margin-left: 13px;
    margin-right: auto;
`;
const RightPointer = Styled.Text`
    font-size: 35px;
    color: #fff;
    margin-right: 20px;
    line-height: 35px;
`;
const HeartImage = Styled.Image`
    margin-left: 22px;
    width: 30px;
    height: 28px`;

const DistressButton = (): JSX.Element => {
    const history = useHistory();
    return (
        <MoreButton onPress={() => history.push('/jah-walkthrough')}>
            <HeartImage source={HeartSource} />
            <MoreText>Distress Survival Guide</MoreText>
            <RightPointer>›</RightPointer>
        </MoreButton>
    );
};

export default DistressButton;
