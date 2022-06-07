import re
from typing import Dict, List, Optional
from django.db.models import Model
from django.db import transaction
from django.utils.functional import cached_property
from django.db.models import Prefetch


from jaspr.apps.kiosk.models import AssignedActivity
from jaspr.apps.kiosk.activities.activity_utils import ActivityType
from .question_json import underscore_to_camel, create_section_dictionary, \
    get_question_action, section_uid_to_answer_key, camelcase_to_underscore

"""
Assigned: CSA, CSP, C&S

Activities: Intro, CSA, LMC, CSP, Outro, C&S
"""

EXPLICIT_ACTIVITIES = [
    ActivityType.SuicideAssessment,
    ActivityType.StabilityPlan,
    ActivityType.ComfortAndSkills,
]


def sort_activities_by_priority(activities):
    count = len(activities)
    if count > 3:
        raise Exception("Can't get priority of more than 3 activities")

    if count == 1:
        return activities
    elif count == 2:
        if EXPLICIT_ACTIVITIES.index(activities[0]) < EXPLICIT_ACTIVITIES.index(activities[1]):
            return activities
        return [activities[1], activities[0]]
    # else
    result = [None, None, None]
    for x in range(len(activities)):
        act = activities[x]
        index = EXPLICIT_ACTIVITIES.index(act)
        result[index] = act
    return result


