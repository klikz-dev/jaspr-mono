export interface Props {
    currentTime: number;
    duration: number;
    pause: () => void;
    play: () => void;
    seek: (time: number) => void;
    seekEnd: (time: number) => void;
}
