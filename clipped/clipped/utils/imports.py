from typing import Dict


class ImportStringCache(dict):
    def __missing__(self, key):
        if "." not in key:
            return __import__(key)

        module_name, class_name = key.rsplit(".", 1)

        module = __import__(module_name, {}, {}, [class_name])
        handler = getattr(module, class_name)

        # We cache a NoneType for missing imports to avoid repeated lookups
        self[key] = handler

        return handler


_cache = ImportStringCache()


def import_string(path: str):
    """
    Path must be module.path.ClassName

    >>> cls = import_string('module_x.ClassY')
    """
    result = _cache[path]
    return result


def import_submodules(context: Dict, root_module: str, path: str):
    """
    Import all submodules and register them in the ``context`` namespace.

    >>> import_submodules(locals(), __name__, __path__)
    """
    import pkgutil

    for _, module_name, _ in pkgutil.walk_packages(path, root_module + "."):
        # this causes a Runtime error with model conflicts
        # module = loader.find_module(module_name).load_module(module_name)
        module = __import__(module_name, globals(), locals(), ["__name__"])
        for k, v in vars(module).items():
            if not k.startswith("_"):
                context[k] = v
        context[module_name] = module
