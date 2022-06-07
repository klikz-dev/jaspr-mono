import { useContext, useEffect, useState } from 'react';
import axios from 'axios';
import { useQuery } from 'lib/useQuery';
import { useHistory } from 'lib/router';
import StoreContext from 'state/context/store';
import { getMe } from 'state/actions/user';
import { setDevice } from 'state/actions/device';
import config from '../../../../config';
import Logo from 'assets/logo-w-text.svg';

import styles from './index.module.scss';
import { UserConstants } from 'state/constants';
import { Device } from 'state/types';
import { PostResponse } from 'state/types/api/technician/epic-oauth-login';
import Segment, { AnalyticNames } from 'lib/segment';

const EpicRedirect = () => {
    const history = useHistory();
    const [, dispatch] = useContext(StoreContext);
    const [token, setToken] = useState<string>();
    const [patient, setPatient] = useState<PostResponse['patient']>();
    const [error, setError] = useState('');
    const query = useQuery();
    const code = query.get('code');
    const state = query.get('state');

    useEffect(() => {
        (async () => {
            if (code) {
                const port = window.location.port;
                try {
                    const response = await axios.post<PostResponse>(
                        `${config.apiRoot}/technician/epic-oauth-login`,
                        {
                            code,
                            state,
                            redirect_uri: `${window.location.protocol}//${
                                window.location.hostname
                            }${port ? `:${port}` : ''}/epic/redirect`,
                        },
                    );
                    setToken(response.data?.token);
                    setPatient(response.data?.patient);
                    Segment.track(AnalyticNames.TECHNICIAN_AUTHENTICATED_WITH_EPIC);

                    if (response.data.patient?.id) {
                        history.push(`/technician/patients/${response.data.patient.id}`);
                    } else {
                        history.push('/technician/patients');
                    }
                } catch (err) {
                    const response = err?.response;
                    if (response?.data?.nonFieldErrors) {
                        setError(response.data.nonFieldErrors);
                    } else {
                        setError('There was an error authenticating.');
                    }
                }
            }
        })();
    }, [history, code, state]);

    useEffect(() => {
        (async () => {
            if (token) {
                axios.defaults.headers.common['Authorization'] = `Token ${token}`;
                dispatch({
                    type: UserConstants.SET_TOKEN,
                    token: token,
                });
                await getMe(dispatch);
                const device: Device = {
                    isEhrEmbedded: true,
                    inPatientContext: true,
                    isTablet: false,
                    code: null, // We could populate this from the oauth login record, but currently don't need this value for EHR sessions
                    codeType: null,
                    patientContextId: patient?.id || null,
                };
                setDevice(dispatch, device);
                Segment.track(AnalyticNames.SET_DEVICE, device);
            }
        })();
    }, [token, dispatch, patient]);

    return (
        <div className={styles.container}>
            <img className={styles.logo} src={Logo} alt="Signing into Jaspr" />

            {Boolean(error) && <div className={styles.error}>{error}</div>}
            {!Boolean(error) && (
                <>
                    <div className={styles.loading}>
                        <div className={styles.loadingIndicator} />
                        <span>Signing you in to Jaspr Health...</span>
                    </div>
                </>
            )}
        </div>
    );
};

export default EpicRedirect;
