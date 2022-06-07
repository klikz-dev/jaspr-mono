import Sentry from './sentry';
import { AxiosResponse, AxiosError } from 'axios';
import { Dispatch } from 'state/types';
import { UserConstants } from 'state/constants';

type ErrorInterceptor = [
    (value: AxiosResponse<any>) => AxiosResponse<any> | Promise<AxiosResponse<any>>,
    (value: AxiosError<any>) => AxiosError<any> | Promise<AxiosError<any>>,
];

const errorInterceptor = (dispatch: Dispatch): ErrorInterceptor => [
    (response: AxiosResponse): AxiosResponse<any> => response,
    (error: AxiosError): AxiosError<any> => {
        if (error.response) {
            const { status } = error.response;
            if (status === 401) {
                dispatch({ type: 'RESET_APP' });
            } else if (status === 403) {
                dispatch({ type: UserConstants.LOCK_SESSION });
            } else if (status === 500) {
                Sentry.captureException(error);
            }
        }
        throw error;
    },
];

export { errorInterceptor };
