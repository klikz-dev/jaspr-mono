import React, { useContext } from 'react';
import Styled from 'styled-components/native';
import { useHistory } from 'lib/router';
import HomeIcon from 'assets/homeIconOnboarding.svg';
import { completedJAHOnboarding } from 'state/actions/user';
import StoreContext from 'state/context/store';

const Container = Styled.TouchableOpacity`
    margin-top: 20px;
    margin-left: auto;
    margin-right: auto;
    height: 79px;
    width: 95px;
    align-items: center;
    justify-content: center;
    border-radius: 5px;
    background-color: #FFFEFE;
`;
const Label = Styled.Text`
    color: #000000;
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 0;
`;

const HomeButton = (): JSX.Element => {
    const history = useHistory();
    const [, dispatch] = useContext(StoreContext);

    const next = () => {
        completedJAHOnboarding(dispatch);
        history.replace('/');
    };

    return (
        <Container onPress={next}>
            <HomeIcon />
            <Label>Home</Label>
        </Container>
    );
};

export default HomeButton;
