import reflex as rx

class WebsiteConfig(rx.Config):
    pass

config = WebsiteConfig(
    app_name="website",
#    api_url="https://api.anga.pro",
    env=rx.Env.DEV,
)