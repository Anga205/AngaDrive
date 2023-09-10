import platform, os, requests
import reflex as rx

TPU_path="..\\login.txt" if platform.system()=='Windows' else "../login.txt"

enable_TPU=os.path.exists(TPU_path) 


def login_page_TPU_button(view):
    if (enable_TPU and view=="Desktop"):
        return rx.vstack(
        rx.hstack(
        rx.divider(border_color="GRAY"),
        rx.text("or", font_size="1.65vh"),
        rx.divider(border_color="GRAY"),
        width="100%"
        ),
    rx.button(
        rx.span(
            rx.image(
                src="/TPU-logo.png", 
                height="3vh", 
                width="2.3vh"
            )
        ), 
        rx.span(
            width="2vh"
        ), 
        rx.span(
            "Sign in with TPU", 
            color="WHITE",
        ),
        font_size="1.6vh",
        height="5vh", 
        bg="BLACK",
        width="22vh",
        _hover={"bg":"#1F1F3F"},
        on_click=rx.redirect("https://privateuploader.com/oauth/9f032bfb-7553-4a5d-9727-217f34537f1e")
    ),
    width="100%"
)

    elif enable_TPU and view=="Mobile":
        return rx.vstack(
            rx.box(height="2vh"),
            rx.hstack(
                rx.divider(border_color="GRAY"),
                rx.text("or", font_size="1.65vh"),
                rx.divider(border_color="GREY"),
                width="100%"
            ),
            rx.button(
                rx.span(
                    rx.image(
                        src="/TPU-logo.png",
                        height="3vh",
                        width="2.3vh"
                    ),
                ),
                rx.span(width="2vh"),
                rx.span("Sign in with TPU", color="WHITE"),
                font_size="1.6vh",
                height="5vh", 
                bg="BLACK",
                width="22vh",
                _hover={"bg":"#1F1F3F"},
                on_click=rx.redirect("https://privateuploader.com/oauth/9f032bfb-7553-4a5d-9727-217f34537f1e")
            ),
            width="100%"
        )

    else:
        return rx.box(width="0px", height="0px")

def verifier(token):
    url="https://images.flowinity.com/api/v3/oauth/user"
    params= {
        "Authorization" : token,
        "X-Tpu-App-Id": open(TPU_path, "r").read().split("\n")[1]
    }
    response=requests.get(url, headers=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None


