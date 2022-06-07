import styles from './index.module.scss';

const LethalMeans = ({ assessment }: any) => {
    const nullOrUndefined = (value: any): boolean => {
        return value === null || value === undefined;
    };

    const didNotAnswer = <span className={styles.didNotAnswer}>Patient did not answer yet</span>;

    const yesNoify = (value: boolean | null) => {
        if (value === true) {
            return 'Yes';
        }
        if (value === false) {
            return 'No';
        }
        return didNotAnswer;
    };

    const hasAnswered = () => {
        return Boolean(
            assessment?.meansYesNo ||
                assessment?.meansYesNoDescribe ||
                assessment?.firearmsYesNo ||
                assessment?.firearmsYesNoDescribe ||
                assessment?.meansWilling,
        );
    };

    return (
        <div className={styles.container}>
            <h3 className="typography--overline">Lethal Means Snapshot</h3>
            {hasAnswered() && (
                <>
                    <h4 className="typography--overline">Access to Means</h4>
                    <div className={styles.dataPoint}>
                        <div className={`typography--body2 ${styles.label}`}>
                            <div
                                className={
                                    nullOrUndefined(assessment?.meansYesNo)
                                        ? styles.triangle
                                        : styles.circle
                                }
                            />
                            {yesNoify(assessment?.meansYesNo)}
                        </div>
                        <div className={`typography--caption ${styles.describe}`}>
                            {assessment?.meansYesNoDescribe ? (
                                <span>{assessment?.meansYesNoDescribe}</span>
                            ) : (
                                didNotAnswer
                            )}
                        </div>
                    </div>
                    <h4 className="typography--overline">Access to Firearms</h4>
                    <div className={styles.dataPoint}>
                        <div className={`typography--body2  ${styles.label}`}>
                            <div
                                className={
                                    nullOrUndefined(assessment?.firearmsYesNo)
                                        ? styles.triangle
                                        : styles.circle
                                }
                            />
                            {yesNoify(assessment?.firearmsYesNo)}
                        </div>
                        <span className={`typography--caption ${styles.describe}`}>
                            {assessment?.firearmsYesNoDescribe ? (
                                <span>{assessment?.firearmsYesNoDescribe}</span>
                            ) : (
                                didNotAnswer
                            )}
                        </span>
                    </div>
                    <h4 className="typography--overline">Willingness to Secure Means</h4>
                    <div className={styles.dataPoint}>
                        <div className={`typography--body2  ${styles.label}`}>
                            <div
                                className={
                                    nullOrUndefined(assessment?.meansWilling)
                                        ? styles.triangle
                                        : styles.circle
                                }
                            />
                            {assessment?.meansWilling || didNotAnswer}
                        </div>
                    </div>
                </>
            )}
            {!hasAnswered() && (
                <p className="typography--body3" style={{ color: 'rgba(77, 77, 77, 1)' }}>
                    Lethal means counseling is offered with assigned suicide assessment and crisis
                    stability planning activities.
                </p>
            )}
        </div>
    );
};

export default LethalMeans;
