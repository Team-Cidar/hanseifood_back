class Singleton(type):  # metaclass
    _instance = {}

    # Override
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(Singleton, cls).__call__(*args, *kwargs)
        return cls._instance[cls]
