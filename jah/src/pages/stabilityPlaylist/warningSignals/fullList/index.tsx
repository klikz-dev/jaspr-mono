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

const WarningSignalsFullList = () => {
    const history = useHistory();
    const [store] = useContext(StoreContext);
    const { crisisStabilityPlan } = store;
    const { wsTop, wsActions, wsFeelings, wsStressors, wsThoughts } = crisisStabilityPlan;
    return (
        <Container>
            <TitleMenu label="My Warning Signals" />
            <List>
                <TopContainer title="Stressors">
                    <Labels>
                        {(wsStressors || []).map((strategy) => (
                            <Item
                                key={strategy}
                                label={strategy}
                                showDot={(wsTop || []).includes(strategy)}
                            />
                        ))}
                    </Labels>
                </TopContainer>

                <TopContainer title="Thoughts">
                    <Labels>
                        {(wsThoughts || []).map((strategy) => (
                            <Item
                                key={strategy}
                                label={strategy}
                                showDot={(wsTop || []).includes(strategy)}
                            />
                        ))}
                    </Labels>
                </TopContainer>

                <TopContainer title="Feelings">
                    <Labels>
                        {(wsFeelings || []).map((strategy) => (
                            <Item
                                key={strategy}
                                label={strategy}
                                showDot={(wsTop || []).includes(strategy)}
                            />
                        ))}
                    </Labels>
                </TopContainer>

                <TopContainer title="Actions">
                    <Labels>
                        {(wsActions || []).map((strategy) => (
                            <Item
                                key={strategy}
                                label={strategy}
                                showDot={(wsTop || []).includes(strategy)}
                            />
                        ))}
                    </Labels>
                </TopContainer>

                <EditButton
                    onPress={() => history.push('/jah-stability-playlist/warning-signals/edit')}
                >
                    <EditText>Edit Warning Signs</EditText>
                </EditButton>
            </List>
            <DistressButton />
            <Menu selected="stability-playlist" />
        </Container>
    );
};

export default WarningSignalsFullList;
