"""
IoT Smart Office — ConfigurationManager (Singleton Pattern)

Only ONE instance exists for the entire application runtime. All parts of the
system share the same configuration without explicitly passing the object around.
"""


class ConfigurationManager:
    """Singleton: guarantees exactly one instance."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._settings = {
                "system_name": "IoT Smart Office",
                "version": "1.0",
                "log_events": True,
            }
        return cls._instance

    def get(self, key, default=None):
        return self._settings.get(key, default)

    def set(self, key, value):
        self._settings[key] = value

    def show(self):
        print("\n  ⚙  Configuration Manager (Singleton)")
        for k, v in self._settings.items():
            print(f"     {k}: {v}")
