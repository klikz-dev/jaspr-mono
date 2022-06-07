from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.urls import reverse


# NOTE: Thanks to https://stackoverflow.com/a/59363986 Initially used in commit after
# `892b2aa709e2c50b64af1b90e091347cdc77700a` to make the `QuestionListQuestion` inline
# in `QuestionList` have `raw_id_fields = ("question",)` without adding an extra
# database query for every inline. It does remove the extra label, which we don't need
# anyway though (with the other fields we're showing). Also, see
# https://code.djangoproject.com/ticket/29294 for the closed ticket.
# Latest NOTE: At the time of writing (right after
# `e83961f45f64ef67207a61643b8734dd367fe761`) (11/18/20), we aren't using this.
# However, going to keep it here for now because it worked for its use case before, and
# could be useful for any time we have inlines that we want `raw_id_fields` set on
# where we have more than, say, 5-10 inlines on average. Significantly speeds up and
# helps querying, etc. especially once past a few dozen inlines since it's linear query
# complexity.
class OptimizedForeignKeyRawIdWidget(ForeignKeyRawIdWidget):
    def label_and_url_for_value(self, value):
        try:
            url = reverse(
                "%s:%s_%s_change"
                % (
                    self.admin_site.name,
                    self.rel.model._meta.app_label,
                    self.rel.model._meta.object_name.lower(),
                ),
                args=(value,),
            )
        except NoReverseMatch:
            url = ""  # Admin not registered for target model.
        return str(value), url
