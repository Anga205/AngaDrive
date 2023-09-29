import os, website.library, reflex as rx
website.library.create_sqlite_database(os.path.join(os.getcwd(),"..","rx.db"))
class WebsiteConfig(rx.Config):
    pass

config = WebsiteConfig(
    app_name="website",
#    api_url="https://testapi.anga.pro",
    env=rx.Env.DEV,
)
