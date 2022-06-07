import { ComponentType, useContext, useState } from 'react';
import Modal from 'react-modal';
import { Router, Route, Switch, RouteProps, Redirect, useLocation } from 'lib/router';
import StoreContext from 'state/context/store';
import Store from 'state/store';
import rootReducer from 'state/reducers';
import IdleTimer from 'lib/idleTimer';
import ScrollToTop from 'lib/scrollTop';
import ServiceWorker from 'lib/serviceWorker';
import OnlineDetector from 'components/OnlineDetector';
import CheckInMonitor from 'components/CheckinMonitor';
import PageRouteMonitor from 'components/PageRouteMonitor';
import MaintenanceNotice from 'components/MaintenanceNotice';
import Login from 'pages/login';
import StartPatientSession from 'pages/start-patient-session';
import Timers from 'pages/patient/timers';

// Tour
import Welcome from 'pages/tour/welcome';
import Consent from 'pages/tour/consent';
import IntroVideo from 'pages/tour/introVideo';

// Tech
import TechActivation from 'pages/technician/activation';
import PatientList from 'pages/technician/patients';
import Patient from 'pages/technician/patient';

// Epic OAuth
import EpicRedirect from 'pages/technician/epic/redirect';
import EhrTimeout from 'pages/technician/ehrTimeout';

// Patient
import PatientLoadingScreen from 'pages/patient/loading';
import PatientHome from 'pages/patient';

import Code from 'pages/activation/code';
import ActivatePhone from 'pages/activation/phone';
import SetPassword from 'pages/activation/account';

import ForgotPassword from 'pages/reset-password/forgot-password';
import ResetPasswordSuccess from 'pages/reset-password/reset-password-success';

import Baseline from 'pages/patient/baseline';

import StaticMedia from 'lib/staticMedia';

// Admin
import Debug from 'pages/admin/debug';

// Freshdesk
import FreshdeskSSO from 'pages/technician/freshdesk/sso';

import ClinicMonitor from 'lib/clinicMonitor';
import UserMonitor from 'lib/userMonitor';
import Toaster from 'components/Toaster';

const Home = (props: any) => {
    const location = useLocation();
    const [store] = useContext(StoreContext);
    const { isTablet, code, codeType, loaded } = store.device;
    const { userType, authenticated } = store.user;

    if (!loaded || userType === undefined) {
        return null; // TODO Loading Screen
    } else if (userType === 'technician') {
        return (
            <Redirect
                to={{
                    pathname: '/technician/patients',
                }}
            />
        );
    } else if (userType === 'patient') {
        const {
            tourComplete,
            activities = { csp: false, csa: false },
            hasSecuritySteps,
        } = store.user;
        const isPath3 = !activities.csp && !activities.csa;
        if (tourComplete === null) return null;
        if (tourComplete || (isPath3 && hasSecuritySteps)) {
            return <PatientHome />;
        }

        if (location.pathname.startsWith('/start-patient-session')) {
            return null;
        }
        return (
            <Redirect
                to={{
                    pathname: '/welcome',
                }}
            />
        );
    }

    if (!authenticated) {
        return (
            <Redirect
                to={{
                    pathname: isTablet ? `/start-patient-session/${codeType}/${code}` : '/login',
                    search: location.search,
                }}
            />
        );
    }
    return null;
};

interface ProtectedRouteProps extends RouteProps {
    permission?: 'patient' | 'technician';
    setShowTimeoutModal?: (showTimeoutModal: boolean) => void;
    component: ComponentType<any>;
}

const ProtectedRoute = ({
    component: Component,
    permission,
    setShowTimeoutModal,
    ...rest
}: ProtectedRouteProps) => {
    const [store] = useContext(StoreContext);
    const { authenticated, userType } = store.user;
    const { loaded } = store.device;

    const route = (
        <Route
            {...rest}
            render={(props) => (
                <IdleTimer setShowTimeoutModal={setShowTimeoutModal}>
                    <Component {...props} />
                </IdleTimer>
            )}
        />
    );

    if (!permission) {
        return route;
    } else if (!loaded || userType === undefined) {
        return null; // Todo Loading screen
    } else if (authenticated && userType === permission) {
        return route;
    } else if (authenticated && userType !== permission) {
        return (
            <Route
                {...rest}
                render={(props) => (
                    <Redirect
                        to={{
                            pathname: '/',
                        }}
                    />
                )}
            />
        );
    }
    return (
        <Route
            {...rest}
            render={(props) => {
                return (
                    <Redirect
                        to={{
                            pathname: '/login',
                            state: { from: props.location },
                        }}
                    />
                );
            }}
        />
    );
};

