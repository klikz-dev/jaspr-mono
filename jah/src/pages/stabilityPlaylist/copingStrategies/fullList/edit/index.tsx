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
    const { copingBody, copingCourage, copingDistract, copingHelpOthers, copingSenses } =
        crisisStabilityPlan;

    const [editedAnswers, setEditedAnswers] = useState({
        copingBody: copingBody || [],
        copingCourage: copingCourage || [],
        copingDistract: copingDistract || [],
        copingHelpOthers: copingHelpOthers || [],
        copingSenses: copingSenses || [],
    });

    useEffect(() => {
        setEditedAnswers({
            copingBody: copingBody || [],
            copingCourage: copingCourage || [],
            copingDistract: copingDistract || [],
            copingHelpOthers: copingHelpOthers || [],
            copingSenses: copingSenses || [],
        });
    }, [copingBody, copingCourage, copingDistract, copingHelpOthers, copingSenses]);

    const save = () => {
        saveCrisisStabilityPlan(dispatch, editedAnswers);
        Segment.track('stability plan edited from JAH', { page: 'coping-strategies' });
        history.goBack();
    };

    return (
        <Container>
            <EditTitleMenu label="Edit Coping Strategies" save={save} />
            <KeyboardAvoidingView
                style={{ flex: 1 }}
                behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            >
                <List>
                    <BubbbleQuestion
                        title="Calm your body chemistry"
                        answerKey="copingBody"
                        editedAnswers={editedAnswers}
                        setEditedAnswers={setEditedAnswers}
                        options={[
                            'Cold shower',
                            'Hot bath',
                            'Hold ice',
                            'Intense exercise',
                            'Climb stairs',
                            'Squats',
                            'Paced breathing',
                        ]}
                        allowCustom
                    />

                    <BubbbleQuestion
                        title="Distract"
                        answerKey="copingDistract"
                        editedAnswers={editedAnswers}
                        setEditedAnswers={setEditedAnswers}
                        options={[
                            'Go for a walk',
                            'Meet a friend',
                            'Go to a place of worship',
                            'Clean my space',
                            'Go to gym',
                            'Go to a library',
                            'Video games',
                            'Call a friend',
                            'Watch an inspiring movie',
                            'Go to a cafe',
                        ]}
                        allowCustom
                    />

                    <BubbbleQuestion
                        title="Help someone"
                        answerKey="copingHelpOthers"
                        editedAnswers={editedAnswers}
                        setEditedAnswers={setEditedAnswers}
                        options={[
                            'Do something kind',
                            'Give a compliment',
                            'Offer encouragement',
                            'Volunteer',
                            'Clean a shared space',
                            'Help someone',
                            'Make a small gift',
                        ]}
                        allowCustom
                    />

                    <BubbbleQuestion
                        title="Courage"
                        answerKey="copingCourage"
                        editedAnswers={editedAnswers}
                        setEditedAnswers={setEditedAnswers}
                        options={[
                            'Pray',
                            'Call a supportive person',
                            'Encourage myself',
                            'Practice mindfulness',
                        ]}
                        allowCustom
                    />

                    <BubbbleQuestion
                        title="Comfort through 5 senses"
                        answerKey="copingSenses"
                        editedAnswers={editedAnswers}
                        setEditedAnswers={setEditedAnswers}
                        options={[
                            'Look at beautiful images',
                            'Be in nature',
                            'Enjoy a hot drink',
                            'Wear favorite clothing',
                            'Listen to soothing music',
                            'Eat a favorite food',
                            'Use scented soap or lotion',
                            'Light a candle',
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
