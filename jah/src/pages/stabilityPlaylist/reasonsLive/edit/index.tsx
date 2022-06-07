import React, { useCallback, useContext, useEffect, useState } from 'react';
import { KeyboardAvoidingView, Platform } from 'react-native';
import DraggableFlatList, { RenderItemParams } from 'react-native-draggable-flatlist';
import Styled from 'styled-components/native';
import { useHistory } from 'lib/router';
import EditTitleMenu from 'components/EditTitleMenu';
import Menu from 'components/Menu/index';
import StoreContext from 'state/context/store';
import { saveCrisisStabilityPlan } from 'state/actions/crisisStabilityPlan';
import Segment from 'lib/segment';

const Container = Styled.View`
    flex: 1;
    background-color: #41476A;
`;
const Row = Styled.View`
    flex-direction: row;
    padding-horizontal: 38px;
    align-items: center;
`;
const Input = Styled.TextInput`
    flex: 1;
    margin-top: 19px;
    padding-horizontal: 5px;
    padding-bottom: 3px;
    border-bottom-width: 1.5px;
    border-bottom-color: #F8F8F8;
    font-size: 18px;
    color: rgba(255, 255, 255, 1);
`;
const Handle = Styled.TouchableOpacity`
    justify-content: space-between;
    width: 12px;
    height: 10px;
    margin-left: 13px;
`;
const HandleLine = Styled.View`
    border-bottom-width: 1px;
    border-bottom-color: #d8d8d8;
`;

const ReasonsLiveEdit = () => {
    const history = useHistory();
    const [store, dispatch] = useContext(StoreContext);
    const { crisisStabilityPlan } = store;
    const { reasonsLive } = crisisStabilityPlan;

    const [editedAnswers, setEditedAnswers] = useState({
        reasonsLive: reasonsLive || [],
    });

    useEffect(() => {
        setEditedAnswers({
            reasonsLive: reasonsLive || [],
        });
    }, [reasonsLive]);

    const save = () => {
        saveCrisisStabilityPlan(dispatch, {
            ...editedAnswers,
            reasonsLive: editedAnswers.reasonsLive.filter((reason) => reason),
        });
        Segment.track('stability plan edited from JAH', { page: 'reasons-live' });
        history.goBack();
    };

    const renderItem = useCallback(({ item, index, drag, isActive }: RenderItemParams<string>) => {
        return (
            <Row>
                <Input
                    value={item}
                    maxLength={10000}
                    placeholder="Tap to start typing"
                    placeholderTextColor="rgba(255, 255, 255, 0.27)"
                    onChangeText={(value) =>
                        setEditedAnswers((answers) => {
                            if (index !== undefined) {
                                const data = [...Array(5)].map(
                                    (_, idx) => answers['reasonsLive']?.[idx] || '',
                                );
                                data[index] = value;
                                return { ...answers, reasonsLive: data };
                            }
                            return answers;
                        })
                    }
                />
                <Handle onPressIn={drag}>
                    <HandleLine />
                    <HandleLine />
                    <HandleLine />
                </Handle>
            </Row>
        );
    }, []);

    const sortData = [...Array(5)].map((_, idx) => editedAnswers['reasonsLive']?.[idx] || '');

    return (
        <Container>
            <EditTitleMenu label="Edit Reasons for Living" save={save} />
            <KeyboardAvoidingView
                style={{ flex: 1 }}
                behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            >
                <DraggableFlatList
                    scrollEnabled={false}
                    data={sortData}
                    renderItem={renderItem}
                    keyExtractor={(_, index) => `draggable-item-${index}`}
                    onDragEnd={({ data }) => {
                        setEditedAnswers((answers) => ({ ...answers, reasonsLive: data }));
                    }}
                />
            </KeyboardAvoidingView>
            <Menu selected="stability-playlist" />
        </Container>
    );
};

export default ReasonsLiveEdit;
