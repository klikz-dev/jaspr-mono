import { useContext, useEffect, useState } from 'react';
import StoreContext from 'state/context/store';
import { getPrivacyImages, setSecurityImage } from 'state/actions/user';
import styles from './index.module.scss';
import { QuestionProps } from '../../question';
import { Patient } from 'state/types';

type SetSecurityQuestionProps = Pick<
    QuestionProps,
    | 'currentQuestion'
    | 'validate'
    | 'isValid'
    | 'setIsValid'
    | 'showValidation'
    | 'setShowValidation'
>;

const SetSecurityQuestion = (props: SetSecurityQuestionProps) => {
    const {
        currentQuestion,
        validate,
        isValid,
        setIsValid,
        showValidation,
        setShowValidation,
    } = props;
    const [store, dispatch] = useContext(StoreContext);
    const { user } = store;
    const { privacyImages = [] } = user as Patient;
    const [selectedImage, setSelectedImage] = useState<number | null>(null);

    useEffect(() => {
        getPrivacyImages(dispatch);
    }, [dispatch]);

    useEffect(() => {
        validate.current = () =>
            new Promise((resolve, reject) => {
                const valid = selectedImage !== undefined && selectedImage !== null;
                setIsValid(valid);
                setShowValidation(!valid);
                if (valid && selectedImage !== null) {
                    setSecurityImage(dispatch, selectedImage);
                    resolve(valid);
                } else {
                    reject();
                }
            });
    }, [dispatch, setIsValid, setShowValidation, validate, selectedImage]);

    return (
        <>
            {!currentQuestion && (
                <div className={styles.completeMessage}>Security image complete</div>
            )}
            {currentQuestion && (
                <div className={styles.container}>
                    <div className={styles.imageSelect}>
                        {privacyImages.map((image) => (
                            <img
                                key={image.id}
                                alt="security secret"
                                src={image.url}
                                onClick={() => {
                                    setSelectedImage(image.id);
                                    setIsValid(true);
                                }}
                                className={`${image.id === selectedImage ? styles.selected : ''} ${
                                    selectedImage === null ? styles.allUnselected : ''
                                }`}
                            />
                        ))}
                    </div>
                    {!isValid && showValidation && (
                        <div className={styles.instruction}>Please select a security image</div>
                    )}
                </div>
            )}
        </>
    );
};

export { SetSecurityQuestion };
export default SetSecurityQuestion;
