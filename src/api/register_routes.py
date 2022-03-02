def register_routes(app):
    from src.api.person import PersonApi
    from src.api.match import MatchApi

    PersonApi.register(app)
    MatchApi.register(app)
