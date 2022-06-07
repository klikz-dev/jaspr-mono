import logo from 'assets/logo.svg';
import styles from './index.module.scss';

const EhrTimeout = () => {
    return (
        <div className={styles.container}>
            <img className={styles.logo} src={logo} alt="" />
            <p>
                Your Jaspr Health session has expired. Please navigate away from the Jaspr Health
                app within your EHR and then back. This will re-authenticate you as a user.
            </p>
        </div>
    );
};

export default EhrTimeout;
