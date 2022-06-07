import React from 'react';

import Menu from 'components/HamburgerMenu';
import JahMenu from 'components/Menu';
import Styled from 'styled-components/native';
import SharedStories from 'components/Stories';
import styles from './index.module.scss';

const StyledContainer = Styled.View`${styles.container};`;

const Stories = () => {
    return (
        <StyledContainer style={{ flexDirection: 'column' }}>
            <Menu selectedItem="stories" hideLogo />
            <SharedStories />
            <JahMenu selected="stories" />
        </StyledContainer>
    );
};

export default Stories;
