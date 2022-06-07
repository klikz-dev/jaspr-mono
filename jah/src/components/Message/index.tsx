import React, { useContext } from 'react';
import StoreContext from 'state/context/store';
import Styled from 'styled-components/native';
import jazIcon from 'assets/jazz.png';
import jasperIcon from 'assets/jasper.png';
import styles from './message.module.css';
import { Patient } from 'state/types';

const Column = Styled.View`${styles.column}`;
const P = Styled.Text`${styles.p}`;
const Header = Styled.View`${styles.header}`;
const HeaderText = Styled.Text`${styles.headerText}`;
const Box = Styled.View`${styles.box} background-color: black;`;
const GuideProfile = Styled.View`${styles.guideProfile}`;
const GuideImage = Styled.Image`${styles.guideImage}`;
const GuideName = Styled.Text`${styles.guideName}`;
const Section = Styled.View`flex: 1; flex-shrink: 1;`;

interface Props {
    paragraphs: string[];
    header: string;
    backEnabled: boolean;
    back: () => void;
    buttons: {
        label: string;
        type: 'primary' | 'secondary';
        command: () => void;
    }[];
}

const Message = (props: Props) => {
    const [store] = useContext(StoreContext);
    const { user } = store;
    const { guide } = user as Patient;
    const { paragraphs, header } = props;

    return (
        <Column>
            {header && (
                <Header>
                    <HeaderText>{header}</HeaderText>
                </Header>
            )}
            <Box>
                <GuideProfile>
                    <GuideImage source={guide === 'Jaz' ? jazIcon : jasperIcon} />
                    <GuideName>{guide || 'Jaz'}</GuideName>
                </GuideProfile>
                <Section>
                    {paragraphs.map((paragraph) => (
                        <P key={paragraph}>{paragraph}</P>
                    ))}
                </Section>
            </Box>
        </Column>
    );
};

export default Message;
