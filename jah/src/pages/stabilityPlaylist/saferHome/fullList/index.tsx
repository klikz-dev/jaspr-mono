import React, { useContext } from 'react';
import { useHistory } from 'lib/router';
import StoreContext from 'state/context/store';
import Styled from 'styled-components/native';
import TitleMenu from 'components/TitleMenu';
import DistressButton from 'components/DistressButton';
import TopContainer from 'components/TopContainer';
import Menu from 'components/Menu/index';
import Item from '../../item';

const Container = Styled.View`flex: 1; background-color: #41476A;`;
const List = Styled.ScrollView`
    background-color: #2F344F;
`;
const Labels = Styled.View`
    flex-direction: row;
    flex-wrap: wrap;
`;
const EditButton = Styled.TouchableOpacity`
    margin-top: auto;
    margin-horizontal: auto;
`;
const EditText = Styled.Text`
    font-size: 20px;
    line-height: 25px;
    text-align: center;
    letter-spacing: 0.15px;
    text-decoration: underline;
    color: #FFFEFE;
`;

const SaferHomeFullList = () => {
    const history = useHistory();
    const [store] = useContext(StoreContext);
    const { crisisStabilityPlan } = store;
    const {
        strategiesCustom,
        strategiesFirearm,
        strategiesGeneral,
        strategiesMedicine,
        strategiesOther,
        strategiesPlaces,
    } = crisisStabilityPlan;
    return (
        <Container>
            <TitleMenu label="Making Home Safer" />
            <List>
                <TopContainer title="General">
                    <Labels>
                        {strategiesGeneral?.map((strategy) => (
                            <Item key={strategy} label={strategy} />
                        ))}
                    </Labels>
                </TopContainer>

                <TopContainer title="Firearm">
                    <Labels>
                        {strategiesFirearm?.map((strategy) => (
                            <Item key={strategy} label={strategy} />
                        ))}
                    </Labels>
                </TopContainer>

                <TopContainer title="Medicine">
                    <Labels>
                        {strategiesMedicine?.map((strategy) => (
                            <Item key={strategy} label={strategy} />
                        ))}
                    </Labels>
                </TopContainer>

                <TopContainer title="Places">
                    <Labels>
                        {strategiesPlaces?.map((strategy) => (
                            <Item key={strategy} label={strategy} />
                        ))}
                    </Labels>
                </TopContainer>

                <TopContainer title="Other">
                    <Labels>
                        {strategiesOther?.map((strategy) => (
                            <Item key={strategy} label={strategy} />
                        ))}
                    </Labels>
                </TopContainer>

                <TopContainer title="Custom">
                    <Labels>
                        {strategiesCustom?.map((strategy) => (
                            <Item key={strategy} label={strategy} />
                        ))}
                    </Labels>
                </TopContainer>

                <EditButton
                    onPress={() => history.push('/jah-stability-playlist/making-home-safer/edit')}
                >
                    <EditText>Edit Make Home Safer</EditText>
                </EditButton>
            </List>

            <DistressButton />
            <Menu selected="stability-playlist" />
        </Container>
    );
};

export default SaferHomeFullList;
