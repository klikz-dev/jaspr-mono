import React from 'react';
import { Platform } from 'react-native';
import { useHistory } from 'lib/router';
import Styled from 'styled-components/native';
import styles from './index.module.css';

const Container = Styled.View<{ fill: boolean; noRoundedCorners: boolean }>`
    ${({ fill }) => (fill ? 'flex: 1' : '')}
    flex-shrink: 0;
    background-color: #2F344F;
    border-top-left-radius: ${({ fill, noRoundedCorners }) =>
        fill || noRoundedCorners ? '0px' : '8px'};
    border-top-right-radius: ${({ fill, noRoundedCorners }) =>
        fill || noRoundedCorners ? '0px' : '8px'};
    margin-top: auto;
    padding-vertical: 13px;
    background-color: #2F344F;
`;
const List = Styled.View``;
const Item = Styled.TouchableOpacity<{ isIOS: boolean }>`
    ${styles.listItem}
    ${({ isIOS }) =>
        isIOS
            ? `
        shadow-color: #000;
        shadow-offset: 2px 4px;
        shadowOpacity: 0.5;
        shadowRadius: 10px;
    `
            : `
        elevation: 7;
    `}
`;
const ListText = Styled.Text`${styles.listItemText}`;

const ListItem = ({ link, label }: { link: string; label: string }) => {
    const history = useHistory();
    return (
        <Item onPress={() => history.push(link)} isIOS={Platform.OS === 'ios'}>
            <ListText>{label}</ListText>
        </Item>
    );
};

interface ListContainerProps {
    fill?: boolean;
    noRoundedCorners?: boolean;
    items: { label: string; link: string }[];
}

const ListContainer = ({ fill = false, noRoundedCorners = false, items }: ListContainerProps) => {
    return (
        <Container fill={fill} noRoundedCorners={noRoundedCorners}>
            <List>
                {items.map(({ label, link }) => (
                    <ListItem key={label} label={label} link={link} />
                ))}
            </List>
        </Container>
    );
};

export default ListContainer;
