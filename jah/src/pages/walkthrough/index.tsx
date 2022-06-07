import React, { useContext, useEffect, useState } from 'react';
import { Modal } from 'react-native';
import { useHistory } from 'lib/router';
import Styled from 'styled-components/native';
import { addAction, actionNames } from 'state/actions/analytics';
import { getWalkthrough } from 'state/actions/assessment';
import { getCrisisStabilityPlan } from 'state/actions/crisisStabilityPlan';
import StoreContext from 'state/context/store';
import TitleMenu from 'components/TitleMenu';
import Controls from 'pages/walkthrough/controls';
import BreatheComponent from './breathe';
import ContactComponent from './contact';
import CopingComponent from './copingStrategy';
import GuideComponent from './guide';
import LethalMeansComponent from './lethalMeans';
import ReasonsLiveComponent from './reasonsLive';
import VideoComponent from './video';
import Recap from './recap';

const Background = Styled.View`
    flex: 1;
    background-color: #232542;
`;

const Container = Styled.View`
    flex: 1;
    overflow: hidden;
    border-top-left-radius: 30px;
    border-top-right-radius: 30px;
    margin-horizontal: 18px;
    margin-top: 18px;
    background-color: #2F344F;
`;

type FrontendRenderType =
    | 'videoDescription'
    | 'video'
    | 'sharedStory'
    | 'breathe'
    | 'guide'
    | 'copingStrategy'
    | 'reasonsForLiving'
    | 'personalizedLethalMeans'
    | 'supportivePeople'
    | 'nationalHotline'
    | 'recap';

const selectWalkthroughType = (
    frontendRenderType: FrontendRenderType,
    stepName: string,
    value: any, // TODO Fix type
    steps: string[] = [],
) => {
    switch (frontendRenderType) {
        case 'videoDescription':
            return <VideoComponent key={value?.id} showDescription {...value} />;
        case 'video':
            return <VideoComponent key={value?.id} {...value} />;
        case 'sharedStory':
            return <VideoComponent key={value?.id} {...value} sharedStory />;
        case 'breathe':
            return <BreatheComponent />;
        case 'guide':
            return <GuideComponent value={value?.message} />;
        case 'copingStrategy':
            return <CopingComponent {...value} />;
        case 'reasonsForLiving':
            return <ReasonsLiveComponent />;
        case 'personalizedLethalMeans':
            return <LethalMeansComponent />;
        case 'supportivePeople':
            return <ContactComponent personalContact {...value} text={value?.phone} />;
        case 'nationalHotline':
            return <ContactComponent {...value} name={stepName} />;
        case 'recap':
            return <Recap steps={steps} />;
        default:
            return null;
    }
};

const Walkthrough = () => {
    const history = useHistory();
    const [store, dispatch] = useContext(StoreContext);
    const { assessment, user } = store;
    const { token } = user;
    const { walkthrough } = assessment;
    const [stepIdx, setStepIdx] = useState(0);
    const [showMenu, setShowMenu] = useState(false);
    const lastStep = stepIdx === walkthrough.length - 1;

    useEffect(() => {
        getWalkthrough(dispatch);
    }, [dispatch]);

    useEffect(() => {
        if (walkthrough.length) {
            const { stepName } = walkthrough[stepIdx];
            // TODO Do we want to add additional details from the value object about the step?
            addAction(actionNames.JAH_WALKTHROUGH_ARRIVE, { extra: stepName });
        }
    }, [walkthrough, stepIdx]);

    useEffect(() => {
        if (token) {
            getCrisisStabilityPlan(dispatch);
        }
    }, [dispatch, token]);

    useEffect(() => {
        return () => {
            addAction(actionNames.JAH_WALKTHROUGH_END);
        };
    }, []);

    if (walkthrough.length === 0) return null;
    const { frontendRenderType, stepName, value } = walkthrough[stepIdx];
    const steps = walkthrough.map((sw: any) => {
        if (sw.frontendRenderType === 'copingStrategy') {
            return sw.value.title;
        } else if (sw.frontendRenderType === 'video') {
            return sw.value.name;
        } else if (sw.frontendRenderType === 'supportivePeople') {
            return sw.value.name;
        }
        return sw.stepName;
    });
    return (
        <Background>
            <TitleMenu label="Distress Survival Guide" />
            <Container>
                {selectWalkthroughType(frontendRenderType, stepName, value, steps)}
                <Controls lastStep={lastStep} setStepIdx={setStepIdx} setShowMenu={setShowMenu} />
            </Container>

            <Modal visible={showMenu}>
                <Background>
                    <TitleMenu label="Distress Survival Guide" />
                    <Container>
                        <Recap
                            setStepIdx={setStepIdx}
                            close={() => setShowMenu(false)}
                            steps={steps}
                        />
                    </Container>
                </Background>
            </Modal>
        </Background>
    );
};

export default Walkthrough;
