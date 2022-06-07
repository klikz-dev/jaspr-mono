from typing import List
from simple_history.utils import bulk_create_with_history, bulk_update_with_history

from django.apps import apps
from jaspr.apps.kiosk.constants import COPING_STRATEGY_CATEGORY_SLUG_MAP
from jaspr.apps.kiosk.models import CopingStrategy, CopingStrategyCategory

def get_patient_filtered_coping_strategies(instance):
    app_label = instance._meta.app_label
    PatientCopingStrategy = apps.get_model(app_label, 'PatientCopingStrategy')
    if app_label == 'jah':
        return PatientCopingStrategy.objects.filter(
            jah_account=instance.jah_account,
        ).all()
    elif app_label == 'kiosk':
        return PatientCopingStrategy.objects.filter(
            encounter=instance.assignedactivity.encounter,
        ).all()
    raise Exception(f"Patient Coping Strategies do not exist for app {app_label}")

def get_patient_user(instance):
    app_label = instance._meta.app_label
    if app_label == 'jah':
        return instance.jah_account.patient.user
    elif app_label == 'kiosk':
        return instance.assignedactivity.encounter.patient.user
    raise Exception(f"Patient Coping Strategies do not exist for app {app_label}")

def create_patient_coping_strategy(instance, title, category_id):
    app_label = instance._meta.app_label
    PatientCopingStrategy = apps.get_model(app_label, 'PatientCopingStrategy')
    if app_label == 'jah':
        return PatientCopingStrategy(
            title=title,
            category_id=category_id,
            jah_account = instance.jah_account,
        )
    elif app_label == 'kiosk':
        return PatientCopingStrategy(
            title=title,
            category_id=category_id,
            encounter=instance.assignedactivity.encounter,
        )
    raise Exception(f"Patient Coping Strategies do not exist for app {app_label}")


def all_coping_strategy_categories() -> List[CopingStrategyCategory]:
    return list(CopingStrategyCategory.objects.filter(status="active"))

def get_category_id_by_slug(slug: str) -> int:
    """
    Match category by slug and return id.
    """

    for category in all_coping_strategy_categories():
        if slug == category.slug:
            break
    else:
        category = None

    assert (
        category
    ), f"No matching Coping Strategy Category found for Category Slug: {slug}"

    return category.id


def update_coping_fields(old_instance, instance):
    PatientCopingStrategy = apps.get_model(instance._meta.app_label, 'PatientCopingStrategy')
    changed_coping_fields = [
        f.name
        for f in instance.coping_fields
        if getattr(instance, f.name) != getattr(old_instance, f.name)
    ]

    if changed_coping_fields:

        # filtering titles based on the changed_coping_fields
        changed_strategies_dict = {
            key: value
            for (key, value) in COPING_STRATEGY_CATEGORY_SLUG_MAP.items()
            if key in changed_coping_fields
        }

        category_slugs = list(changed_strategies_dict.values())

        changed_titles = list(
            CopingStrategy.objects.filter(
                category__slug__in=category_slugs
            ).values_list("title", flat=True)
        )

        # create list of titles of patient coping strategies within this category
        # This list will include both archived and active items.
        changed_patient_titles = list(
            get_patient_filtered_coping_strategies(instance).filter(
                category__slug__in=category_slugs,
            ).values_list("title", flat=True)
        )

        # make a list of archived patient coping strategy titles also within this category
        archived_patient_titles = list(
            get_patient_filtered_coping_strategies(instance).filter(
                status="archived",
                category__slug__in=category_slugs,
            ).values_list("title", flat=True)
        )

        # iterate through slug map looking for strategies that
        # 1) don't have a matching CopingStrategy Record and haven't been custom created yet
        # 2) are already created and present in PatientCopingStrategy table
        # When found, append to appropriate list.
        new_patient_strategies = []
        already_created_active_patient_strategy_titles = []
        already_created_archived_patient_strategy_titles = []
        for field_name, slug in changed_strategies_dict.items():
            category_id = get_category_id_by_slug(slug)
            field_name_titles = getattr(instance, field_name, []) or []

            for title in field_name_titles:
                if title not in changed_titles and title not in changed_patient_titles:
                    new_patient_strategies.append(
                        create_patient_coping_strategy(
                            instance,
                            title=title,
                            category_id=category_id,
                        )
                    )
                elif title in archived_patient_titles:
                    already_created_archived_patient_strategy_titles.append(title)

                elif title in changed_patient_titles:
                    already_created_active_patient_strategy_titles.append(title)

        # Mark this patient's unused PatientCopingStrategy records as archived.
        no_longer_used_strategies = list(
            get_patient_filtered_coping_strategies(instance).filter(
                title__in=changed_patient_titles,
                status="active",
            ).exclude(title__in=already_created_active_patient_strategy_titles)
        )
        for old_strategy in no_longer_used_strategies:
            old_strategy.status = "archived"
        bulk_update_with_history(
            no_longer_used_strategies,
            PatientCopingStrategy,
            ["status"],
            batch_size=500,
            default_user=get_patient_user(instance),
        )

        # Mark this patient's newly restored, previously_archived PatientCopingStrategy records as active.
        newly_restored_strategies = list(
            get_patient_filtered_coping_strategies(instance).filter(
                title__in=already_created_archived_patient_strategy_titles,
                status="archived",
            )
        )
        for newly_restored_strategy in newly_restored_strategies:
            newly_restored_strategy.status = "active"
        bulk_update_with_history(
            newly_restored_strategies,
            PatientCopingStrategy,
            ["status"],
            batch_size=500,
            default_user=get_patient_user(instance),
        )

        # bulk create our new items.
        bulk_create_with_history(
            new_patient_strategies,
            PatientCopingStrategy,
            batch_size=500,
            default_user=get_patient_user(instance),
        )
