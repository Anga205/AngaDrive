import reflex as rx
import website.updating_components as updating_components
from website.State import State


def text_inside_uploader(files):
    def text_widget(text):
         return rx.text(text, font_size="1.65vh", color="WHITE")
    return rx.cond(
        files,
        rx.vstack(
            rx.foreach(
                 files,
                 text_widget
            )
        ),
        rx.text("Drag and drop files or click to select", font_size="1.65vh", color="WHITE"),
    )


def upload_popup_in_dashboard(state_enable_popup_to_upload, state_turn_off_popup_to_upload, upload_handler):
    return rx.alert_dialog(
            rx.alert_dialog_overlay(
                rx.alert_dialog_content(
                    rx.alert_dialog_header("Upload Files", color="BLUE"),
                    rx.alert_dialog_body(
                        rx.upload(
                            rx.vstack(
                                rx.box(height="3.4vh"),
                                text_inside_uploader(rx.selected_files),
                                rx.box(height="3.4vh"),
                                spacing="0px"
                            ),
                            border=("1px dotted #ffffff"),
                        ),
                        color="WHITE",
                    ),
                    rx.alert_dialog_footer(
                        rx.hstack(
                            rx.cond(
                                rx.selected_files,
                                rx.button(
                                    "Upload",
                                    color="BLACK",
                                    on_click=lambda: upload_handler(rx.upload_files()),
                                ),
                                rx.box()
                            ),
                            rx.button(
                                "Close",    
                                color="WHITE",
                                on_click=state_turn_off_popup_to_upload,
                                bg="RED",
                            )
                        )
                    ),
                    bg="#111112"
                ),
            ),
            is_open=state_enable_popup_to_upload,
        )



def dashboard_file_hosted_widget(State,file_object):
    file_size, timestamp, new_file_name, link=file_object[3], file_object[2], file_object[0], file_object[-1]
    return rx.vstack(
        rx.span(
            file_object[4],
            color="WHITE",
            font_size="2vh"
        ),
        rx.divider(border_color="GRAY"),
        rx.hstack(
            rx.vstack(
                rx.text("File Size: "),
                rx.text("Upload Date: "),
                rx.text("File Link: "),
                font_size="1.65vh",
                color="WHITE",
                spacing="0.3vh",
                align_items="flex-end"
            ),
            rx.vstack(
                rx.text(file_size),
                rx.text(timestamp),
                rx.tooltip(
                    rx.text(new_file_name, on_click=rx.set_clipboard(link)),
                    label="click to copy"
                ),
                spacing="0.3vh",
                align_items="flex-start",
                color="WHITE",
                font_size="1.65vh"
            ),
        ),
        rx.hstack(
            rx.spacer(),
            rx.button(
                rx.icon(tag="delete", color='RED'),
                bg="#301b19",
                font_size="1.65vh",
                border_radius="1.5vh",
                height="3vh",
                on_click=State.delete_file(file_object[0])
            ),
            rx.spacer(),
            rx.button(
                rx.icon(tag="copy", color="#009688"),
                bg="#132523",
                height="3vh",
                border_radius="1.5vh",
                on_click=rx.set_clipboard(link),
                font_size="1.65vh"
            ),
            rx.spacer()
        ),
        border_width="0.5vh",
        border_color="#0a0a0a",
        border_radius="1vh",
        spacing="0px",
        bg="#0a0a0a"
    )

def file_hosting_page(State, bool_files_associated_with_account, state_enable_popup_to_upload, state_turn_off_popup_to_upload, state_turn_on_popup_to_upload, upload_handler):
    return rx.vstack(
        rx.box(height="2vh"),
        rx.hstack(
            rx.box(width="5%"),
            rx.heading(
                "My files",
                color="WHITE",
                font_size="4vh"
                ),
            rx.spacer(),
            rx.box(
                rx.button(
                    "Upload",
                    rx.box(width="10%"),
                    rx.image(src="/upload.png",height="4vh"),
                    on_click=state_turn_on_popup_to_upload,
                    bg="BLUE",
                    color="WHITE",
                    height="5vh",
                    font_size="1.65vh",
                    border_radius="1vh",
                    width="13vh"
                ),
                upload_popup_in_dashboard(state_enable_popup_to_upload, state_turn_off_popup_to_upload, upload_handler),
            ),
            rx.box(width="5%"),
            width="100%",
            spacing="0px"
        ),
        rx.box(height="3vh"),
        rx.cond(
            bool_files_associated_with_account,
            rx.wrap(
                rx.foreach(
                    State.file_data_list_associated_with_account,
                    lambda file_obj: dashboard_file_hosted_widget(State, file_obj)
                )
            ),
            rx.text("You have not uploaded anything yet, click 'upload' to start hosting files on drive.anga.pro!", color="WHITE"),
        ),
        width="100%",
        spacing="1vh"
    )

def support_card(title, *components):
    return rx.vstack(
        rx.heading(
            title,
            font_size="3.5vh",
            color="white",
            ),
        rx.divider(
            border_color="GRAY"
        ),
        *components,
        border_radius="2vh",
        bg="#10112b",
        border_color="#10112b",
        border_width="1vh",
        width="35vh",
        spacing="1vh"
    )

