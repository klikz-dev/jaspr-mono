import { createContext } from 'react';
interface TimerContext {
    sendHeartbeat: () => void;
}

const context = {
    sendHeartbeat: (): null => null,
};

const timerContext = createContext<TimerContext>(context);

export default timerContext;
