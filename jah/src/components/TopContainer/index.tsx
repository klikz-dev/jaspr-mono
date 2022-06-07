import React from 'react';
import { useHistory } from 'lib/router';
import Styled from 'styled-components/native';
import Pencil from 'assets/pencilWhite.svg';
import styles from './index.module.css';

const Container = Styled.View`${styles.container}
    shadow-color: #000;
    shadow-offset: 2px 4px;
    shadowOpacity: 0.5;
    shadowRadius: 10px;
    elevation: 7;
`;
const Header = Styled.View`${styles.header}`;
const Title = Styled.Text`${styles.title}`;
const Link = Styled.TouchableOpacity`${styles.link}`;

const Dot = Styled.View`
    width: 5px;
    height: 5px;
    border-radius: 2.5px;
    background-color: rgba(255,255,255,1);
`;

const Content = Styled.View`${styles.content}`;
const MoreContainer = Styled.TouchableOpacity`
    border-top-width: 1px;
    border-top-color: #5c6597;
    align-items: center;
    justify-content: center;
    padding-vertical: 18px;
`;
const MoreText = Styled.Text`
    color: #C9CFD8;
    font-size: 18px;
    font-weight: 500;
    letter-spacing: 0.14px;
    line-height: 21px;
    text-align: center;
`;
interface TopContainerProps {
    title: string;
    moreLabel?: string;
    moreLink?: string;
    link?: string;
    showPencil?: boolean;
    children: React.ReactNode;
}

const TopContainer = ({
    title,
    moreLabel,
    moreLink,
    link,
    showPencil = false,
    children,
}: TopContainerProps) => {
    const history = useHistory();

    return (
        <Container>
            <Header>
                <Title>{title}</Title>
                {Boolean(link) && link !== undefined && (
                    <Link onPress={() => history.push(link)}>
                        {showPencil && <Pencil />}
                        {!showPencil && (
                            <>
                                <Dot />
                                <Dot />
                                <Dot />
                            </>
                        )}
                    </Link>
                )}
            </Header>
            <Content>{children}</Content>
            {Boolean(moreLabel) && (
                <MoreContainer
                    onPress={() => (Boolean(moreLink) ? history.push(moreLink) : () => {})}
                >
                    <MoreText>{moreLabel}</MoreText>
                </MoreContainer>
            )}
        </Container>
    );
};

export default TopContainer;