def support_page(State):
    return rx.vstack(
        rx.heading(
            "You can get support from the following platforms:",
            font_size="3vh",
            color="WHITE"
        ),
        rx.hstack(
            rx.spacer(),
            rx.wrap(
                support_card(
                    "Discord",
                    rx.box(
                        element="iframe",
                        src="https://discordapp.com/widget?id=760062846423269416&theme=dark",
                        width="100%",
                        height="40vh"
                    ),
                ),
                support_card(
                    "Instagram",
                    rx.link(
                        rx.image(
                            src="/instagram_qr.png",
                            height="auto",
                            width="auto",
                            border_radius="1vh"
                        ),
                        href="https://instagram.com/_anga205"
                    )
                ),
                support_card(
                    "𝕏 (formerly twitter)",
                    rx.vstack(
                        rx.vstack(
                            rx.spacer(),
                            rx.hstack(
                                rx.heading("𝕏", font_size="7vh", color="WHITE"),
                                rx.spacer(),
                                rx.text("custom profile iframe", font_size="1.65vh", color="WHITE"),
                                spacing="0px",
                                width="85%"
                            ),
                            rx.spacer(),
                            bg="BLACK",
                            spacing="0px",
                            height="8vh",
                            width="100%",
                            border_radius="1vh 1vh 0vh 0vh"
                        ),
                        rx.hstack(
                            rx.image(src="https://pbs.twimg.com/profile_images/1113432700126322688/4jSs4ljT_400x400.png", height="auto", width="8vh", border_radius="4vh"),
                            rx.spacer(),
                            rx.heading("@_anga205", _as="b", font_size="1.65vh"),
                            spacing="0vh",
                            width="85%"
                        ),
                        rx.divider(border_radius="GRAY"),
                        rx.text("idk what to put here", font_size="1vh"),
                        rx.spacer(),
                        rx.button("Follow me on 𝕏",bg="BLACK", font_size="2.5vh", height="3.5vh", width="90%", color="WHITE", _hover={"color":"BLACK", "bg":"WHITE"}),
                        rx.box(height="0vh", width="0px"),
                        spacing="1vh",
                        width="100%",
                        height="100%",
                        bg="WHITE",
                        border_radius="1.5vh 1.5vh 1vh 1vh",
                        on_click=rx.redirect("https://twitter.com/_anga205/")
                    )
                ),
                support_card(
                    "GitHub",
                    rx.vstack(
                        rx.spacer(),
                        rx.heading("This website doesnt provide an inbuilt social media widget that i can embed so im working on a custom card to put here :/",font_size="2vh",width="85%"),
                        rx.spacer(),
                        width="100%",
                        height="100%",
                        bg="WHITE",
                        border_radius="1vh",
                    )
                ),
                support_card(
                    "Threads",
                    rx.vstack(
                        rx.spacer(),
                        rx.heading("This website doesnt provide an inbuilt social media widget that i can embed so im working on a custom card to put here :/",font_size="2vh",width="85%"),
                        rx.spacer(),
                        width="100%",
                        height="100%",
                        bg="WHITE",
                        border_radius="1vh",
                    )
                ),
                support_card(
                    "Email",
                    rx.vstack(
                        rx.spacer(),
                        rx.heading("This website doesnt provide an inbuilt social media widget that i can embed so im working on a custom card to put here :/",font_size="2vh",width="85%"),
                        rx.spacer(),
                        width="100%",
                        height="100%",
                        bg="WHITE",
                        border_radius="1vh",
                    )
                ),
                support_card(
                    "Telegram",
                    rx.vstack(
                        rx.spacer(),
                        rx.heading("This website doesnt provide an inbuilt social media widget that i can embed so im working on a custom card to put here :/",font_size="2vh",width="85%"),
                        rx.spacer(),
                        width="100%",
                        height="100%",
                        bg="WHITE",
                        border_radius="1vh",
                    )
                ),
                support_card(
                    "Live Chat",
                    rx.vstack(
                        rx.spacer(),
                        rx.heading("Chat with me in this website itself without logging into any social media, This is a work in progress :)",font_size="2vh",width="85%"),
                        rx.spacer(),
                        width="100%",
                        height="100%",
                        bg="WHITE",
                        border_radius="1vh",
                    )
                ),
#                align_items="baseline",
                width="85%"
            ),
            rx.spacer(),
            width="100%"
        ),
        spacing="1vh"
    )




def password_manager():
    return rx.vstack(
        rx.accordion(
            rx.accordion_item(
                rx.accordion_button(
                    rx.spacer(),
                    rx.heading(
                        "Change password", 
                        font_size = "2vh"
                        ),
                    rx.accordion_icon(),
                    rx.spacer()
                ),
                rx.accordion_panel(
                    rx.vstack(
                        rx.password(
                            placeholder="Enter current password", 
                            on_blur=State.set_reset_password_auth_password
                            ),
                        rx.password(
                            placeholder="Enter new password", 
                            on_blur=State.set_reset_password_new_password
                            ),
                        rx.password(
                            placeholder="Retype new password", 
                            on_blur=State.set_reset_password_new_password_retyped
                            ),
                        rx.hstack(
                            rx.spacer(),
                            rx.button(
                                "Change password",
                                is_disabled=State.disable_reset_button,
                                on_click=State.change_password_button_clicked
                                ),
                            rx.spacer(),
                            width="100%"
                        ),
                        spacing="0.5vh"
                    )
                )
            ),
            allow_toggle=True,
            width="100%"
        ),
        width="90%",
        bg="gray",
        spacing="0vh",
        border_radius="1vh",
        border_color="gray",
        border_width="1vh"
    )


def account_manager():
    return rx.vstack(
        rx.heading("Manage account", font_size="4vh", color="WHITE"),
        rx.divider(border_color="WHITE"),
        updating_components.add_TPU_to_account_widget(State.TPU_verified),
        password_manager(),
        border_radius="2vh",
        bg="#0F0F10",
        spacing="0.5vh",
        width="100%",
        border_color="#0F0F10",
        border_width="1vh"
    )