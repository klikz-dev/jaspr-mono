import { useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import styles from './index.module.scss';
import Logo from 'assets/logo-w-text.svg';
import { useQuery } from 'lib/useQuery';
import useAxios from 'lib/useAxios';
import { GetResponse } from 'state/types/api/technician/freshdesk';

const FreshdeskSSO = () => {
    const history = useHistory();
    const axios = useAxios();
    const query = useQuery();
    const nonce = query.get('nonce');
    const state = query.get('state');
    console.log(state, nonce);

    useEffect(() => {
        (async () => {
            try {
                const response = await axios.get<GetResponse>(
                    `technician/freshdesk?nonce=${nonce}&state=${state}`,
                );
                const { data } = response;
                window.location.replace(data.redirect_url);
            } catch (error) {
                // TODO New toaster if error
            }
        })();
    }, [axios, history, nonce, state]);

    return (
        <div className={styles.container}>
            <img className={styles.logo} src={Logo} alt="" />
            <div className={styles.loading}>
                <div className={styles.loadingIndicator} />
                <span>Signing you in to Freshdesk...</span>
            </div>
        </div>
    );
};

export default FreshdeskSSO;
