import AddButton from '../../Components/AddButton';
import Section from '../../Components/Section';
import styles from './index.module.scss';
import { AssessmentAnswers } from 'state/types';

interface SupportivePeopleTabProps {
    setAnswers: (
        answers:
            | Partial<AssessmentAnswers>
            | ((answers: Partial<AssessmentAnswers>) => Partial<AssessmentAnswers>),
    ) => void;
    answers: Partial<AssessmentAnswers>;
}

const SupportivePeopleTab = ({ answers, setAnswers }: SupportivePeopleTabProps) => {
    const { supportivePeople = [{ name: '', phone: '' }] } = answers;

    const addNewPerson = () => {
        setAnswers((answers) => ({
            ...answers,
            supportivePeople: [...(answers.supportivePeople || []), { name: '', phone: '' }],
        }));
    };

    const editName = (value: string, idx: number): void => {
        setAnswers((answers) => {
            const supportivePeople = [...(answers.supportivePeople || [{ name: '', phone: '' }])];
            supportivePeople[idx].name = value;
            return {
                ...answers,
                supportivePeople,
            };
        });
    };

    const editPhone = (value: string, idx: number): void => {
        setAnswers((answers) => {
            const supportivePeople = [...(answers.supportivePeople || [{ name: '', phone: '' }])];
            supportivePeople[idx].phone = value;
            return {
                ...answers,
                supportivePeople,
            };
        });
    };

    const remove = (idx: number): void => {
        setAnswers((answers) => {
            const supportivePeople = [...(answers.supportivePeople || [{ name: '', phone: '' }])];
            supportivePeople.splice(idx, 1);
            return {
                ...answers,
                supportivePeople,
            };
        });
    };

    return (
        <Section
            number="2"
            title="Supportive People"
            tooltip="Are there people who help you feel better when you're upset? Any professionals who can help when things are hardest?"
        >
            <div className={styles.people}>
                <div className={styles.fieldHeaders}>
                    <span className={styles.headerName}>NAME</span>
                    <span className={styles.headerPhone}>PHONE NUMBER</span>
                </div>

                {(supportivePeople || [{ name: '', phone: '' }]).map((person, idx) => (
                    <div className={styles.person} key={idx}>
                        <input
                            className={styles.name}
                            value={person.name || ''}
                            placeholder="Type name here"
                            onChange={({ target }) => editName(target.value, idx)}
                        />
                        <input
                            className={styles.phone}
                            value={person.phone || ''}
                            type="tel"
                            pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"
                            placeholder="Type number here"
                            onChange={({ target }) => editPhone(target.value, idx)}
                        />
                        <button className={styles.remove} onClick={() => remove(idx)}>
                            &#10006;
                        </button>
                    </div>
                ))}
                <AddButton onClick={addNewPerson} />
            </div>
        </Section>
    );
};

export default SupportivePeopleTab;
