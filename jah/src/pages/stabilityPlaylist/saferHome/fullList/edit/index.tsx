import React, { useContext, useEffect, useState } from 'react';
import { KeyboardAvoidingView, Platform } from 'react-native';
import Styled from 'styled-components/native';
import { useHistory } from 'lib/router';
import EditTitleMenu from 'components/EditTitleMenu';
import BubbbleQuestion from 'components/BubbleQuestion';
import Menu from 'components/Menu/index';
import StoreContext from 'state/context/store';
import { saveCrisisStabilityPlan } from 'state/actions/crisisStabilityPlan';
import Segment from 'lib/segment';

const Container = Styled.View`flex: 1; background-color: #41476A;`;

const List = Styled.ScrollView`
    background-color: #2F344F;
`;

const SaferHomeEdit = () => {
    const history = useHistory();
    const [store, dispatch] = useContext(StoreContext);
    const { crisisStabilityPlan } = store;
    const {
        strategiesCustom,
        strategiesFirearm,
        strategiesGeneral,
        strategiesMedicine,
        strategiesOther,
        strategiesPlaces,
    } = crisisStabilityPlan;

    const [editedAnswers, setEditedAnswers] = useState({
        strategiesCustom: strategiesCustom || [],
        strategiesFirearm: strategiesFirearm || [],
        strategiesGeneral: strategiesGeneral || [],
        strategiesMedicine: strategiesMedicine || [],
        strategiesOther: strategiesOther || [],
        strategiesPlaces: strategiesPlaces || [],
    });

    useEffect(() => {
        setEditedAnswers({
            strategiesCustom: strategiesCustom || [],
            strategiesFirearm: strategiesFirearm || [],
            strategiesGeneral: strategiesGeneral || [],
            strategiesMedicine: strategiesMedicine || [],
            strategiesOther: strategiesOther || [],
            strategiesPlaces: strategiesPlaces || [],
        });
    }, [
        strategiesCustom,
        strategiesFirearm,
        strategiesGeneral,
        strategiesMedicine,
        strategiesOther,
        strategiesPlaces,
    ]);

    const save = () => {
        saveCrisisStabilityPlan(dispatch, editedAnswers);
        Segment.track('stability plan edited from JAH', { page: 'safer-home' });
        history.goBack();
    };

    return (
        <Container>
            <EditTitleMenu label="Edit Making Home Safer" save={save} />
            <KeyboardAvoidingView
                style={{ flex: 1 }}
                behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            >
                <List>
                    <BubbbleQuestion
                        title="General"
                        answerKey="strategiesGeneral"
                        editedAnswers={editedAnswers}
                        setEditedAnswers={setEditedAnswers}
                        options={[
                            'Dispose of method',
                            'Store with trusted person',
                            'Store in a lock box, give key to a trusted person',
                            'Plan how to avoid the method (i.e. not go to dangerous location)',
                        ]}
                    />

                    <BubbbleQuestion
                        title="Firearm"
                        answerKey="strategiesFirearm"
                        editedAnswers={editedAnswers}
                        setEditedAnswers={setEditedAnswers}
                        options={[
                            'Family, friend, or neighbor',
                            'Gun dealers',
                            'Shooting range',
                            'Commercial storage facility',
                            'Pawn shop',
                            'Police/sheriff',
                            'Lock box',
                            'Gun safe',
                            'Locking device',
                            'Disassemble',
                        ]}
                    />

                    <BubbbleQuestion
                        title="Medicine"
                        answerKey="strategiesMedicine"
                        editedAnswers={editedAnswers}
                        setEditedAnswers={setEditedAnswers}
                        options={['Disposal', 'Locked up at home', 'Stored with a trusted person']}
                    />

                    <BubbbleQuestion
                        title="Places"
                        answerKey="strategiesPlaces"
                        editedAnswers={editedAnswers}
                        setEditedAnswers={setEditedAnswers}
                        options={['Avoid location']}
                    />

                    <BubbbleQuestion
                        title="Other"
                        answerKey="strategiesOther"
                        editedAnswers={editedAnswers}
                        setEditedAnswers={setEditedAnswers}
                        options={[
                            'Limit access when and where it is possible',
                            'Have list of emergency response and lifelines available',
                        ]}
                    />

                    <BubbbleQuestion
                        title="Custom"
                        answerKey="strategiesCustom"
                        editedAnswers={editedAnswers}
                        setEditedAnswers={setEditedAnswers}
                        options={[]}
                        allowCustom
                    />
                </List>
            </KeyboardAvoidingView>
            <Menu selected="stability-playlist" />
        </Container>
    );
};

export default SaferHomeEdit;
