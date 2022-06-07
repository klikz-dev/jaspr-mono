import React, { ComponentType, useContext, useState } from 'react';
import Styled from 'styled-components/native';
import { Router, Route, RouteProps, Redirect, BackButton } from 'lib/router';
import StoreContext from 'state/context/store';
import Store from 'state/store';
import rootReducer from 'state/reducers';
import CacheControl from 'lib/cacheControl';
import ScreenLock from 'lib/screenLock';
import StateMonitor from 'lib/stateMonitor';
import NativeStatusBar from 'components/NativeStatusBar';
import OnlineDetector from 'components/OnlineDetector';
import PageRouteMonitor from 'components/PageRouteMonitor';
import ErrorBoundary from 'components/UnhandledError';
import HandledError from 'components/HandledError';
import MaintenanceNotice from 'components/MaintenanceNotice';

import Login from 'pages/login';

// Patient
import Breathe from 'pages/breathe';
import Stories from 'pages/stories';
import Skills from 'pages/skills';
import Account from 'pages/account';
import ChangePassword from 'pages/account/change-password';

// JAH
import JahHome from 'pages/home/index';
import JahStabilityPlaylist from 'pages/stabilityPlaylist';
import JahFavorites from 'pages/home/favorites';
import JahContacts from 'pages/contacts';
import JahSupportivePeopleInfo from 'pages/contacts/supportivePeopleInfo';
import JahSupportivePeople from 'pages/contacts/supportivePeople';
import JAHSupportivePeopleEdit from 'pages/contacts/supportivePeople/EditContact';
import JahConversationStarters from 'pages/contacts/conversationStarters';
import JahContactsSharedStories from 'pages/contacts/sharedStories';
import JAHContactsHotlineContacts from 'pages/contacts/hotlineContacts';
import JahContactsHotlineInfo from 'pages/contacts/hotlineInfo';
import JahContactsHotlineCrisisLines from 'pages/contacts/hotlineInfo/crisisLines';
import JahContactsHotlineInfoCommonConcerns from 'pages/contacts/hotlineInfo/commonConcerns';
import JahContactsHotlineInfoWhatToExpect from 'pages/contacts/hotlineInfo/whatToExpect';
import JahWalkthrough from 'pages/walkthrough';
import JahStabilityPlanWarningSignals from 'pages/stabilityPlaylist/warningSignals';
import JahStabilityPlanWarningSignalsFullList from 'pages/stabilityPlaylist/warningSignals/fullList';
import JAHStabilityPlanWarningSignalsEdit from 'pages/stabilityPlaylist/warningSignals/fullList/edit';
import JahStabilityPlanReasonsLive from 'pages/stabilityPlaylist/reasonsLive';
import JAHStabilityPlanReasonsLiveEdit from 'pages/stabilityPlaylist/reasonsLive/edit';
import JahStabilityPlanSaferHome from 'pages/stabilityPlaylist/saferHome';
import JahStabilityPlanSaferHomeFullList from 'pages/stabilityPlaylist/saferHome/fullList';
import JAHStabilityPlanSaferHomeEdit from 'pages/stabilityPlaylist/saferHome/fullList/edit';
import JahStabilityPlanCopingStrategies from 'pages/stabilityPlaylist/copingStrategies';
import JahStabilityPlanCopingStrategiesFullList from 'pages/stabilityPlaylist/copingStrategies/fullList';
import JAHStabilityPlanCopingStrategiesEdit from 'pages/stabilityPlaylist/copingStrategies/fullList/edit';
import JahSignup from 'pages/signup';
import JahOnboarding from 'pages/onboarding';
import JahForgotPassword from 'pages/forgotPassword';
import StaticMedia from 'lib/staticMedia';

// Admin
import { Patient as PatientType } from 'state/types';

const ContainerView = Styled.View`
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    background-color: #2f3251;
`;

const Home = (props: any) => {
    const [store] = useContext(StoreContext);
    const { userType } = store.user;
    if (userType === undefined) {
        return null; // TODO Loading Screen
    } else if (userType === 'patient') {
        const { tourComplete, /* resetPassword, */ onboarded } = store.user as PatientType;
        if (tourComplete === null) return null;
        if (!onboarded) {
            return (
                <Redirect
                    to={{
                        pathname: '/jah-onboarding',
                    }}
                />
            );
        }
        return <JahHome />;
    }

    return <Login {...props} />;
};

