import React from 'react';
import { useWindowDimensions } from 'react-native';
import { useHistory } from 'lib/router';
import { modelName } from 'expo-device';
import Styled from 'styled-components/native';
import styles from './index.module.scss';

// TODO add 1x and 2x assets
import IconHome from './icons/home.png';
import IconStories from './icons/stories.png';
import IconStability from './icons/stabilityplan.png';
import IconSkills from './icons/skills.png';
import IconContacts from './icons/contacts.png';
import IconHomeSelected from './icons/home-selected.png';
import IconStoriesSelected from './icons/stories-selected.png';
import IconStabilitySelected from './icons/stabilityplan-selected.png';
import IconSkillsSelected from './icons/skills-selected.png';
import IconContactsSelected from './icons/contacts-selected.png';

const SafeAreaBuffer = Styled.View<{ hasHomeIndicator: boolean }>`
    padding-bottom: ${({ hasHomeIndicator }) => (hasHomeIndicator ? '15px' : 0)}
    background-color: #2f344f;`;
const Container = Styled.View<{ small: boolean }>`${styles.container}
    height: ${({ small }) => (small ? '52px' : '56px')}
    padding-horizontal: 16px;
`;
const MenuItem = Styled.TouchableOpacity`
    position: relative;
    height: 100%;
    align-items: center;
    flex-grow: 1;
    justify-content: center;
    margin-top: 8px;
`;
const MenuItemText = Styled.Text<{ selected: boolean }>`
    position: absolute;
    bottom: 5px;
    width: 100px;
    ${styles.menuItemText}
    opacity: ${({ selected }) => (selected ? 1 : 0)};
    color: ${({ selected }) => (selected ? 'rgba(248, 248, 248, 1)' : 'rgba(248, 248, 248, 0.7)')};
    font-size: ${({ selected }) => (selected ? '10px' : '9px')};
    font-weight: ${({ selected }) => (selected ? '400' : '100')};
`;

const Image = Styled.Image`
    ${styles.icon}
    margin-bottom: 20px;
`;

interface MenuProps {
    selected: 'home' | 'stories' | 'stability-playlist' | 'skills' | 'contacts';
}

const Menu = ({ selected }: MenuProps): JSX.Element => {
    const history = useHistory();
    const windowHeight = useWindowDimensions().height;

    const hasHomeIndicator = [
        'iPhone X',
        'iPhone XR',
        'iPhone XS',
        'iPhone XS Max',
        'iPhone 11',
        'iPhone 11 Pro',
        'iPhone 11 Pro Max',
        'iPhone 12',
        'iPhone 12 Pro',
        'iPhone 12 Pro Max',
    ].includes(modelName || '');

    return (
        <SafeAreaBuffer hasHomeIndicator={hasHomeIndicator}>
            <Container small={windowHeight < 750}>
                <MenuItem onPress={() => history.push('/')} style={{ marginLeft: 12 }}>
                    <Image
                        source={selected === 'home' ? IconHomeSelected : IconHome}
                        resizeMode="contain"
                    ></Image>
                    <MenuItemText selected={selected === 'home'}>Home</MenuItemText>
                </MenuItem>
                <MenuItem onPress={() => history.push('/stories')}>
                    <Image
                        source={selected === 'stories' ? IconStoriesSelected : IconStories}
                        resizeMode="contain"
                    ></Image>
                    <MenuItemText selected={selected === 'stories'}>Shared Stories</MenuItemText>
                </MenuItem>
                <MenuItem onPress={() => history.push('/jah-stability-playlist')}>
                    <Image
                        source={
                            selected === 'stability-playlist'
                                ? IconStabilitySelected
                                : IconStability
                        }
                        resizeMode="contain"
                    ></Image>
                    <MenuItemText selected={selected === 'stability-playlist'}>
                        Stability Plan
                    </MenuItemText>
                </MenuItem>
                <MenuItem onPress={() => history.push('/skills')}>
                    <Image
                        source={selected === 'skills' ? IconSkillsSelected : IconSkills}
                        resizeMode="contain"
                    ></Image>
                    <MenuItemText selected={selected === 'skills'}>
                        Comfort &amp; Skills
                    </MenuItemText>
                </MenuItem>
                <MenuItem onPress={() => history.push('/jah-contacts')} style={{ marginRight: 12 }}>
                    <Image
                        source={selected === 'contacts' ? IconContactsSelected : IconContacts}
                        resizeMode="contain"
                    ></Image>
                    <MenuItemText selected={selected === 'contacts'}>Contacts</MenuItemText>
                </MenuItem>
            </Container>
        </SafeAreaBuffer>
    );
};

export default Menu;
