import logging
from asyncio import Task
from typing import TYPE_CHECKING

from core.workers.abstract import RabbitWorkerType
from core.workers.error import ErrorResultWorker
from core.workers.success import SuccessResultWorker
from yt_shared.utils.tasks.tasks import create_task

if TYPE_CHECKING:
    from core.bot import VideoBot


class RabbitWorkerManager:
    _TASK_TYPES = (ErrorResultWorker, SuccessResultWorker)

    def __init__(self, bot: 'VideoBot') -> None:
        self._log = logging.getLogger(self.__class__.__name__)
        self._bot = bot
        self._workers: dict[RabbitWorkerType, Task] = {}

    async def start_workers(self) -> None:
        """Start background result workers.

        Workers watch RabbitMQ queues and dispatch payload to the appropriate handlers.
        """
        for task_cls in self._TASK_TYPES:
            self._log.info('Starting %s', task_cls.__name__)
            self._workers[task_cls.TYPE] = create_task(
                task_cls(self._bot).run(),
                task_name=task_cls.__name__,
                logger=self._log,
                exception_message='RabbitMQ worker %s raised an exception',
                exception_message_args=(task_cls.__name__,),
            )

    def stop_workers(self) -> None:
        self._log.info('Stopping %d RabbitMQ workers', len(self._workers))
        for worker_type, worker_task in self._workers.items():
            self._log.info('Stopping %s RabbitMQ worker', worker_type.value)
            worker_task.cancel()
