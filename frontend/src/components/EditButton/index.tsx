import React from 'react';
import styles from './index.module.scss';
import Pencil from 'assets/icons/Pencil';

type Props = {
    containerStyle?: React.CSSProperties;
    style?: React.CSSProperties;
    onClick: (event: React.SyntheticEvent<HTMLDivElement, MouseEvent | TouchEvent>) => void;
};

const EditButton = (props: Props) => {
    const { containerStyle, onClick, style } = props;
    return (
        <div className={styles.editIconWrapper} style={containerStyle || {}}>
            <div className={styles.editIconContainer} style={style || {}} onClick={onClick}>
                <Pencil color="#000000" height={13} />
            </div>
        </div>
    );
};

export { EditButton };
export default EditButton;
