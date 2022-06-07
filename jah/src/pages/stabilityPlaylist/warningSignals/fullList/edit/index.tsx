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
    const { wsActions, wsFeelings, wsStressors, wsThoughts } = crisisStabilityPlan;

    const [editedAnswers, setEditedAnswers] = useState({
        wsActions: wsActions || [],
        wsFeelings: wsFeelings || [],
        wsStressors: wsStressors || [],
        wsThoughts: wsThoughts || [],
    });

    useEffect(() => {
        setEditedAnswers({
            wsActions: wsActions || [],
            wsFeelings: wsFeelings || [],
            wsStressors: wsStressors || [],
            wsThoughts: wsThoughts || [],
        });
    }, [wsActions, wsFeelings, wsStressors, wsThoughts]);

    const save = () => {
        saveCrisisStabilityPlan(dispatch, editedAnswers);
        Segment.track('stability plan edited from JAH', { page: 'warning-signals' });
        history.goBack();
    };

    return (
        <Container>
            <EditTitleMenu label="Edit Warning Signs" save={save} />
            <KeyboardAvoidingView
                style={{ flex: 1 }}
                behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            >
                <List>
                    <BubbbleQuestion
                        title="Stressors &amp; Situations"
                        answerKey="wsStressors"
                        editedAnswers={editedAnswers}
                        setEditedAnswers={setEditedAnswers}
                        options={['Conflict in relationship', 'Conflict with family or friend']}
                        allowCustom
                    />

                    <BubbbleQuestion
                        title="Internal Signals"
                        answerKey="wsThoughts"
                        editedAnswers={editedAnswers}
                        setEditedAnswers={setEditedAnswers}
                        options={['This will never end', "I can't take it anymore"]}
                        allowCustom
                    />

                    <BubbbleQuestion
                        title="Sensations or emotions"
                        answerKey="wsFeelings"
                        editedAnswers={editedAnswers}
                        setEditedAnswers={setEditedAnswers}
                        options={[
                            'Feeling on edge',
                            'Restless',
                            'Shaking/trembling',
                            'Nausea',
                            'Panicky',
                            'Physical pain',
                            'Guilt',
                            'Anger',
                            'Worry',
                            'Shame',
                            'Sadness',
                        ]}
                        allowCustom
                    />

                    <BubbbleQuestion
                        title="Actions"
                        answerKey="wsActions"
                        editedAnswers={editedAnswers}
                        setEditedAnswers={setEditedAnswers}
                        options={[
                            'Problems sleeping',
                            'Avoiding people',
                            'Pacing',
                            'Harming myself',
                            'Practicing/rehearsing suicide attempt',
                            'Crying',
                            'Yelling/screaming',
                            'Getting ready for suicide attempt',
                        ]}
                        allowCustom
                    />
                </List>
            </KeyboardAvoidingView>
            <Menu selected="stability-playlist" />
        </Container>
    );
};

export default SaferHomeEdit;
