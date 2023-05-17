from typing import Any, Optional, Union

from typing_extensions import Literal

from .. import globals, outbox


def notify(message: Any, *,
           position: Literal['top-left', 'top-right', 'bottom-left', 'bottom-right', 'top', 'bottom', 'left', 'right', 'center'] = 'bottom',
           close_button: Union[bool, str] = False,
           type: Optional[Literal['positive', 'negative', 'warning', 'info', 'ongoing']] = None,
           color: Optional[str] = None,
           multi_line: Optional[bool] = False,
           **_kwargs,
           ) -> None:
    """Notification

    Displays a notification on the screen.

    :param message: content of the notification
    :param position: position on the screen ("top-left", "top-right", "bottom-left", "bottom-right", "top", "bottom", "left", "right" or "center", default: "bottom")
    :param close_button: optional label of a button to dismiss the notification (default: `False`)
    :param type: optional type ("positive", "negative", "warning", "info" or "ongoing")
    :param color: optional color name
    :param multi_line: optional boolean to enable multi-line notifications

    Note: You can pass additional keyword arguments according to `Quasar's Notify API <https://quasar.dev/quasar-plugins/notify#notify-api>`_.
    """
    _arg_map = {'close_button': 'closeBtn',
                'multi_line':   'multiLine',
                }
    options = {_arg_map.get(key, key): value
               for key, value
               in locals().items()
               if not key.startswith('_') and value is not None
               }
    options['message'] = str(message)
    options.update(_kwargs)
    outbox.enqueue_message('notify', options, globals.get_client().id)
