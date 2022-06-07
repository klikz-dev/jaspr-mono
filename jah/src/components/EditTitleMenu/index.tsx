import React from 'react';
import { SafeAreaView } from 'react-native';
import Styled from 'styled-components/native';
import { useHistory } from 'lib/router';

const Background = Styled.View`
    background-color: #5C6597;
`;
const Container = Styled.View`
    position: relative;
    flex-direction: row;
    height: 60px;
    align-items: center;
    justify-content: space-between;
    padding-horizontal: 21px;
`;
const Button = Styled.TouchableOpacity``;
const BackButtonText = Styled.Text`
    font-size: 16px;
    letter-spacing: 0.15px;
    line-height: 20px;
    color: #FFFEFE;
`;
const SaveButtonText = Styled.Text`
    font-size: 20px;
    letter-spacing: 0.165px;
    line-height: 20px;
    color: #FFFEFE;
`;
const Title = Styled.Text`
    flex: 1;
    color: #FFFEFE;
    font-size: 20px;
    line-height: 20px;
    letter-spacing: 0.15px;
    text-align: center;
`;

interface TitleMenuProps {
    cancel?: () => void;
    label: string;
    save: () => void;
}

const EditTitleMenu = ({ cancel, label, save }: TitleMenuProps): React.ReactNode => {
    const history = useHistory();
    return (
        <Background>
            <SafeAreaView>
                <Container>
                    <Button onPress={cancel ? cancel : history.goBack}>
                        <BackButtonText>Cancel</BackButtonText>
                    </Button>
                    <Title numberOfLines={1}>{label}</Title>
                    <Button onPress={save}>
                        <SaveButtonText>Save</SaveButtonText>
                    </Button>
                </Container>
            </SafeAreaView>
        </Background>
    );
};

export default EditTitleMenu;
