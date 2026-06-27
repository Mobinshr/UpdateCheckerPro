from packaging.version import Version

def is_update_available(installed, latest):
    try:
        return Version(latest) > Version(installed)
    except Exception:
        return False