import React from 'react';
import { SafeAreaView } from 'react-native';
import Styled from 'styled-components/native';

const TouchableWithoutFeedback = Styled.TouchableWithoutFeedback``;
const Container = Styled.View`
    flex: 1;
    background-color: rgba(118, 123, 150, 0.95);
`;
const CloseText = Styled.Text`
    font-size: 35px;
    color: rgba(255,255,255,1);
`;
const CloseButton = Styled.TouchableOpacity`
    position: absolute;
    right: 40px;
    top: 45px;
    z-index: 1;
`;
const ContentContainer = Styled.View`
    position: relative;
    margin-top: 83px;
    margin-horizontal: 37px;
    background-color: #fff;
    max-height: 80%;
    border-radius: 9.5px;
    overflow: hidden;
`;

const HeaderContainer = Styled.View`
    background-color: #2F344F;
    padding-horizontal: 20px;
    padding-vertical: 30px;
`;
const HeaderText = Styled.Text`
    opacity: 0.9;
    color: #FFFFFF;
    font-size: 20px;
    letter-spacing: 0;
    text-align: center;
`;
const Body = Styled.ScrollView`
    height: 100%;
`;
const ContentHeader = Styled.Text`
    font-size: 16px;
    font-weight: 600;
    line-height: 24px;
    padding-vertical: 10px;
    padding-horizontal: 21px;
    color: rgba(47,51,80,1);
`;
const ContentBody = Styled.Text`
    padding-horizontal: 21px;
    font-size: 16px;
    color: rgba(47,51,80,1);
    line-height: 24px;
    letter-spacing: 0.04px;
`;
const BodyText = Styled.Text`
    padding-horizontal: 21px;
    padding-vertical: 30px;
    color: rgba(47,51,80,1);
    font-size: 16px;
    font-weight: 300;
    letter-spacing: 0.04px;
    line-height: 24px;
`;
const View = Styled.View``;

interface InfoModalProps {
    title: string;
    content?: { header: string; body: string }[];
    close: () => void;
    body?: string;
}

const InfoModal = ({ close, title, body, content }: InfoModalProps): JSX.Element => {
    return (
        <SafeAreaView style={{ flex: 1 }}>
            <TouchableWithoutFeedback onPress={close}>
                <Container>
                    <CloseButton
                        onPress={close}
                        hitSlop={{ top: 10, bottom: 10, right: 10, left: 10 }}
                    >
                        <CloseText>⨉</CloseText>
                    </CloseButton>
                    <TouchableWithoutFeedback>
                        <ContentContainer>
                            <HeaderContainer>
                                <HeaderText numberOfLines={2}>{title}</HeaderText>
                            </HeaderContainer>
                            <Body>
                                <TouchableWithoutFeedback>
                                    <View onStartShouldSetResponder={() => true}>
                                        {Boolean(body) && <BodyText>{body}</BodyText>}
                                        {Boolean(content) &&
                                            content !== undefined &&
                                            content.map((section) => (
                                                <React.Fragment key={section.header}>
                                                    <ContentHeader>{section.header}</ContentHeader>
                                                    <ContentBody>{section.body}</ContentBody>
                                                </React.Fragment>
                                            ))}
                                    </View>
                                </TouchableWithoutFeedback>
                            </Body>
                        </ContentContainer>
                    </TouchableWithoutFeedback>
                </Container>
            </TouchableWithoutFeedback>
        </SafeAreaView>
    );
};

export default InfoModal;
