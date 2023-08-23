import reflex as rx
import platform

class WebsiteConfig(rx.Config):
    pass


if platform.system()=='Windows':
    api="https://testapi.anga.pro"
else:
    api="https://api.anga.pro"

config = WebsiteConfig(
    app_name="website",
    api_url=api,
    env=rx.Env.DEV,
)