class ActivityManagerMixin(Model):

    class Meta:
        abstract = True

    def filter_activities(self, active_only=False, explicit_only=False) -> List[AssignedActivity]:
        act_count = {}
        active_activities = []
        # This function depends on assignedactivity_set having an .order_by("-created").  We run the order_by
        # in the prefetch to prevent requerying here, so it should already be sorted.  We sort explicilty in
        # application space to improve performance since this function is called repeatably during many requests
        activities = sorted(
            self.assignedactivity_set.all(),
            key=lambda x: x.created, reverse=True
        )

        for activity in activities:
            at = activity.type
            if not explicit_only or at in EXPLICIT_ACTIVITIES:
                if at not in act_count:
                    act_count[at] = 0
                act_count[at] += 1
                if not active_only or act_count[at] <= 1:
                    active_activities.append(activity)
        active_activities.reverse()
        return active_activities

    def get_explicit_activities(self, active_only=False):
        return self.filter_activities(active_only=active_only, explicit_only=True)

    def has_activity(self, activity_type: ActivityType):
        for activity in self.assignedactivity_set.all():
            if activity.type == activity_type:
                return True
        return False

    def get_activity(self, type: ActivityType):
        # This function depends on assignedactivity_set having an .order_by("-created").  We run the order_by
        # in the prefetch to prevent requerying here, so it should already be sorted.  We sort explicilty in
        # application space to improve performance since this function is called repeatably during many requests
        activities = sorted(
            self.assignedactivity_set.all(),
            key=lambda x: x.created, reverse=True
        )

        for activity in activities:
            if activity.type == type:
                return activity.get_active_module()
        return None

    def add_activities(self, activities: List[ActivityType]) -> None:
        """
        TODO: Should CSA's and CSP's be started from scratch?
        If a new CSA is added, should the existing one be locked?
        If a new activity is added, should any previously added activities be locked?
        How do we want the API to work to specify whats active?
        """
        if len(activities) > 3:
            raise Exception("Only three activities allowed to be added at a time")
        activities = sort_activities_by_priority(activities)
        assigned_activities = []
        append_outro = False
        lmc_added = False
        current_answers = self.get_answers().get('answers')
        # Remove supportive_people from previous answers if they are null as they won't validate
        if "supportive_people" in current_answers and current_answers['supportive_people'] is None:
            current_answers.pop("supportive_people")

        if not self.has_activity(ActivityType.Intro):
            assigned_activities.append(self._create_intro())

        for x in range(len(activities)):
            ca = activities[x]
            if ca.is_implicit():
                raise Exception("Can only provide explicit activities to the add_activites function")

            if ca is ActivityType.SuicideAssessment:
                assigned_activities.append(self._create_csa())
                if not self.has_activity(ActivityType.LethalMeans):
                    lmc_added = True
                    assigned_activities.append(self._create_lmc())
                append_outro = True
            elif ca is ActivityType.StabilityPlan:
                if not self.has_activity(ActivityType.LethalMeans) and not lmc_added:
                    lmc_added = True
                    assigned_activities.append(self._create_lmc())
                csp = self._create_csp()
                assigned_activities.append(csp)
                csp.save_answers(current_answers)
                if not append_outro:
                    append_outro = True
            elif ca is ActivityType.ComfortAndSkills:
                assigned_activities.append(self._create_cs())

        if append_outro:
            assigned_activities.append(self._create_outro())

        try:
            # Remove cached property so it can be refreshed
            del self.sections_dictionary
        except AttributeError:
            # Property has not been cached
            pass

        try:
            # Remove cached property so it can be refreshed
            del self.section_uid_ordered_list
        except AttributeError:
            # Property has not been cached
            pass

        # Keep patients on the current question unless that question has been moved (e.g. if they are on an outro
        # question and a new outro is assigned, make sure to assign the patient to the first question of the new
        # activities)

        found_uid = False
        current_index = self.get_safe_index(self.current_section_uid)
        for activity in assigned_activities:
            questions = activity.get_questions()
            for question in questions:
                if "uid" in question:
                    if question["uid"].startswith('progressBar') or question["uid"].startswith('sectionChange'):
                        continue
                    if current_index > self.get_safe_index(camelcase_to_underscore(question["uid"])):
                        self.current_section_uid = camelcase_to_underscore(question["uid"])
                        self.save()
                        found_uid = True
                    break
            if found_uid:
                break

        return None

    def _create_intro(self):
        # Need to import here due to circular reference
        from jaspr.apps.kiosk.activities.intro.factory import create
        return create(self)

    def _create_csa(self):
        # Need to import here due to circular reference
        from jaspr.apps.kiosk.activities.suicide_assessment.factory import create
        return create(self)

    def _create_csp(self):
        # Need to import here due to circular reference
        from jaspr.apps.kiosk.activities.stability_plan.factory import create
        return create(self)

    def _create_outro(self):
        # Need to import here due to circular reference
        from jaspr.apps.kiosk.activities.outro.factory import create
        return create(self)

    def _create_lmc(self):
        # Need to import here due to circular reference
        from jaspr.apps.kiosk.activities.lethal_means.factory import create
        return create(self)

    def _create_cs(self):
        # Need to import here due to circular reference
        from jaspr.apps.kiosk.activities.comfort_and_skills.factory import create
        return create(self)

    def get_questions(self) -> List:
        """
        Returns all the questions from active activities for an encounter as a flat list.
        """
        questions = []
        for activity in self.filter_activities(active_only=True):
            locked = activity.locked
            questions = questions + [dict(question, **{'locked': locked}) for question in activity.get_questions()]
        return questions

    def get_next_section_uid(self, section_uid: Optional[str] = None, unlocked_only: bool = True) -> Optional[str]:
        if not section_uid:
            section_uid = self.current_section_uid
        section_uid = underscore_to_camel(section_uid)
        questions = self.get_questions()
        index = -1
        for i, question in enumerate(questions):
            if question["uid"] == section_uid:
                index = i + 1
                break

        if index > -1 and i < len(questions) - 1:
            for question in questions[index:]:
                if not unlocked_only or not question["locked"]:
                    return camelcase_to_underscore(question["uid"])

        return None

    def get_answers(self) -> dict:
        answers = {}
        metadata = {
            "current_section_uid": self.get_current_section_uid(),
        }
        # grab the last activities first so the new ones override them
        for activity in reversed(self.filter_activities(active_only=True)):
            act_answers = activity.get_answers()
            if act_answers is not None:
                answers.update(act_answers)
            act_metadata = activity.get_metadata()
            if act_metadata is not None:
                metadata.update(act_metadata)
        return {
            "answers": answers,
            "metadata": metadata
        }

    def save_answers(self, answers: dict, takeaway_kit: bool = False) -> None:

        # We place a read lock on encounter using select_for_update so that multiple simultaneous requests do not
        # clobber each other.  We do not put a read lock on each individual activity since we can't do
        # select_for_update on nullable joins, and selecting each individually would greatly increase the number
        # of database requests.  Locking the encounter should be sufficient for blocking requests since we typically
        # only interact with the activities through the encounter object.
        with transaction.atomic():
            instance = type(self).objects.select_for_update(of=('self',)).select_related('patient',
                                                                                         'department').prefetch_related(
                Prefetch(
                    "assignedactivity_set",
                    queryset=AssignedActivity.objects.order_by("-created").select_related(
                        'stability_plan', 'suicide_assessment', 'comfort_and_skills', 'intro', 'outro', 'lethal_means'
                    ).prefetch_related(
                        "assignmentlocks_set",
                    ),
                )).get(pk=self.pk)
            last_section_uid = instance.get_last_section_uid(answers)
            if last_section_uid is not None and not takeaway_kit:
                # save_answer below causes an update_status already so don't do it here
                instance.update_section_uid(last_section_uid, update_status=False)
            for activity in instance.filter_activities(active_only=True):
                activity.save_answers(answers, takeaway_kit=takeaway_kit)

        # Make sure changes in select_for_update instance are reflected in parent encounter instance so subsequent
        # calls using self object have the correct data.  A potential optimization would be to switch instances, or
        # copy changed fields from one instance to the other.
        self.refresh_from_db()

    def update_section_uid(self, section_uid, update_status=True):
        if self.get_safe_index(section_uid) > self.get_safe_index(self.current_section_uid):
            self.current_section_uid = section_uid
            self.save(update_fields=["current_section_uid", "modified"])

        if update_status:
            for activity in self.assignedactivity_set.all():
                activity.update_status()

    def get_statuses(self) -> List:
        result = []
        for activity in self.filter_activities(active_only=True):
            result.append({
                "type": str(activity.type),
                "status": str(activity.get_status())
            })
        return result

    def get_question_action(self, answer_key: str) -> Optional[dict]:
        return get_question_action(self.get_questions(), answer_key)

    def get_current_section_uid(self) -> Optional[str]:
        current_section_uid = self.current_section_uid
        if current_section_uid is None:
            return None
        return underscore_to_camel(current_section_uid)

    @cached_property
    def sections_dictionary(self):
        return create_section_dictionary(self.get_questions())

    def get_section_uid_for_answer_key(self, answer_key: str) -> Optional[str]:
        section_dict = self.sections_dictionary
        return section_uid_to_answer_key(section_dict, answer_key)

    def get_last_section_uid(self, answers):
        keys = answers.keys()
        highest_section_uid_index = -1
        highest_section_uid = None
        for key in keys:
            section_uid = self.get_section_uid_for_answer_key(key)
            index = self.get_safe_index(section_uid)
            if index > highest_section_uid_index:
                highest_section_uid_index = index
                highest_section_uid = section_uid
        return highest_section_uid
