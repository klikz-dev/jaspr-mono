/**
 * JAH Only endpoint
 * Get the crisis stability plan
 */
export interface GetResponse {
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

/**
 * JAH Only endpoint
 */
export type PatchResponse = GetResponse;

/**
 * JAH Only endpoint
 */
export type PatchRequest = Partial<PatchResponse>;
