from copy import deepcopy
from jaspr.apps.test_infrastructure.testcases import JasprTestCase


class TestClinicLocationModel(JasprTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.system = cls.create_healthcare_system(name="Test Clinic")

    def test_ip_addresses_and_ranges_whitelist_save_behavior(self):
        clinic = self.create_clinic(
            system=self.system,
            name="IP Test Clinic",
            ip_addresses_whitelist=[
                "192.192.192.195",
                "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
                "192.192.192.195",
                "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
            ],
            ip_address_ranges_whitelist=[
                "192.168.100.0/22",
                "2002:db8::/34",
                "192.168.100.0/22",
                "2002:db8::/34",
            ],
        )

        self.assertEqual(len(clinic.ip_addresses_whitelist), 2)
        self.assertEqual(len(clinic.ip_address_ranges_whitelist), 2)
        self.assertEqual(
            [*map(str, clinic.ip_addresses_whitelist)],
            [
                "192.192.192.195/32",
                "2001:db8:85a3::8a2e:370:7334/128",
            ],
        )
        self.assertEqual(
            [*map(str, clinic.ip_address_ranges_whitelist)],
            [
                "192.168.100.0/22",
                "2002:db8::/34",
            ],
        )

        # Do the same thing again, this time with the now native python IP
        # address/range values instead of strings. Make sure it still behaves as
        # intended.
        clinic.ip_addresses_whitelist.extend(
            deepcopy(clinic.ip_addresses_whitelist)
        )
        clinic.ip_address_ranges_whitelist.extend(
            deepcopy(clinic.ip_address_ranges_whitelist)
        )
        clinic.save()

        self.assertEqual(len(clinic.ip_addresses_whitelist), 2)
        self.assertEqual(len(clinic.ip_address_ranges_whitelist), 2)
        self.assertEqual(
            [*map(str, clinic.ip_addresses_whitelist)],
            [
                "192.192.192.195/32",
                "2001:db8:85a3::8a2e:370:7334/128",
            ],
        )
        self.assertEqual(
            [*map(str, clinic.ip_address_ranges_whitelist)],
            [
                "192.168.100.0/22",
                "2002:db8::/34",
            ],
        )

    def test_has_ip_whitelisting(self):
        clinic = self.create_clinic(system=self.system)
        self.assertEqual(clinic.ip_addresses_whitelist, [], "Pre-condition")
        self.assertEqual(
            clinic.ip_address_ranges_whitelist, [], "Pre-condition"
        )

        self.assertFalse(clinic.has_ip_whitelisting)

        clinic.ip_addresses_whitelist.append("192.192.192.195/32")
        self.assertTrue(clinic.has_ip_whitelisting)

        clinic.ip_addresses_whitelist = []
        clinic.ip_address_ranges_whitelist.append("192.168.100.0/22")
        self.assertTrue(clinic.has_ip_whitelisting)

        clinic.ip_addresses_whitelist.append("192.192.192.195/32")
        self.assertTrue(clinic.has_ip_whitelisting)

    def test_ip_satisfies_whitelisting_if_no_whitelisting_rules(self):
        clinic = self.create_clinic(system=self.system)
        self.assertEqual(clinic.ip_addresses_whitelist, [], "Pre-condition")
        self.assertEqual(
            clinic.ip_address_ranges_whitelist, [], "Pre-condition"
        )

        self.assertTrue(clinic.ip_satisfies_whitelisting("127.0.0.1"))

    def test_ip_satisfies_whitelisting_with_ipv4_or_ipv6(self):
        clinic = self.create_clinic(
            system=self.system,
            name="IP Test Clinic",
            ip_addresses_whitelist=[
                "192.192.192.195",
                "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
            ],
            ip_address_ranges_whitelist=[
                "192.168.100.0/22",
                "2002:db8::/34",
            ],
        )

        # Test IPV4 matched address.
        self.assertTrue(clinic.ip_satisfies_whitelisting("192.192.192.195"))
        # Test IPV6 matched address.
        self.assertTrue(
            clinic.ip_satisfies_whitelisting(
                "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
            )
        )
        # Test IPV4 in range.
        self.assertTrue(clinic.ip_satisfies_whitelisting("192.168.100.111"))
        # Test IPV6 in range.
        self.assertTrue(
            clinic.ip_satisfies_whitelisting(
                "2002:0db8:0000:0000:0000:8a2e:0370:7331"
            )
        )

        # Test unsatisfied IPV4 (close but not exact with an exact address).
        self.assertFalse(clinic.ip_satisfies_whitelisting("192.192.192.196"))
        # Test unsatisfied IPV6 (close but not exact with an exact address).
        self.assertFalse(
            clinic.ip_satisfies_whitelisting(
                "2001:0db8:85a3:0000:0000:8a2e:0370:7333"
            )
        )
        # Test unsatisfied IPV4 (close (string relatively speaking) but not in a range).
        self.assertFalse(clinic.ip_satisfies_whitelisting("192.167.100.0"))
        # Test unsatisfied IPV6 (close (string relatively speaking) but not in a range).
        self.assertFalse(
            clinic.ip_satisfies_whitelisting(
                "2002:0db7:85a3:0000:0000:8a2e:0370:7331"
            )
        )


