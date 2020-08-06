class PySettings(object):

    def __init__(self, path):
        self.settings_path = path

    def __call__(self, env):
        self.SETTINGS_ENV = env
        self.manager = SettingsManager(env, self.settings_path, self)
        return self.manager

    def get(self, key):
        return getattr(self, key)

    def __getattr__(self, item):
        if not self.SETTINGS_ENV:
            raise EnvironmentError(
                'You are not within the PySettings context. Please use it as a context manager'
                'or as a decorator'
            )


class SettingsManager(object):
    """This should support context manager + decorator interfaces"""

    def __init__(self, env, settings_path, settings_instance):
        self.env = env
        self.settings_path = settings_path[0] if isinstance(settings_path, (list, tuple)) else settings_path
        self.settings_instance = settings_instance
        self.settings_module = None
        self.settings_vars_dict = {}

    def _recursive_import(self, path, env):
        if not path:
            ValueError(f'Settings path cannot be an empty value. {path} given')
        chunks = path.split('/')
        index_from_right = -1
        while abs(index_from_right) <= len(chunks):
            subpath = '.'.join(chunks[index_from_right:])
            try:
                self.settings_module = __import__(f'{subpath}.{env}', fromlist=env)
                self.settings_vars_dict = self.settings_module.__dict__
                return
            except ModuleNotFoundError:
                index_from_right -= 1
        raise ImportError(f'Could not import any relative settings package from {path}')

    def settings_on(self, vars_dict):
        for k, v in vars_dict.items():
            setattr(self.settings_instance, k, v)

    def settings_off(self, vars_dict):
        for k, v in vars_dict.items():
            self.settings_instance.__dict__.pop(k)

    def __enter__(self):
        self._recursive_import(self.settings_path, self.env)
        self.settings_on(self.settings_vars_dict)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.settings_instance.SETTINGS_ENV = None
        self.settings_off(self.settings_vars_dict)
