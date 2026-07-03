"""RouteRegistry — singleton tracking named routes. Mirrors NodeAdmin's namedRoutes.ts."""


class RouteRegistry:
    _instance = None
    _routes: dict = {}
    _path_method_map: dict = {}

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register(self, name: str, method: str, path_pattern: str):
        guard = 'api' if name.startswith('api.') else 'web'
        key = f'{name}:{method.upper()}'
        entry = {
            'name': name,
            'method': method.upper(),
            'path': path_pattern,
            'guard': guard,
        }
        self._routes[key] = entry
        self._path_method_map[(method.upper(), path_pattern)] = name

    def get_all(self) -> list:
        return list(self._routes.values())

    def get_name_by_path_method(self, method: str, path: str) -> str | None:
        return self._path_method_map.get((method.upper(), path))

    def clear(self):
        self._routes.clear()
        self._path_method_map.clear()


route_registry = RouteRegistry.instance()