interface ProtectedRouteProps extends RouteProps {
    timeout?: number;
    component: ComponentType<any>;
}

const ProtectedRoute = ({ component: Component, timeout, ...rest }: ProtectedRouteProps) => {
    const [store] = useContext(StoreContext);
    const { authenticated, userType } = store.user;

    const route = <Route {...rest} render={(props) => <Component {...props} />} />;

    if (userType === undefined) {
        return null; // Todo Loading screen
    } else if (authenticated) {
        return route;
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

const Jaspr = () => {
    return (
        <ErrorBoundary>
            <Store rootReducer={rootReducer}>
                <NativeStatusBar />
                <ScreenLock />
                <StaticMedia />
                <StateMonitor />
                <MaintenanceNotice />

                <ContainerView>
                    <Router>
                        {/* Patient Protected Pages */}
                        <BackButton />
                        <CacheControl />
                        <PageRouteMonitor />

                        <ProtectedRoute exact path="/breathe" component={Breathe} />

                        <ProtectedRoute exact path="/stories" component={Stories} />

                        <ProtectedRoute exact path="/skills" component={Skills} />

                        <ProtectedRoute exact path="/account" component={Account} />

                        <ProtectedRoute exact path="/change-password" component={ChangePassword} />

                        <ProtectedRoute exact path="/" component={Home} />

                        <ProtectedRoute exact path="/jah-favorites" component={JahFavorites} />

                        <ProtectedRoute
                            exact
                            path="/jah-stability-playlist"
                            component={JahStabilityPlaylist}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-stability-playlist/warning-signals"
                            component={JahStabilityPlanWarningSignals}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-stability-playlist/warning-signals/full"
                            component={JahStabilityPlanWarningSignalsFullList}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-stability-playlist/warning-signals/edit"
                            component={JAHStabilityPlanWarningSignalsEdit}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-stability-playlist/making-home-safer"
                            component={JahStabilityPlanSaferHome}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-stability-playlist/making-home-safer/full"
                            component={JahStabilityPlanSaferHomeFullList}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-stability-playlist/making-home-safer/edit"
                            component={JAHStabilityPlanSaferHomeEdit}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-stability-playlist/reasons-for-living"
                            component={JahStabilityPlanReasonsLive}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-stability-playlist/reasons-for-living/edit"
                            component={JAHStabilityPlanReasonsLiveEdit}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-stability-playlist/coping-strategies"
                            component={JahStabilityPlanCopingStrategies}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-stability-playlist/coping-strategies/full"
                            component={JahStabilityPlanCopingStrategiesFullList}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-stability-playlist/coping-strategies/edit"
                            component={JAHStabilityPlanCopingStrategiesEdit}
                        />

                        <ProtectedRoute exact path="/jah-contacts" component={JahContacts} />

                        <ProtectedRoute
                            exact
                            path="/jah-supportive-people"
                            component={JahSupportivePeople}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-supportive-people/edit"
                            component={JAHSupportivePeopleEdit}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-supportive-people/edit/:contactId"
                            component={JAHSupportivePeopleEdit}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-supportive-people-info"
                            component={JahSupportivePeopleInfo}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-conversation-starters"
                            component={JahConversationStarters}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-contacts/shared-stories"
                            component={JahContactsSharedStories}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-contacts/hotline-info"
                            component={JahContactsHotlineInfo}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-contacts/hotlines"
                            component={JAHContactsHotlineContacts}
                        />
                        <ProtectedRoute
                            exact
                            path="/jah-contacts/hotline-info/crisis-lines"
                            component={JahContactsHotlineCrisisLines}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-contacts/hotline-info/common-concerns"
                            component={JahContactsHotlineInfoCommonConcerns}
                        />

                        <ProtectedRoute
                            exact
                            path="/jah-contacts/hotline-info/what-to-expect"
                            component={JahContactsHotlineInfoWhatToExpect}
                        />

                        <ProtectedRoute exact path="/jah-walkthrough" component={JahWalkthrough} />

                        <ProtectedRoute exact path="/jah-onboarding" component={JahOnboarding} />

                        <Route exact path="/jah-signup" component={JahSignup} />

                        <Route exact path="/jah-forgot-password" component={JahForgotPassword} />

                        <Route path="/login" component={Login} />

                        <HandledError />
                        <OnlineDetector />
                    </Router>
                </ContainerView>
            </Store>
        </ErrorBoundary>
    );
};

export default Jaspr;
