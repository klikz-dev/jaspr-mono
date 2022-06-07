import React from 'react';
import { SafeAreaView } from 'react-native';
import { useHistory } from 'lib/router';
import Styled from 'styled-components/native';
import Hamburger from 'components/Hamburger';

const Background = Styled.View`
    background-color: #2F344F;
`;
const Container = Styled.View`
    position: relative;
    flex-direction: row;
    height: 50px;
    align-items: center;
    justify-content: space-between;
    
`;
const BackButton = Styled.TouchableOpacity``;
const BackButtonText = Styled.Text`
    width: 50px;
    color:  #FFFEFE;
    font-size: 34px;
    margin-top: -10px;
    margin-left: 30px;
`;
const Title = Styled.Text`
    flex: 1;
    color: #FFFEFE;
    font-size: 16px;
    font-weight: 500;
    letter-spacing: 0.15px;
    text-align: center;
    margin-right: auto;
    margin-left: auto;
`;
const HamburgerContainer = Styled.View`
    margin-top: -50px;
    width: 50px;
    position: relative;
`;

interface TitleMenuProps {
    goBack?: () => void;
    label: string;
}

const TitleMenu = ({ goBack, label }: TitleMenuProps): JSX.Element => {
    const history = useHistory();
    return (
        <Background>
            <SafeAreaView>
                <Container>
                    <BackButton onPress={goBack ? goBack : history.goBack}>
                        <BackButtonText>‹</BackButtonText>
                    </BackButton>
                    <Title numberOfLines={1}>{label}</Title>
                    <HamburgerContainer>
                        <Hamburger inline />
                    </HamburgerContainer>
                </Container>
            </SafeAreaView>
        </Background>
    );
};

export default TitleMenu;
