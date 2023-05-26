from dataclasses import dataclass
from typing import Any, Callable, Dict, List

from typing_extensions import Self

from .. import background_tasks, globals
from ..dependencies import register_component
from ..element import Element
from ..helpers import KWONLY_SLOTS, is_coroutine

register_component('refreshable', __file__, 'refreshable.js')


@dataclass(**KWONLY_SLOTS)
class RefreshableTarget:
    container: Element
    instance: Any
    args: List[Any]
    kwargs: Dict[str, Any]

    def run(self, func: Callable[..., Any]) -> None:
        if is_coroutine(func):
            async def wait_for_result() -> None:
                with self.container:
                    if self.instance is None:
                        await func(*self.args, **self.kwargs)
                    else:
                        await func(self.instance, *self.args, **self.kwargs)
            return wait_for_result()
        else:
            with self.container:
                if self.instance is None:
                    func(*self.args, **self.kwargs)
                else:
                    func(self.instance, *self.args, **self.kwargs)


class refreshable:

    def __init__(self, func: Callable[..., Any]) -> None:
        """Refreshable UI functions

        The `@ui.refreshable` decorator allows you to create functions that have a `refresh` method.
        This method will automatically delete all elements created by the function and recreate them.
        """
        self.func = func
        self.instance = None
        self.targets: List[RefreshableTarget] = []

    def __get__(self, instance, _) -> Self:
        self.instance = instance
        return self

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        self.prune()
        target = RefreshableTarget(container=Element('refreshable'), instance=self.instance, args=args, kwargs=kwargs)
        self.targets.append(target)
        target.run(self.func)

    def refresh(self) -> None:
        self.prune()
        for target in self.targets:
            if target.instance != self.instance:
                continue
            target.container.clear()
            result = target.run(self.func)
            if is_coroutine(self.func):
                if globals.loop and globals.loop.is_running():
                    background_tasks.create(result)
                else:
                    globals.app.on_startup(result)

    def prune(self) -> None:
        self.targets = [target for target in self.targets if target.container.client.id in globals.clients]
