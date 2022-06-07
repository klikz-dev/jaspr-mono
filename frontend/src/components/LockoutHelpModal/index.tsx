import modalStyles from '../layouts/modals/index.module.scss';

interface Props {
    goBack: () => void;
}

const LockoutHelpModal = (props: Props) => {
    const { goBack } = props;

    return (
        <div className={modalStyles.modal}>
            <h2>Need help with secret image and security question?</h2>
            <p>You set up a secret image and security question when you started using Jaspr.</p>
            <p>
                If you can't remember one of them, or don't see your image or question listed, ask
                the person who gave you the Jaspr tablet to help reset your image and security
                question.
            </p>
            <div className={modalStyles.spacer} />
            <div className={modalStyles.buttonGroup}>
                <div className={modalStyles.filledButton} onClick={goBack}>
                    Back to login screen
                </div>
            </div>
        </div>
    );
};

export { LockoutHelpModal };
export default LockoutHelpModal;
