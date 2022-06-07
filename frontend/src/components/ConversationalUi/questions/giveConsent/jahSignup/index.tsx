import React, { useContext, useState } from 'react';
import Button from 'components/Button';
import StoreContext from 'state/context/store';
import { setupToolsToGo } from 'state/actions/user';
import styles from './index.module.scss';

interface JahSignupProps {
    close: () => void;
}

const JahSignup = ({ close }: JahSignupProps) => {
    const [, dispatch] = useContext(StoreContext);
    const [mobilePhone, setMobilePhone] = useState('');
    const [email, setEmail] = useState('');
    const [showValidation, setShowValidation] = useState(false);

    const submit = (e: React.FormEvent<HTMLFormElement>) => {
        e?.preventDefault();
        if (!showValidation) {
            setShowValidation(true);
        } else {
            setupToolsToGo(dispatch, email, mobilePhone);
            close();
        }
    };

    const back = () => {
        if (showValidation) {
            setShowValidation(false);
        } else {
            close();
        }
    };

    return (
        <div className={`${styles.container} ${showValidation ? styles.validate : ''}`}>
            <h3>Confirm Your Information</h3>
            <p>
                Enter your email address and phone number to set up your account. We will send you
                an email and text message to finish your account set up.
            </p>
            <form onSubmit={submit}>
                <label>
                    Phone Number
                    <input
                        required
                        type="tel"
                        autoComplete="off"
                        autoCapitalize="off"
                        autoFocus
                        readOnly={showValidation}
                        value={mobilePhone}
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
                        readOnly={showValidation}
                        value={email}
                        onChange={({ target }) => setEmail(target.value)}
                    />
                </label>
                <div className={styles.buttons}>
                    <Button variant="secondary" onClick={back}>
                        {showValidation ? 'Go back and update' : 'Back'}
                    </Button>
                    <Button type="submit">{showValidation ? 'This is Correct' : 'Next'}</Button>
                </div>
            </form>
        </div>
    );
};

export { JahSignup };
export default JahSignup;
