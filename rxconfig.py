import website.library, reflex as rx
website.library.create_sqlite_database(website.library.database_directory)
class WebsiteConfig(rx.Config):
    pass

config = WebsiteConfig(
    app_name="website",
    api_url="https://testapi.anga.pro",
    env=rx.Env.DEV,
)
