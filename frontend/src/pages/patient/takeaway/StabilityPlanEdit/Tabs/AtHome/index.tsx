import { useContext, useEffect, useState } from 'react';
import Section from '../../Components/Section';
import StoreContext from 'state/context/store';
import styles from './index.module.scss';
import { Patient } from 'state/types';
import Button from 'components/Button';
import { setupToolsToGo } from 'state/actions/user';

const AtHomeTab = () => {
    const [store, dispatch] = useContext(StoreContext);
    const { user } = store;
    const {
        toolsToGoStatus,
        email: patientEmail,
        mobilePhone: patientMobilePhone,
    } = user as Patient;
    const [mobilePhone, setMobilePhone] = useState(patientMobilePhone);
    const [email, setEmail] = useState(patientEmail);
    const [saving, setSaving] = useState(false);
    const [editing, setEditing] = useState(false);

    const submit = async (e: React.FormEvent<HTMLFormElement>) => {
        e?.preventDefault();
        setSaving(true);
        await setupToolsToGo(dispatch, email, mobilePhone);
        setSaving(false);
        setEditing(false);
    };

    useEffect(() => {
        setMobilePhone(patientMobilePhone);
        setEmail(patientEmail);
    }, [patientEmail, patientMobilePhone]);

    return (
        <Section
            number="6"
            title="Jaspr at Home Signup"
            tooltip="Signup for your Jaspr at Home account"
        >
            <div
                className={`${styles.container} ${
                    editing || toolsToGoStatus === 'Not Started' ? '' : styles.validate
                }`}
            >
                <h4>Please ask your patient:</h4>
                <p>
                    Would you like your own access to your crisis plan and notes from today, by
                    creating a Jaspr Health account?
                </p>
                <p>
                    Jaspr Health will keep a secure copy of your information, that you can access
                    from your mobile phone. In future visits, you can also choose to share this
                    information with your doctor or other healthcare providers.{' '}
                    <strong>Your data is always in your control</strong>.
                </p>
                <p>
                    <em>If they say yes, please enter their information below.</em>
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
                            readOnly={!(editing || toolsToGoStatus === 'Not Started')}
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
                            readOnly={!(editing || toolsToGoStatus === 'Not Started')}
                            value={email}
                            onChange={({ target }) => setEmail(target.value)}
                        />
                    </label>
                    <div className={styles.buttons}>
                        <Button type="submit" dark disabled={saving}>
                            Submit
                        </Button>
                    </div>
                </form>
                {toolsToGoStatus !== 'Not Started' && (
                    <div className={styles.alreadySetup}>
                        Jaspr at Home set up complete.{' '}
                        {toolsToGoStatus === 'Email Sent' && !editing && (
                            <button onClick={() => setEditing(true)}>Edit</button>
                        )}
                    </div>
                )}
            </div>
        </Section>
    );
};

export default AtHomeTab;
