import unittest

from src.app import app


DEFAULT_HEADERS = {"Content-Type": "application/json"}


class BaseTest(unittest.TestCase):

    def set_up_table(self, TableCls, read_capacity=1, write_capacity=1, wait=True):
        if TableCls.exists():
            TableCls.delete_table()
            TableCls.create_table(read_capacity_units=read_capacity, write_capacity_units=write_capacity, wait=wait)
        else:
            TableCls.create_table(read_capacity_units=read_capacity, write_capacity_units=write_capacity, wait=wait)

    def delete_table(self, TableCls):
        TableCls.delete_table()

    def _setup_app(self):
        self.app = app.test_client()


class BaseApiTest(BaseTest):

    def setUp(self):
        self._setup_app()

    def get_request_as_json(self, uri, expected_response=200):
        response = self.app.get('/api/' + uri)
        assert response.status_code == expected_response
        return response.json

    def post_request_as_json(self, uri, body, headers=None, expected_response=201,
                             return_as_json=True):
        post_response = self.app.post(
            '/api/' + uri,
            headers=DEFAULT_HEADERS if headers is None else headers,
            data=body
        )
        assert post_response.status_code == expected_response
        return post_response.json if return_as_json else post_response