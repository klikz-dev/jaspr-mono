import { useEffect, useState } from 'react';
import styles from './index.module.scss';
import closeSrc from 'assets/close.svg';
import axios from 'axios';

const MaintenanceNotice = () => {
    const [show, setShow] = useState(false);
    const [notice, setNotice] = useState({ title: '', description: '' });

    const dismiss = () => {
        setShow(false);
    };

    useEffect(() => {
        axios.get('/maintenance.json').then((response) => {
            const { data } = response;
            const { noticeStart, end } = data;
            if (new Date(noticeStart) < new Date() && new Date(end) > new Date()) {
                setNotice(data);
                setShow(true);
            }
        });
    }, []);

    return (
        <>
            {show && (
                <div className={styles.container}>
                    <img
                        onClick={dismiss}
                        className={styles.dismiss}
                        style={{ cursor: 'pointer' }}
                        src={closeSrc}
                        alt="Dismiss notice"
                    />
                    <div className={styles.title}>{notice.title}</div>
                    <div className={styles.description}>{notice.description}</div>
                </div>
            )}
        </>
    );
};

export { MaintenanceNotice };
export default MaintenanceNotice;
