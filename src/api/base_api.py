from flask.views import MethodView


class BaseApi(MethodView):
    api = '/api/'

    @classmethod
    def register(cls, app):
        raise NotImplementedError('please implement BaseApi.register()')
