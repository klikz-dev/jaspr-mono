import React from 'react';
import Styled from 'styled-components/native';
import Hamburger from 'components/Hamburger';
import { actionNames } from 'state/actions/analytics';
import { SafeAreaView } from 'react-native';

const StyledContainer = Styled.View`
    background-color: #2f344f;
    flex-direction: column;
    align-items: flex-end;
    padding-right: 0px;
    width: 100%;
    height: 54px;
`;

const Menu = () => {
    return (
        <SafeAreaView style={{ backgroundColor: 'rgba(48,52,78,1)' }}>
            <StyledContainer>
                <Hamburger />
            </StyledContainer>
        </SafeAreaView>
    );
};

export default Menu;
