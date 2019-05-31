import fangler
import unittest

# NOTE: Using double quotes throughout this test file due to JSON requirements
# TODO: Refactor with test variables separated from the post requests (clean up)

class BatchTestDefang(unittest.TestCase):
    defang_test_domains = {"https://www.twitter.com": "hxxps:$$www[dot]twitter[dot]com",
                           "http://www.twitter.com": "hxxp:$$www[dot]twitter[dot]com",
                           "ftp://www.twitter.com": "fxp:$$www[dot]twitter[dot]com",
                           "https://www.twitter.com/demo/url": "hxxps:$$www[dot]twitter[dot]com$demo$url",
                           "https://www.twitter.com": "hxxps:$$www[dot]twitter[dot]com"}

    def setUp(self):
        fangler.app.testing = True
        self.app = fangler.app.test_client()

    def test_defang_batch(self):
        for domain in BatchTestDefang.defang_test_domains:
            result = self.app.post("/api/defang",
                                   json={"data": domain},
                                   headers={"Content-Type": "application/json"})
            assert result.status == "200 OK"
            self.assertEqual(
                BatchTestDefang.defang_test_domains.get(domain),
                result.json['response']
            )


class TestDefang(unittest.TestCase):
    def setUp(self):
        fangler.app.testing = True
        self.app = fangler.app.test_client()

    def test_defang_single(self):
        result = self.app.post("/api/defang",
                               json={"data": "https://www.twitter.com"},
                               headers={"Content-Type": "application/json"})
        assert result.status == "200 OK"
        self.assertEqual(
            "hxxps:$$www[dot]twitter[dot]com",
            result.json['response']
        )

    def test_defang_single_no_protocol(self):
        result = self.app.post("/api/defang",
                               json={"data": "www.twitter.com"},
                               headers={"Content-Type": "application/json"})
        assert result.status == "400 BAD REQUEST"

    def test_defang_single_weird_protocol(self):
        result = self.app.post("/api/defang",
                               json={"data": "sppppp://www.twitter.com"},
                               headers={"Content-Type": "application/json"})
        assert result.status == "400 BAD REQUEST"

    def test_defang_list(self):
        result = self.app.post("/api/defang",
                               json={"data": ["https://www.twitter.com", "ftp://www.google.com"]},
                               headers={"Content-Type": "application/json"})
        assert result.status == "200 OK"
        self.assertEqual(
            b'{\"response\": [\"hxxps:$$www[dot]twitter[dot]com\", \"fxp:$$www[dot]google[dot]com\"]}\n',
            result.data
        )

    def test_defang_list_bad_entry(self):
        result = self.app.post("/api/defang",
                               json={"data": ["https://www.twitter.com", "sppppp://www.twitter.com"]},
                               headers={"Content-Type": "application/json"})
        assert result.status == "400 BAD REQUEST"



class TestRefang(unittest.TestCase):
    def setUp(self):
        fangler.app.testing = True
        self.app = fangler.app.test_client()

    def test_refang_single(self):
        result = self.app.post("/api/refang",
                               json={"data": "hxxps:$$www[dot]twitter[dot]com"},
                               headers={"Content-Type": "application/json"})
        assert result.status == "200 OK"
        self.assertEqual(
            b"{\"response\": \"https://www.twitter.com\"}\n",
            result.data
        )

    def test_defang_single_no_protocol(self):
        result = self.app.post("/api/refang",
                               json={"data": "www[dot]twitter[dot]com"},
                               headers={"Content-Type": "application/json"})
        assert result.status == "400 BAD REQUEST"

    def test_defang_single_weird_protocol(self):
        result = self.app.post("/api/refang",
                               json={"data": "sppppp://www.twitter.com"},
                               headers={"Content-Type": "application/json"})
        assert result.status == "400 BAD REQUEST"

    def test_refang_list(self):
        result = self.app.post("/api/refang",
                               json={"data": ["hxxps:$$www[dot]twitter[dot]com", "sfxp:$$www[dot]google[dot]com"]},
                               headers={"Content-Type": "application/json"})
        assert result.status == "200 OK"
        self.assertEqual(
            b"{\"response\": [\"https://www.twitter.com\", \"sftp://www.google.com\"]}\n",
            result.data
        )

    def test_refang_list_bad_entry(self):
        result = self.app.post("/api/refang",
                               json={"data": ["hxxps:$$www[dot]twitter[dot]com", "sppppp:$$www[dot]twitter[dot]com"]},
                               headers={"Content-Type": "application/json"})
        assert result.status == "400 BAD REQUEST"



if __name__ == "__main__":
    unittest.main()
