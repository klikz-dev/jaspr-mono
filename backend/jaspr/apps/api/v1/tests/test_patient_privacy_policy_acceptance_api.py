
from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)


class TestPatientPrivacyPolicyAccepatancePermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(resource_pattern="patient/accept-privacy-policy", version_prefix="v1")

        self.action_group_map["create"]["allowed_groups"] = ["Patient"]