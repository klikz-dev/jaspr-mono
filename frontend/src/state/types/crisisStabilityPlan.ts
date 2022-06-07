export interface CrisisStabilityPlan {
    reasonsLive: string[] | null;
    strategiesGeneral: string[] | null;
    strategiesFirearm: string[] | null;
    strategiesMedicine: string[] | null;
    strategiesPlaces: string[] | null;
    strategiesOther: string[] | null;
    strategiesCustom: string[] | null;
    meansSupportYesNo: boolean | null;
    meansSupportWho: string | null;
    copingBody: string[] | null;
    copingDistract: string[] | null;
    copingHelpOthers: string[] | null;
    copingCourage: string[] | null;
    copingSenses: string[] | null;
    supportivePeople: { name: string; phone: string }[] | null;
    copingTop: string[] | null;
    wsStressors: string[] | null;
    wsThoughts: string[] | null;
    wsFeelings: string[] | null;
    wsActions: string[] | null;
    wsTop: string[] | null;
}
