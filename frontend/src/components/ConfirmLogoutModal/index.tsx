import Modal, { Styles as ModalStyles } from 'react-modal';
import zIndexHelper from 'lib/zIndexHelper';
import modalStyles from '../layouts/modals/index.module.scss';
import styles from './index.module.scss';

const modalConfirmLogoutStyle: ModalStyles = {
    overlay: {
        display: 'flex',
        justifyContent: 'space-evenly',
        backgroundColor: 'rgba(45, 44, 63, 0.85)',
        zIndex: zIndexHelper('patient.confirm-logout'),
    },
    content: {
        position: 'static',
        display: 'flex',
        width: '523px',
        height: '286px',
        alignSelf: 'center',
    },
};

type Props = {
    goBack: () => void;
    logout: () => void;
    confirmLogoutOpen: boolean;
};

const ConfirmLogoutModal = (props: Props) => {
    const { goBack, logout, confirmLogoutOpen } = props;

    return (
        <Modal isOpen={confirmLogoutOpen} style={modalConfirmLogoutStyle}>
            <div className={modalStyles.modal}>
                <div className={modalStyles.crossedPlus} onClick={goBack} />
                <h2>Are you sure you want to log out?</h2>
                <p>You will need a staff member to log you back in.</p>
                <div className={styles.buttonGroup}>
                    <div className={styles.outlinedButton} onClick={goBack}>
                        No, go back to Jaspr
                    </div>
                    <div className={styles.filledButton} onClick={logout}>
                        Yes, log out of Jaspr
                    </div>
                </div>
            </div>
        </Modal>
    );
};

export { ConfirmLogoutModal };
export default ConfirmLogoutModal;
