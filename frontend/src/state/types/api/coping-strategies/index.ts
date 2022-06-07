/**
 * JAH Only endpoint
 * Returns a list of coping strategies
 */
export type GetResponse = {
    id: number;
    title: string;
    image: string;
    category: {
        id: number;
        name: string;
        whyText: string;
    };
}[];
