import React, { useContext } from 'react';
import { useHistory } from 'lib/router';
import { completeTour } from 'state/actions/user';
import { actionNames, addAction } from 'state/actions/analytics';
import StoreContext from 'state/context/store';
import Styled from 'styled-components/native';
import styles from './index.module.scss';
import { QuestionProps } from '../../question';

interface Button {
    label: string;
    selected?: boolean;
    analyticsAction?: keyof typeof actionNames;
    action?: string;
    params?: string;
    path?: string;
    goto?: string;
}

const Container = Styled.View`${styles.container}
    width: 100%;
    margin-left: 0;
    margin-right: 0;
    padding-top: 34px;
    margin-top: auto;
    align-items: center;
    justify-content: center;
`;
const ButtonsContainer = Styled.View``;
const Button = Styled.TouchableOpacity<{ answered?: boolean }>`
    height: 53px;
    border-radius: 5px;
    background-color: ${({ answered }) => (answered ? 'rgba(88, 92, 114, 0.8)' : '#68BBD0')};
    align-items: center;
    justify-content: center;
    padding: ${({ answered }) => (answered ? '13px 27px' : '14px')}
    margin-left: ${({ answered }) => (answered ? 'auto' : '0')}
    min-width: 89px;
`;
const ButtonText = Styled.Text`font-size: 20px;`;

export type ButtonProps = Pick<
    QuestionProps,
    'answered' | 'setAnswered' | 'next' | 'isValid' | 'validate' | 'setShowValidation' | 'answerKey'
> & {
    orientation?: 'vertical' | 'horizontal';
    submissionInProgress: boolean;
    setSubmissionInProgress: (submissionInProgress: boolean) => void;
    buttons: Button[];
    validation?: boolean;
};

const Buttons = (props: ButtonProps) => {
    const history = useHistory();
    const {
        answered,
        buttons,
        setAnswered,
        next,
        isValid,
        validation,
        validate,
        setShowValidation,
        submissionInProgress,
        setSubmissionInProgress,
    } = props;
    const [, dispatch] = useContext(StoreContext);

    const onClick = (button: Button) => {
        const handleValidation = () => {
            setAnswered(Boolean(button.label));

            if (button.analyticsAction) {
                addAction(actionNames[button.analyticsAction]);
            }

            if (button.action === 'navigate') {
                if (button.params === '?completeTour=true') {
                    // This is a hack.  It doesn't really belong in this component
                    completeTour(dispatch);
                }
                history.push({ pathname: button.path, search: button.params || '' });
            } else {
                next(button.goto);
            }
        };
        setShowValidation(false);
        if (validate?.current) {
            setSubmissionInProgress(true);
            validate
                .current()
                .then(handleValidation)
                .catch((err) => {})
                .finally(() => setSubmissionInProgress(false));
        } else {
            if (!validation || isValid) {
                handleValidation();
            } else {
                setShowValidation(true);
            }
        }
    };

    return (
        <Container>
            <ButtonsContainer>
                {buttons.map((button) => (
                    <Button
                        answered={answered}
                        disabled={Boolean(answered) || submissionInProgress}
                        key={button.label}
                        onPress={() => onClick(button)}
                    >
                        <ButtonText numberOfLines={1}>{button.label}</ButtonText>
                    </Button>
                ))}
            </ButtonsContainer>
        </Container>
    );
};

export default Buttons;
