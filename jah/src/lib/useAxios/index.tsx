import { useContext, useEffect } from 'react';
import axios, { AxiosInstance, AxiosStatic } from 'axios';
import Sentry from 'lib/sentry';
import StoreContext from 'state/context/store';
import { displayError } from 'state/actions/error';
import config from 'config';
import { UserConstants } from 'state/constants';

type CustomAxiosInstance = AxiosInstance & Pick<AxiosStatic, 'isCancel' | 'CancelToken'>;

// @ts-ignore
const instance: CustomAxiosInstance = axios.create({
    baseURL: config.apiRoot,
});
instance.CancelToken = axios.CancelToken;
instance.isCancel = axios.isCancel;

const useAxios = () => {
    const [store, dispatch] = useContext(StoreContext);
    const { user } = store;
    const { authenticated, token, userType } = user;

    useEffect(() => {
        const onSuccess = (response: any) => response; // Do nothing
        const onFailure = (error: any) => {
            const status = error.status || error.response.status;

            if (status === 401) {
                return dispatch({ type: UserConstants.RESET_APP });
            } else if (status === 403) {
                if (userType === 'patient') {
                    return dispatch({ type: UserConstants.LOCK_SESSION });
                }
                return dispatch({ type: UserConstants.RESET_APP });
            } else if (status === 500) {
                Sentry.captureException(error);
                displayError(dispatch);
            }
        };

        if (token) {
            instance.defaults.headers.common['Authorization'] = `Token ${token}`;
        } else {
            delete instance.defaults.headers.common['Authorization'];
        }
        if (authenticated) {
            const reqInterceptor = instance.interceptors.request.use(onSuccess, onFailure);
            return () => instance.interceptors.request.eject(reqInterceptor);
        }
    }, [authenticated, dispatch, token, userType]);

    return instance;
};

export default useAxios;
