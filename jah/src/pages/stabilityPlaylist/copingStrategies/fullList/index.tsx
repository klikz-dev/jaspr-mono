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

const CopingStrategiesFullList = () => {
    const history = useHistory();
    const [store] = useContext(StoreContext);
    const { crisisStabilityPlan } = store;
    const { copingTop, copingBody, copingCourage, copingDistract, copingHelpOthers, copingSenses } =
        crisisStabilityPlan;
    return (
        <Container>
            <TitleMenu label="My Coping Strategies" />
            <List>
                <TopContainer title="Body Sensation Strategies">
                    <Labels>
                        {copingBody?.map((strategy) => (
                            <Item
                                key={strategy}
                                label={strategy}
                                showDot={(copingTop || []).includes(strategy)}
                            />
                        ))}
                    </Labels>
                </TopContainer>

                <TopContainer title="Distractions">
                    <Labels>
                        {(copingDistract || []).map((strategy) => (
                            <Item
                                key={strategy}
                                label={strategy}
                                showDot={(copingTop || []).includes(strategy)}
                            />
                        ))}
                    </Labels>
                </TopContainer>

                <TopContainer title="Helping Others">
                    <Labels>
                        {(copingHelpOthers || []).map((strategy) => (
                            <Item
                                key={strategy}
                                label={strategy}
                                showDot={(copingTop || []).includes(strategy)}
                            />
                        ))}
                    </Labels>
                </TopContainer>

                <TopContainer title="Courage">
                    <Labels>
                        {copingCourage?.map((strategy) => (
                            <Item
                                key={strategy}
                                label={strategy}
                                showDot={(copingTop || []).includes(strategy)}
                            />
                        ))}
                    </Labels>
                </TopContainer>

                <TopContainer title="Senses">
                    <Labels>
                        {(copingSenses || []).map((strategy) => (
                            <Item
                                key={strategy}
                                label={strategy}
                                showDot={(copingTop || []).includes(strategy)}
                            />
                        ))}
                    </Labels>
                </TopContainer>
                <EditButton
                    onPress={() => history.push('/jah-stability-playlist/coping-strategies/edit')}
                >
                    <EditText>Edit Coping Strategies</EditText>
                </EditButton>
            </List>
            <DistressButton />
            <Menu selected="stability-playlist" />
        </Container>
    );
};

export default CopingStrategiesFullList;
