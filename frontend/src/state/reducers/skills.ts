import { SkillsConstants } from 'state/constants';
import { Skills } from 'state/types';
import { ActionSetSkills, ActionSaveSkillForLater, ActionRateSkills } from 'state/types/actions';

export type SkillReducerState = Skills;

export type SkillsReducerType = ActionSetSkills | ActionSaveSkillForLater | ActionRateSkills;

const initialState: SkillReducerState = [];

const SkillsReducer = (
    state: SkillReducerState = initialState,
    action: SkillsReducerType,
): SkillReducerState => {
    switch (action.type) {
        case SkillsConstants.SET_SKILLS:
            return [...action.skills.sort((a, b) => a.order - b.order)];
        case SkillsConstants.SAVE_SKILL_FOR_LATER:
            return state.map((skill) => {
                if (skill.id === action.skillActivity.activity) {
                    const { id, saveForLater } = action.skillActivity;
                    return {
                        ...skill,
                        saveForLater,
                        patientActivity: id !== undefined ? id : skill.patientActivity,
                    };
                }
                return skill;
            });
        case SkillsConstants.RATE_SKILL:
            return state.map((skill) => {
                if (skill.id === action.skillActivity.activity) {
                    const { id, rating } = action.skillActivity;
                    return {
                        ...skill,
                        rating,
                        patientActivity: id !== undefined ? id : skill.patientActivity,
                    };
                }
                return skill;
            });
        default:
            return state;
    }
};

export { SkillsReducer, initialState };
