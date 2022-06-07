import Button from 'components/Button';
import styles from './index.module.scss';

interface Step1Props {
    email: string;
    setEmail: (email: string) => void;
    mobilePhone: string;
    setMobilePhone: (mobilePhone: string) => void;
    nextAccountSetupStep: () => void;
    prevAccountSetupStep: () => void;
    error: string;
}

const Step1 = ({
    prevAccountSetupStep,
    email,
    setEmail,
    mobilePhone,
    setMobilePhone,
    nextAccountSetupStep,
    error,
}: Step1Props) => {
    const submit = async () => {
        nextAccountSetupStep();
    };

    return (
        <div className={styles.box}>
            <header>Jaspr at Home Account Setup</header>
            <p>
                Enter your email address and phone number to set up your account. We will send you
                an email and text message to finish your account set up.
            </p>
            <form onSubmit={submit}>
                <label>
                    Phone Number
                    <input
                        value={mobilePhone}
                        required
                        type="tel"
                        autoComplete="off"
                        autoCapitalize="off"
                        autoFocus
                        onChange={({ target }) => setMobilePhone(target.value)}
                    />
                </label>

                <label>
                    Email Address
                    <input
                        required
                        type="email"
                        autoComplete="off"
                        autoCapitalize="off"
                        value={email}
                        onChange={({ target }) => setEmail(target.value)}
                    />
                </label>
                <div className={styles.error}>{error}</div>
                <div className={styles.buttons}>
                    <Button variant="tertiary" onClick={prevAccountSetupStep}>
                        Back
                    </Button>
                    <Button type="submit">Next</Button>
                </div>
            </form>
        </div>
    );
};

export default Step1;
