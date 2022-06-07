import React, { useContext } from 'react';
import Styled from 'styled-components/native';
import StoreContext from 'state/context/store';
import avatarJaz from 'assets/jazz.png';
import avatarJasper from 'assets/jasper.png';
import { Patient } from 'state/types';

const Chat = Styled.View`
    width: 100%;
    justify-content: center;
    padding: 28px;
    background-color: #ECEEF5;
`;
const Avatar = Styled.Image`
    width: 90px;
    height: 90px;
`;
const TextBox = Styled.View`
    margin-top: 15px;
    background-color: #FFFEFE;
    padding: 20px;
`;
const Text = Styled.Text`
    font-size: 22px;
    letter-spacing: 0;
    line-height: 26px;
`;

const Triangle = Styled.View`
    position: absolute;
    top: -12px;
    width: 0;
    height: 0;
    background-color: transparent;
    border-style: solid;
    border-top-width: 0;
    border-right-width: 35px;
    border-bottom-width: 12px;
    border-left-width: 0;
    border-top-color: transparent;
    border-right-color: transparent;
    border-bottom-color: #ffffff;
    border-left-color: transparent;
`;

interface Props {
    value: string;
}

const Guide = ({ value }: Props) => {
    const [store] = useContext(StoreContext);
    const { user } = store;
    const { guide } = user as Patient;

    return (
        <Chat>
            <Avatar source={guide === 'Jasper' ? avatarJasper : avatarJaz} />
            <TextBox>
                <Triangle />
                <Text>{value}</Text>
            </TextBox>
        </Chat>
    );
};

export default Guide;
