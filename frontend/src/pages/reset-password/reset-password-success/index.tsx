import { useHistory } from 'lib/router';
import logo from 'assets/logo.png';
import Button from 'components/Button';
import styles from './index.module.scss';

const ResetPasswordSuccess = () => {
    const history = useHistory();
    return (
        <div className={styles.container}>
            <header>
                <img src={logo} alt="Jaspr Health" /> Jaspr Health
            </header>
            <div className={styles.box}>
                <h1>Account Details</h1>
                <p>You have successfully reset the password for your Jaspr account.</p>
                <Button onClick={() => history.push('/')}>Done</Button>
            </div>
        </div>
    );
};

export default ResetPasswordSuccess;
