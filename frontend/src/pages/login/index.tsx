import React, { FormEvent, useState, useEffect, useContext } from 'react';
import { Link, useHistory, useLocation } from 'lib/router';
import StoreContext from 'state/context/store';
import { loginAction } from 'state/actions/user';
import supportedBrowsers from '../../supportedBrowsers';
import logo from 'assets/logo.svg';
import styles from './login.module.scss';
import Button from 'components/Button';

const Login = () => {
    const history = useHistory();
    const location = useLocation<{ from?: { pathname: string } }>();
    const [store, dispatch] = useContext(StoreContext);
    const { device, user } = store;
    const { authenticated, userType } = user;
    const { isTablet, code, codeType } = device;
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [loggingIn, setLoggingIn] = useState<boolean>(false);
    const [loginError, setLoginError] = useState<string>('');
    const [secretDebugCount, setSecretDebugCount] = useState(0);

    /** If there is an application update and the user has not begun to interact with the app
     * then automatically update to the latest version
     */
    useEffect(() => {
        if (device.updateAvailable && !username && !password && !loginError) {
            window.location.reload();
        }
    }, [device.updateAvailable, loginError, password, username]);

    const handleLogin = async (e: FormEvent<HTMLFormElement>) => {
        if (e) {
            e.preventDefault();
        }

        setLoggingIn(true);
        let response;

        const domain = window.location.hostname;
        let slug;
        // On the dev server, we separate clinic slugs from feature
        // branches with a '--', otherwise, the first subdomain is the clinic slug
        if (domain.split('--').length > 1) {
            [slug] = domain.split('--');
        } else {
            [slug] = domain.split('.');
        }
        response = await loginAction(dispatch, username, password, slug);

        if (response?.status === 400 || response?.status === 403) {
            // @ts-ignore We know this is always the ErrorResponse.  How to assert?
            const json: {
                nonFieldErrors?: string[];
                email?: string[];
                password?: string[];
                detail?: string;
            } = response?.data;

            if (json?.email?.length) {
                setLoginError(json.email[0]);
            } else if (json?.password?.length) {
                setLoginError(json.password[0]);
            } else if (json.nonFieldErrors && json.nonFieldErrors.length > 0) {
                setLoginError(json.nonFieldErrors[0]);
            } else if (json.detail) {
                setLoginError(json.detail);
            } else {
                setLoginError('There was an unknown error');
            }
        }
    };

    useEffect(() => {
        if (authenticated) {
            let from = { pathname: '/' };
            if (location.state?.from && location.state.from.pathname !== location.pathname) {
                from = location.state.from;
            }
            history.push(from);
        }
    }, [authenticated, history, location.pathname, location.state, userType]);

    useEffect(() => {
        setUsername('');
        setPassword('');
    }, []);

    const handleLogout = (e?: React.MouseEvent<HTMLButtonElement>) => {
        if (e) {
            e.preventDefault();
        }

        dispatch({ type: 'RESET_APP' });
    };

    const goToDebug = () => {
        if (secretDebugCount === 9) {
            history.push('/ebpi-debug');
        } else {
            setSecretDebugCount((prev) => prev + 1);
        }
    };

    useEffect(() => {
        setSecretDebugCount(0);
    }, [username, password]);

    return (
        <div
            className={styles.login}
            style={{ background: 'linear-gradient(270deg, #383C58 0%, #4C526B 100%)' }}
        >
            <div
                className={styles.container}
                style={{ background: 'linear-gradient(270deg, #383c58 0%, #343245 100%)' }}
            >
                <img className={styles.logo} src={logo} alt="" onClick={goToDebug} />
                {supportedBrowsers.test(navigator.userAgent) && (
                    <>
                        <form
                            className={styles.form}
                            data-loading={loggingIn}
                            onSubmit={handleLogin}
                        >
                            {!authenticated && (
                                <>
                                    <label htmlFor="username" className={styles.label}>
                                        Email
                                    </label>
                                    <input
                                        autoComplete="email"
                                        autoFocus
                                        type="email"
                                        id="username"
                                        className={`${styles.inputContainer} ${styles.input}`}
                                        value={username}
                                        onChange={(e) => {
                                            setUsername(e.target.value);
                                        }}
                                    />
                                    <label htmlFor="password" className={styles.label}>
                                        Password
                                    </label>
                                    <input
                                        autoComplete="current-password"
                                        type="password"
                                        id="password"
                                        className={`${styles.inputContainer} ${styles.input}`}
                                        value={password}
                                        onChange={(e) => {
                                            setPassword(e.target.value);
                                        }}
                                    />
                                    {!store.user?.online && (
                                        <div className={styles.error}>
                                            Your device is not connected to the internet.
                                        </div>
                                    )}
                                    <div className={styles.error}>{loginError}</div>
                                    <Button type="submit">Login</Button>
                                    {/* Make tertiary */}
                                    <Link className={styles.forgot} to="/forgot-password">
                                        Forgot your password? <strong>Click here</strong>
                                    </Link>
                                    {isTablet && (
                                        <>
                                            <div className={styles.orDivider}>
                                                <span />
                                                or
                                                <span />
                                            </div>
                                            <Link
                                                className={styles.forgot}
                                                to={{
                                                    pathname: `/start-patient-session/${codeType}/${code}`,
                                                    search: location.search,
                                                }}
                                            >
                                                Open patient session with 6-Digit Code
                                            </Link>
                                        </>
                                    )}
                                </>
                            )}
                            {authenticated && <Button onClick={handleLogout}>Logout</Button>}
                        </form>
                        <div className={styles.disclaimer}>
                            Jaspr Health is intended to support crisis care and inform provider care
                            decisions; it is not a substitute for professional behavioral or medical
                            care.
                            <div
                                className={styles.version}
                            >{`${process.env.REACT_APP_VERSION}.${process.env.REACT_APP_BUILD_NUMBER}`}</div>
                        </div>
                    </>
                )}
                {!supportedBrowsers.test(navigator.userAgent) && (
                    <div className={styles.error}>Your browser is not currently supported</div>
                )}
            </div>
        </div>
    );
};

export default Login;
