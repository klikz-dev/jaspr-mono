import { useEffect, useState } from 'react';
import { useHistory, useLocation } from 'lib/router';
import Dropdown from 'react-dropdown';
import Button from 'components/Button';
import styles from './index.module.scss';

export interface ViewProps {
    show: 'intro' | 'instructions' | 'breathe';
    bpm: {
        label: string;
        value: string;
    };
    setTotalBreaths: (state: (breaths: number) => number) => void;
    close: () => void;
    togglePlay: () => void;
    playing: boolean;
    totalBreaths: number;
    INITIAL_BREATHS: number;
    goInstructions: () => void;
    goBreathe: () => void;
    setBpm: (bpm: { label: string; value: string }) => void;
    remainingBreaths: number;
}

const Breathe = () => {
    const history = useHistory();
    const location = useLocation<{ from?: string }>();
    const INITIAL_BREATHS = 5;
    const [show, setShow] = useState<'intro' | 'breathe' | 'instructions'>('intro');
    const [playing, setPlaying] = useState(false);
    const [remainingBreaths, setRemainingBreaths] = useState(INITIAL_BREATHS);
    const [totalBreaths, setTotalBreaths] = useState(0);
    const [bpm, setBpm] = useState({
        label: '6 BPM',
        value: '6',
    });

    const close = () => {
        /* TODO REPLACE WITH LOCATION STATE */
        const params = new URLSearchParams(location.search || '');
        const returnUrl = params.get('return') || '/skills';
        const prevReturn = params.get('prevReturn');
        params.delete('return');
        params.delete('prevReturn');
        if (prevReturn) {
            params.set('return', prevReturn);
        }
        if (location.state?.from) {
            history.replace(location.state.from);
        } else {
            history.push({ pathname: returnUrl, search: params.toString() });
        }
    };

    const goInstructions = () => {
        setShow('instructions');
    };

    const goBreathe = () => {
        setShow('breathe');
    };

    const togglePlay = () => {
        if (!playing) {
            requestAnimationFrame(() => setPlaying(true));
        } else {
            setPlaying(false);
        }
    };

    useEffect(() => {
        if (playing && totalBreaths > 0 && INITIAL_BREATHS - totalBreaths >= 0) {
            setRemainingBreaths((prevBreaths) => prevBreaths - 1);
        }
    }, [playing, totalBreaths]);

    return (
        <div className={styles.breathe} data-play={playing} data-speed={bpm.value}>
            <div className={styles.close} onClick={close}>
                ⨉
            </div>
            {show === 'intro' && (
                <div
                    className={styles.intro}
                    style={{ boxShadow: '1px 2px 7px 0 rgba(0, 0, 0, 0.2)' }}
                >
                    <h5>Paced Breathing</h5>
                    <p className="typography--body1">
                        Our breathing changes when we are stressed or in pain. Slow and smooth
                        breathing can calm our nervous system and heart rate, and soothe our
                        emotions. This activity helps you learn this skill of calm breathing.
                    </p>
                    <div className={styles.buttons}>
                        <Button onClick={goInstructions}>Take me to the activity</Button>
                        <Button variant="secondary" onClick={close}>
                            Take me back to Comfort &amp; Skills
                        </Button>
                    </div>
                </div>
            )}
            {show === 'instructions' && (
                <>
                    <div className={styles.instructions}>
                        <p className="typography--h5">
                            Before you start take a normal breath, then take a deep breath.
                        </p>
                        <p className="typography--h5">
                            Breathe in slowly through your nose. Let your belly and chest expand.
                        </p>
                        <p className="typography--h5">
                            Breathe out slowly through your mouth, pursing your lips.
                        </p>
                    </div>
                    <Button onClick={goBreathe}>Got it</Button>
                </>
            )}
            {show === 'breathe' && (
                <>
                    <Dropdown
                        className={styles.bpmSelector}
                        controlClassName={styles.control}
                        placeholderClassName={styles.placeholder}
                        arrowClassName={styles.arrow}
                        menuClassName={styles.menu}
                        value={bpm}
                        placeholder={bpm.label}
                        // @ts-ignore The Option label expects a React.Node
                        onChange={(value) => setBpm(value)}
                        options={[
                            {
                                label: '2 BPM',
                                value: '2',
                            },
                            {
                                label: '3 BPM',
                                value: '3',
                            },
                            {
                                label: '4 BPM',
                                value: '4',
                            },
                            {
                                label: '5 BPM',
                                value: '5',
                            },
                            {
                                label: '6 BPM',
                                value: '6',
                            },
                            {
                                label: '7 BPM',
                                value: '7',
                            },
                            {
                                label: '8 BPM',
                                value: '8',
                            },
                        ]}
                    />
                    {remainingBreaths === INITIAL_BREATHS && (
                        <div className={styles.step}>
                            Let's start with {INITIAL_BREATHS} breaths.
                        </div>
                    )}
                    {remainingBreaths > 0 && remainingBreaths < INITIAL_BREATHS && (
                        <div className={styles.step}>
                            {remainingBreaths} more breath{remainingBreaths > 1 ? 's' : ''}.
                        </div>
                    )}
                    {remainingBreaths === 0 && (
                        <div className={styles.step}>
                            You've taken {totalBreaths} calming breaths.
                        </div>
                    )}

                    <div className={styles.breatheContainer}>
                        <ul className={styles.circleContainer}>
                            {[...Array(100)].map((e, i) => (
                                <li key={i} data-circle-num={i}>
                                    <div />
                                </li>
                            ))}
                        </ul>
                        <div
                            className={styles.orbiter}
                            onAnimationIteration={() =>
                                setTotalBreaths((prevBreaths) => prevBreaths + 1)
                            }
                        />
                        <div className={styles.inner} />
                        <div className={styles.text}>
                            <span data-text="ready">Ready?</span>
                            <span data-text="inhale">Inhale</span>
                            <span data-text="hold">Hold it</span>
                            <span data-text="exhale">Exhale</span>
                        </div>
                    </div>
                    <Button
                        //className={styles.button}
                        dark
                        onClick={totalBreaths >= INITIAL_BREATHS ? close : togglePlay}
                    >
                        {playing && totalBreaths >= INITIAL_BREATHS && "I'm done"}
                        {playing && totalBreaths < INITIAL_BREATHS && 'Pause'}
                        {!playing && totalBreaths === 0 && 'Start'}
                        {!playing && totalBreaths > 0 && 'Resume'}
                    </Button>
                </>
            )}
        </div>
    );
};

export default Breathe;
