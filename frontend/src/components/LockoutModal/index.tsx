import React, { useEffect, useState, useContext, useCallback } from 'react';
import Modal, { Styles } from 'react-modal';
import { getPrivacyImages, getSecurityQuestion, validateSession, getMe } from 'state/actions/user';
import StoreContext from 'state/context/store';
import LockoutHelpModal from '../LockoutHelpModal';
import styles from './index.module.scss';
import Hamburger from 'components/Hamburger';
import zIndexHelper from 'lib/zIndexHelper';
import logo from 'assets/logo.png';
import { Patient } from 'state/types';

const modalHelpStyle: Styles = {
    overlay: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'rgba(45, 44, 63, 0.85)',
        zIndex: zIndexHelper('patient.lockout-help'),
    },
    content: {
        position: 'static',
        display: 'flex',
        width: '50vw',
        minHeight: '50vh',
        alignSelf: 'center',
        borderRadius: 0,
    },
};

const LockoutModal = () => {
    const [store, dispatch] = useContext(StoreContext);
    const { privacyImages = [], securityQuestion } = store.user as Patient;
    const [selectedImage, setSelectedImage] = useState<number>(null);
    const [securityAnswer, setSecurityAnswer] = useState('');
    const [showHelpModal, setShowHelpModal] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {
        getPrivacyImages(dispatch);
        getSecurityQuestion(dispatch);
    }, [dispatch]);

    const validate = async () => {
        const response = await validateSession(dispatch, selectedImage, securityAnswer);
        if (response?.status === 200) {
            getMe(dispatch);
        } else {
            const { data = {} } = response || {};
            if (data.nonFieldErrors?.length) {
                setErrorMessage(data.nonFieldErrors[0]);
            } else if (data.image?.length) {
                setErrorMessage(data.image[0]);
            } else if (data.securityQuestionAnswer?.length) {
                setErrorMessage(data.securityQuestionAnswer[0]);
            } else {
                setErrorMessage('An unknown error occurred');
            }
        }
    };

    const toggleHelpModal = useCallback(() => {
        setShowHelpModal(!showHelpModal);
    }, [showHelpModal]);

    const keyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
        // TODO Update deprecated keyCode
        if (e.keyCode === 13) {
            validate();
        }
    };

    return (
        <>
            <div className={styles.lockout}>
                <Hamburger dark />
                <div className={styles.container}>
                    <img
                        alt="JASPR Logo"
                        aria-label="Jasper Logo"
                        src={logo}
                        className={styles.logo}
                    />
                    <span className={styles.selectSecret}>Select your secret image</span>
                    <div className={styles.imageSelect}>
                        {privacyImages.map((image) => (
                            <img
                                key={image.id}
                                alt="security secret"
                                src={image.url}
                                onClick={() => setSelectedImage(image.id)}
                                className={`${image.id === selectedImage ? styles.selected : ''} ${
                                    selectedImage === null ? styles.allUnselected : ''
                                }`}
                            />
                        ))}
                    </div>
                    <div className={styles.securityQuestion}>
                        {securityQuestion ? securityQuestion.question : ''}
                    </div>
                    <div className={styles.securityAnswer}>
                        <input
                            type="text"
                            placeholder="Enter answer"
                            value={securityAnswer}
                            onChange={(e) => setSecurityAnswer(e.target.value)}
                            onKeyDown={keyPress}
                        />
                    </div>
                    <div className={styles.button} onClick={validate}>
                        Next
                    </div>
                    <div className={styles.error}>{errorMessage}</div>
                    <div className={styles.help} onClick={toggleHelpModal}>
                        Need help?
                    </div>
                </div>
            </div>
            <Modal isOpen={showHelpModal} style={modalHelpStyle} onRequestClose={toggleHelpModal}>
                <LockoutHelpModal goBack={toggleHelpModal} />
            </Modal>
        </>
    );
};

export { LockoutModal };
export default LockoutModal;
