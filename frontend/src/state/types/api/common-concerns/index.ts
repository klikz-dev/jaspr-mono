/**
 * JAH Only endpoint
 * Returns a list of common concerns
 */
export type GetResponse = {
    id: number;
    title: string;
    content: string;
}[];
