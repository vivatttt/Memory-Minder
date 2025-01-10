class ConfigError(Exception):
    pass


class UnknownEnviromentError(ConfigError):
    pass


class UnknownUpdateTypeError(Exception):
    pass
