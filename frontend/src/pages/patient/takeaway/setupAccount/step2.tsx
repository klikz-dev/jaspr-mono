import { useContext } from 'react';
import { setupToolsToGo } from 'state/actions/user';
import Button from 'components/Button';
import StoreContext from 'state/context/store';
import styles from './index.module.scss';

interface Step2Props {
    close: () => void;
    mobilePhone: string;
    email: string;
    prevAccountSetupStep: () => void;
    nextAccountSetupStep: () => void;
    setError: (error: string) => void;
}

const Step2 = ({
    email,
    mobilePhone,
    prevAccountSetupStep,
    nextAccountSetupStep,
    setError,
}: Step2Props) => {
    const [, dispatch] = useContext(StoreContext);

    const submit = async () => {
        const response = await setupToolsToGo(dispatch, email, mobilePhone);
        if (response.status === 400) {
            let error = '';
            if (response?.data?.email) {
                error = response.data.email[0];
            } else if (response?.data?.mobilePhone) {
                error = response.data.mobilePhone[0];
            } else if (response?.data?.nonFieldErrors) {
                error = response.data.nonFieldErrors[0];
            } else {
                error = 'There was an unknown error.  Please try again';
            }
            setError(error);
            prevAccountSetupStep();
        } else {
            setError('');
            nextAccountSetupStep();
        }
    };

    return (
        <div className={styles.box}>
            <header>Confirm Your Information</header>

            <form onSubmit={submit}>
                <label>
                    Phone Number
                    <input
                        value={mobilePhone}
                        disabled
                        required
                        type="tel"
                        autoComplete="off"
                        autoCapitalize="off"
                        autoFocus
                    />
                </label>

                <label>
                    Email Address
                    <input
                        disabled
                        required
                        type="email"
                        autoComplete="off"
                        autoCapitalize="off"
                        value={email}
                    />
                </label>
                <div className={styles.buttons} style={{ justifyContent: 'center' }}>
                    <Button variant="tertiary" onClick={prevAccountSetupStep}>
                        Back
                    </Button>
                    <Button onClick={submit}>Submit</Button>
                </div>
            </form>
        </div>
    );
};

export default Step2;
