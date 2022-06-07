interface CopingStrategy {
    id: number;
    title: string;
    image: string;
    category: {
        id: number;
        name: string;
        whyText: string;
    };
}

export type ResponseListCopingStrategy = CopingStrategy[];
