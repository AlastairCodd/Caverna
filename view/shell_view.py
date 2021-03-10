from random import randrange
from typing import List

from prompt_toolkit import Application, HTML
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import VSplit, HSplit, Window, BufferControl, FormattedTextControl, Layout
from prompt_toolkit.layout.containers import Container

from core.enums.caverna_enums import ResourceTypeEnum

kb: KeyBindings = KeyBindings()


class ShellView(object):
    def __init__(self):
        buffer1: Buffer = Buffer()  # Editable buffer.

        top_host: Container = VSplit([
            # One window that holds the BufferControl with the default buffer on
            # the left.
            Window(content=BufferControl(buffer=buffer1)),

            # A vertical line in the middle. We explicitly specify the width, to
            # make sure that the layout engine will not try to divide the whole
            # width by three for all these windows. The window will simply fill its
            # content by repeating this character.
            Window(width=1, char='ǁ'),

            # Display the text 'Hello world' on the right.
            Window(content=FormattedTextControl(text=HTML('<ansired>Hello world</ansired>'))),
        ])

        resource_names: List[str] = []
        max_length: int = -1

        for resource in ResourceTypeEnum:
            if resource != ResourceTypeEnum.begging_marker:
                max_length = max(len(resource.name), max_length)
                resource_names.append(resource.name)

        resources_horizontal_separator: str = " | "
        resources_header: str = resources_horizontal_separator.join([s.ljust(max_length) for s in resource_names])
        resources_vertical_separator: str = "-|-".join(["-" * max_length for _ in resource_names])
        resources_values: str = resources_horizontal_separator.join([str(randrange(0, 12)).rjust(max_length) for _ in resource_names])

        resources: str = resources_header + "\n" + resources_vertical_separator + "\n" + resources_values

        main_host: Container = HSplit([
            top_host,
            Window(height=1, char='='),
            Window(content=FormattedTextControl(text=resources))
        ])

        layout: Layout = Layout(main_host)

        app: Application = Application(
            key_bindings=kb,
            full_screen=True,
            layout=layout
        )
        app.run()

    @kb.add('c-q')
    def close_event(self) -> None:
        exit()
    # def close_event(self, event) -> None:
    #     event.app.exit()

