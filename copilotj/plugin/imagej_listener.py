# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from typing import override

from copilotj.plugin._base import Request, Response, Verbosity

__all__ = ["HistoryResponse", "GetOperationHistoryRequest"]

TIME_FMT = "%H:%M:%S"
DATETIME_FMT = f"%Y-%m-%d {TIME_FMT}"


class _LogMessage(Response):
    message: str
    timestamp_earliest: datetime
    timestamp_latest: datetime | None
    count: int

    @override
    def _describe(self, *, level: int, verbosity: Verbosity) -> list[str]:
        if self.count > 1:
            t1 = self.timestamp_earliest.strftime(DATETIME_FMT)
            if self.timestamp_latest is not None:
                fmt = TIME_FMT if self.timestamp_earliest.date() == self.timestamp_latest.date() else DATETIME_FMT
                t2 = self.timestamp_latest.strftime(fmt)
                return [f"{t1} ~ {t2}: {self.message} (x{self.count})"]
            else:
                return [f"{t1}: {self.message} (x{self.count})"]
        else:
            t = self.timestamp_earliest.strftime(DATETIME_FMT)
            return [f"{t}: {self.message}"]


TIP_HISTORY_RESPONSE = """\
All operations are shown in the history. However, some of messages may be overflowed due to the capacity of history \
queue of ImageJ plugin.\
"""


class HistoryResponse(Response):
    messages: list[_LogMessage]
    is_complete: bool
    since: datetime
    until: datetime | None  # TODO: we need to implement this, including request

    @override
    def _describe(self, *, level: int, verbosity: Verbosity) -> list[str]:
        heading = "#" * level

        lines = []
        lines.append(f"{heading} Operation History")

        seconds = (datetime.now() - self.since).total_seconds()
        if seconds < 60:
            t = f"{seconds:.0f} seconds ago"
        elif seconds < 3600:
            t = f"{(seconds // 60):.0f} minutes {(seconds % 60):.0f} seconds ago"
        else:
            t = "long time ago"

        if len(self.messages) == 0:
            summary = f"There have been no operations recorded since {t}"
            lines.append(summary)
            return lines

        summary = f"There are {len(self.messages)} operations history since {t}"
        lines.append(summary)

        if self.is_complete:
            lines.append(TIP_HISTORY_RESPONSE)

        for log_message in self.messages:
            lines.extend("- " + line for line in log_message._describe(level=level + 1, verbosity=verbosity))

        return lines[-20:]


class GetOperationHistoryRequest(
    Request[HistoryResponse], event="get_operation_history", response_type=HistoryResponse
):
    since: datetime
