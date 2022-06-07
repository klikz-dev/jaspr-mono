import { createContext, Dispatch, SetStateAction } from 'react';

interface IAnswerContext {
    answers: { [key: string]: any };
    updateAnswers: Dispatch<SetStateAction<{ [key: string]: any }>>;
}

export const AnswerContext = createContext<IAnswerContext>({
    answers: {},
    updateAnswers: () => {},
});
