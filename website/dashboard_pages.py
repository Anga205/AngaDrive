import reflex as rx


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



def dashboard_file_hosted_widget(file_name="Fetching...", file_size="Fetching...", timestamp="Fetching...", link="Fetching..."):
    return rx.vstack(
        rx.span(
            "Head.txt",
            color="WHITE",
            font_size="2vh"
        ),
        rx.divider(border_color="GRAY"),
        rx.hstack(
            rx.vstack(
                rx.text("File Size: "),
                rx.text("Upload Date: "),
                rx.text("File Link: "),
                color="WHITE",
                spacing="0.3vh"
            ),
            rx.vstack(
                rx.text(file_size),
                rx.text(timestamp),
                rx.tooltip(
                    rx.text(link, on_click=rx.set_clipboard(link)),
                    label="click to copy"
                )
                spacing="0.3vh",
                color="WHITE"
            ),
        ),
        border_width="0.5vh",
        border_color="#0a0a0a",
        border_radius="1vh",
        spacing="0px",
        bg="#0a0a0a"
    )



def file_hosting_page(state_enable_popup_to_upload, state_turn_off_popup_to_upload, state_turn_on_popup_to_upload, upload_handler):
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
        dashboard_file_hosted_widget(),
        width="100%",
        spacing="1vh"
    )