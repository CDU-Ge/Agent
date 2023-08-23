# -*- coding: utf-8 -*-
# Copyright (c) CDU

"""Model Docstrings

"""

from __future__ import absolute_import
from __future__ import annotations
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import json
import pathlib
from typing import overload

log_dir = pathlib.Path(__file__).parent.parent / "logs" / "agent_record"
log_dir.mkdir(exist_ok=True)


@overload
def record(msg: dict) -> str: ...


def record(msg: dict) -> str:
    msg: str = json.dumps(msg, indent=2, ensure_ascii=False)
    _record(msg)
    return msg


def _record(msg: str):
    """"""
    filename = str(datetime.datetime.now().timestamp()).replace(".", "_")
    with open(log_dir / filename, "a", encoding="utf-8") as f:
        f.write(msg)
        f.write("\n")


if __name__ == '__main__':
    print(record({"hahah": "hahah"}))
