from datascience_cookiecutter import Cookiecutter, CookiecutterSettings


if __name__ == "__main__":
    print("Running test.py")
    settings = CookiecutterSettings(name="cookietest", path=".", git=True)
    cc = Cookiecutter(settings)
    cc()