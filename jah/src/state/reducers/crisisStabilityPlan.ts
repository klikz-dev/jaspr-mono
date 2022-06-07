import { CrisisStabilityPlanConstants } from 'state/constants';
import { CrisisStabilityPlan } from 'state/types';

import { ActionSetCrisisStabilityPlan } from 'state/types/actions';

const initialState: CrisisStabilityPlan = {
    reasonsLive: null,
    strategiesGeneral: null,
    strategiesFirearm: null,
    strategiesMedicine: null,
    strategiesPlaces: null,
    strategiesOther: null,
    strategiesCustom: null,
    meansSupportYesNo: null,
    meansSupportWho: null,
    copingBody: null,
    copingDistract: null,
    copingHelpOthers: null,
    copingCourage: null,
    copingSenses: null,
    supportivePeople: null,
    copingTop: null,
    wsStressors: null,
    wsThoughts: null,
    wsFeelings: null,
    wsActions: null,
    wsTop: null,
};

export type CrisisStabilityPlanState = CrisisStabilityPlan;

type CrisisStabilityPlanReducerType = ActionSetCrisisStabilityPlan;

const CrisisStabilityPlanReducer = (
    state: CrisisStabilityPlanState = initialState,
    action: CrisisStabilityPlanReducerType,
): CrisisStabilityPlanState => {
    switch (action.type) {
        case CrisisStabilityPlanConstants.SET_CRISIS_STABILITY_PLAN:
            return { ...state, ...action.crisisStabilityPlan };
        default:
            return state;
    }
};

export { CrisisStabilityPlanReducer, initialState };