Modal.setAppElement('#root');

const Jaspr = () => {
    const [showTimeoutModal, setShowTimeoutModal] = useState(false);

    return (
        <Store rootReducer={rootReducer}>
            <StaticMedia />
            <MaintenanceNotice />

            <div
                style={{
                    display: 'flex',
                    flexDirection: 'column',
                    flexGrow: 1,
                    backgroundColor: '#2f3251',
                }}
            >
                <Router>
                    {/* Patient Protected Pages */}
                    <ScrollToTop />
                    <PageRouteMonitor />
                    <ClinicMonitor />
                    <UserMonitor />
                    <ServiceWorker />
                    <Toaster />
                    <Switch>
                        <Route
                            path="/start-patient-session/:codeType?/:code?"
                            component={StartPatientSession}
                        />
                        <ProtectedRoute
                            exact
                            path="/welcome"
                            permission="patient"
                            component={Welcome}
                            setShowTimeoutModal={setShowTimeoutModal}
                        />
                        <ProtectedRoute
                            exact
                            path="/consent"
                            permission="patient"
                            component={Consent}
                            setShowTimeoutModal={setShowTimeoutModal}
                        />
                        <ProtectedRoute
                            exact
                            path="/intro-video"
                            permission="patient"
                            component={IntroVideo}
                            setShowTimeoutModal={setShowTimeoutModal}
                        />
                        <ProtectedRoute
                            exact
                            path="/baseline"
                            permission="patient"
                            component={Baseline}
                            setShowTimeoutModal={setShowTimeoutModal}
                        />

                        {/* Tech Protected Pages */}
                        <Route path="/technician/activate" component={TechActivation} />

                        <ProtectedRoute
                            path="/technician/patients/:patientId"
                            permission="technician"
                            component={Patient}
                        />

                        <ProtectedRoute
                            path="/technician/patients"
                            exact
                            permission="technician"
                            component={PatientList}
                            setShowTimeoutModal={setShowTimeoutModal}
                        />

                        <Route path="/login" component={Login} />
                        <Route path="/epic/redirect" component={EpicRedirect} />
                        <Route exact path="/ehr-timeout" component={EhrTimeout} />

                        <Route exact path="/activate-tools-to-go" component={ActivatePhone} />
                        <Route exact path="/activate-code" component={Code} />
                        <Route exact path="/set-password" component={SetPassword} />

                        <Route exact path="/forgot-password" component={ForgotPassword} />
                        <Route
                            exact
                            path="/password-reset/success"
                            component={ResetPasswordSuccess}
                        />
                        <ProtectedRoute
                            path="/freshdesk-sso"
                            component={FreshdeskSSO}
                            permission="technician"
                            setShowTimeoutModal={setShowTimeoutModal}
                        />
                        <Route
                            path="/reset-password/confirm"
                            render={(props) => {
                                if (props.history.location.hash.includes('userType=Technician')) {
                                    return <SetPassword />;
                                }
                                return <ActivatePhone />;
                            }}
                        />

                        <Route path="/reset-password/activate-code" component={Code} />
                        <Route path="/reset-password/set-password" component={SetPassword} />

                        {/* EBPI ADMIN ROUTES */}
                        <Route exact path="/ebpi-debug" component={Debug} />

                        <ProtectedRoute
                            exact={false}
                            path="/"
                            component={Home}
                            setShowTimeoutModal={setShowTimeoutModal}
                        />
                    </Switch>
                    <Timers
                        setShowTimeoutModal={setShowTimeoutModal}
                        showTimeoutModal={showTimeoutModal}
                    />
                    <OnlineDetector />
                    <CheckInMonitor />
                    <PatientLoadingScreen /* Should load after checking monitor and online detector */
                    />
                </Router>
            </div>
        </Store>
    );
};

export default Jaspr;
