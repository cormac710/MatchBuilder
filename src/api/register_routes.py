def register_routes(app):
    from src.api.player import PlayerApi
    from src.api.match import MatchApi

    PlayerApi.register(app)
    MatchApi.register(app)
