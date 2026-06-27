import winreg


def get_installed_apps():
    apps = []

    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    for path in registry_paths:
        try:
            reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
        except:
            continue

        for i in range(0, winreg.QueryInfoKey(reg)[0]):
            try:
                subkey_name = winreg.EnumKey(reg, i)
                subkey_path = path + "\\" + subkey_name
                subkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path)

                name = None
                version = None

                try:
                    name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                except:
                    pass

                try:
                    version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                except:
                    version = "Unknown"

                if name:
                    apps.append((name, version))

            except:
                continue

    return apps