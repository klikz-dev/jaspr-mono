import Button from 'components/Button';
import styles from './index.module.scss';

interface Step0Props {
    close: () => void;
    nextAccountSetupStep: () => void;
}

const Step0 = ({ close, nextAccountSetupStep }: Step0Props) => {
    return (
        <div className={styles.box}>
            <header>Jaspr At Home Account Setup</header>
            <p>
                Would you like your own access to your crisis plan and notes from today, by creating
                a Jaspr Health account?
            </p>
            <p>
                By selecting yes, Jaspr Health will keep a secure copy of your information, that you
                can access from your mobile phone. In future visits, you can also choose to share
                this information with your doctor or other healthcare providers.{' '}
                <strong>Your data is always in your control.</strong>
            </p>
            <p>
                By selecting no, you will not be able to access your information in the future on
                your mobile device or at other healthcare providers.
            </p>

            <div className={styles.buttons}>
                <Button variant="tertiary" onClick={close}>
                    No, don't save my information
                </Button>
                <Button onClick={nextAccountSetupStep}>Yes</Button>
            </div>
        </div>
    );
};

export default Step0;
