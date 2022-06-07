import { useHistory } from 'lib/router';
import Hamburger from 'components/Hamburger';
import logo from 'assets/logo.png';
import styles from './welcome.module.scss';

const Welcome = () => {
    const history = useHistory();

    return (
        <div
            className={styles.welcome}
            style={{ background: 'linear-gradient(270deg, #3b4a67 0%, #4c526b 100%)' }}
        >
            <Hamburger dark={true} />
            <div className={styles.container}>
                <img alt="JASPR Logo" aria-label="Jasper Logo" src={logo} className={styles.logo} />
                <div className={styles.hello}>Hello.</div>
                <div className={styles.message}>
                    <span aria-label="We're Jasper">We're Jaspr.</span>
                    <br />
                    We'd like to help you get
                    <br />
                    through this.
                </div>
                <div
                    className={styles.button}
                    onClick={() => {
                        history.push('/consent');
                    }}
                >
                    Give it a try
                </div>
            </div>
        </div>
    );
};

export default Welcome;
