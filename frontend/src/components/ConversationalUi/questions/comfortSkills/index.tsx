import styles from './index.module.scss';
import Skills from 'pages/patient/skills';

const ComfortSkillsQuestion = (): JSX.Element => {
    return (
        <div className={styles.wrapper}>
            <Skills inCRP />
        </div>
    );
};

export { ComfortSkillsQuestion };
export default ComfortSkillsQuestion;
