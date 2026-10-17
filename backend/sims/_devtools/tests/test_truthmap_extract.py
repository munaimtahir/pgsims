from django.test import SimpleTestCase

from sims._devtools import truthmap_extract


class TruthMapExtractTests(SimpleTestCase):
    def test_permissions_and_endpoint_extraction(self):
        class PublicView:
            pass

        self.assertEqual(truthmap_extract.get_permissions(PublicView), [])
        endpoints = truthmap_extract.extract_endpoints()
        self.assertTrue(endpoints)
        self.assertTrue(all("path" in endpoint for endpoint in endpoints))
