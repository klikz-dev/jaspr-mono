import Button from 'components/Button';
import check from 'assets/check.svg';
import styles from './index.module.scss';

interface Step2Props {
    close: () => void;
}

const Step2 = ({ close }: Step2Props) => {
    const submit = () => {
        close();
    };

    return (
        <div className={styles.box}>
            <header>You're all set!</header>
            <div className={styles.step}>
                You'll find next steps for accessing Jaspr at Home in your email inbox.
            </div>
            <img src={check} alt="You're all set" style={{ height: '110px', width: '110px' }} />
            <div className={styles.buttons} style={{ justifyContent: 'center' }}>
                <Button onClick={submit}>Done</Button>
            </div>
        </div>
    );
};

export default Step2;
