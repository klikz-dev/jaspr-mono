import styles from './index.module.scss';
import SavedSkillsListItem from '../savedSkillsListItem';
import SavedSkillsListItemAdd from '../savedSkillsListItemAdd';

import { Skills, Skill } from 'state/types';

type SavedSkillsListProps = {
    skills: Skills;
    onAdd?: () => void;
    onRemove?: (skill: Skill) => void;
    setQuestionDisableAudio?: (disable: boolean) => void;
};

const SavedSkillsList = (props: SavedSkillsListProps): JSX.Element => {
    const { skills, onAdd, onRemove, setQuestionDisableAudio } = props;
    return (
        <ul className={styles.list}>
            {skills.map((skill) => (
                <SavedSkillsListItem
                    skill={skill}
                    onRemove={onRemove}
                    key={skill.id}
                    setQuestionDisableAudio={setQuestionDisableAudio}
                />
            ))}
            {onAdd && <SavedSkillsListItemAdd onAdd={onAdd} />}
        </ul>
    );
};

export default SavedSkillsList;
