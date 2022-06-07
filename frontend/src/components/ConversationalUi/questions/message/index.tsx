import { useContext, useEffect, useState } from 'react';
import template from 'lodash/template';
import StoreContext from 'state/context/store';
import Loading from '../loading';
import styles from './index.module.scss';
import jazIcon from 'assets/jazz.png';
import jasperIcon from 'assets/jasper.png';
import { Patient } from 'state/types';

interface Props {
    currentQuestion: boolean;
    message: string;
    index: number;
}

export interface ViewProps {
    index: number;
    isHidden: boolean;
    isLoading: boolean;
    guide: 'Jasper' | 'Jaz' | null;
    templatedMessage: string;
}

const Message = (props: Props): JSX.Element => {
    const { currentQuestion, index, message } = props;
    const [store] = useContext(StoreContext);
    const { user } = store;
    const { guide } = user as Patient;
    // Set these false by default and change to true in the onMount
    // useEffect so we can get a correctly calculated content height
    const [isHidden, setIsHidden] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    let templatedMessage = message;
    try {
        templatedMessage = template(message)({ guide });
    } catch {
        templatedMessage = message;
    }

    useEffect(() => {
        // Set these here, instead of as default values so final view size can be calculated with useLayoutEffect
        if (currentQuestion) {
            setIsHidden(true);
            setIsLoading(true);
            const loadingTimer = setTimeout(() => {
                setIsLoading(false);
            }, (index + 1) * 1500);
            const hiddenTimer = setTimeout(() => setIsHidden(false), index * 1500);
            return () => {
                clearTimeout(hiddenTimer);
                clearTimeout(loadingTimer);
            };
        } else {
            setIsHidden(false);
            setIsLoading(false);
        }
    }, [index, currentQuestion]);

    return (
        <>
            {!isHidden && isLoading && <Loading />}
            {!isHidden && !isLoading && (
                <div className={styles.container} style={{ margin: '14px 180px 14px 80px' }}>
                    <img
                        className={styles.guide}
                        style={{
                            borderRadius: '50%',
                        }}
                        src={guide === 'Jasper' ? jasperIcon : jazIcon}
                        alt={`Your guide ${guide || 'Jaz'}`}
                    />
                    <div
                        className={`typography--body1 ${styles.message}`}
                        style={{ marginLeft: '1rem' }}
                    >
                        {templatedMessage}
                    </div>
                </div>
            )}
        </>
    );
};

export { Message };
export default Message;
