import React from 'react';
import Modal, { Styles } from 'react-modal';

const modalStyle: Styles = {
    overlay: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'rgba(0,0,0,0.4)',
    },
    content: {
        position: 'relative',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-around',
        flexDirection: 'column',
        border: 'none',
        backgroundColor: '#ffffff',
        padding: 60,
        maxWidth: '688px',
        maxHeight: '456px',
        width: '95%',
        height: '95%',
        overflow: 'hidden',
        borderRadius: '6px',
    },
};

type JasprModalProps = {
    zIndex?: number;
    children: React.ReactNode;
} & Modal.Props;

const JasprModal = ({
    isOpen,
    style = { overlay: {}, content: {} },
    children,
    zIndex = 20,
    ...rest
}: JasprModalProps) => (
    <Modal
        isOpen={isOpen}
        style={{
            overlay: { zIndex, ...modalStyle.overlay, ...style.overlay },
            content: { ...modalStyle.content, ...style.content },
        }}
        {...rest}
    >
        {children}
    </Modal>
);

export default JasprModal;
