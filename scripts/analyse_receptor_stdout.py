#!/usr/bin/env python
# Script to analyze an Ansible receptor stdout file, by default in the current
# directory detecting all hosts never returning from a started task.
# If TASK_UUID is defined, the validation is limited to this specific task.
# Usage: analyse_receptor_stdout.py [/var/lib/awx/receptor/.../stdout] [task-uuid]
# VERSION: v2026-03-11-09

import json
import os
import sys

# input parameters, a bit crude but it works
STDOUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "stdout"
TASK_UUID = sys.argv[2] if len(sys.argv) > 2 else None

# start and stop events
RUNNER_START = {"runner_on_start"}
RUNNER_STOP = {
    "runner_on_ok",
    "runner_on_failed",
    "runner_on_skipped",
    "runner_on_unreachable",
}


def del_runner(started_dict, stopped_key):
    """Remove a stopped runner from dictionary of started ones"""
    if stopped_key in started_dict:
        del started_dict[stopped_key]
    else:
        print(f"WARNING: '{stopped_key}' was never started", file=sys.stderr)


def get_lingering_runners(stdout_file, task_uuid=None):
    """Return a dictionary of tasks started but not finished"""
    runners_started = {}
    with open(stdout_file, "r", encoding="utf-8", errors="replace") as stdout_fp:
        for line_num, line in enumerate(stdout_fp, 1):
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                print(f"WARNING: skipping malformed JSON on line {line_num}", file=sys.stderr)
                continue

            if "event" not in event:
                continue

            event_data = event.get("event_data")
            if not event_data:
                continue

            host = event_data.get("host")
            event_task_uuid = event_data.get("task_uuid")
            if not host or not event_task_uuid:
                continue

            if task_uuid and event_task_uuid != task_uuid:
                continue

            if event["event"] in RUNNER_START:
                key = host if task_uuid else f"{host}/{event_task_uuid}"
                runners_started[key] = event
            elif event["event"] in RUNNER_STOP:
                key = host if task_uuid else f"{host}/{event_task_uuid}"
                del_runner(runners_started, key)

    return runners_started


if __name__ == "__main__":
    if not os.path.isfile(STDOUT_FILE):
        print(f"Error: File '{STDOUT_FILE}' doesn't exist or isn't a regular file", file=sys.stderr)
        sys.exit(1)
    if not os.access(STDOUT_FILE, os.R_OK):
        print(f"Error: File '{STDOUT_FILE}' is not readable", file=sys.stderr)
        sys.exit(1)
    runners_lingering = get_lingering_runners(STDOUT_FILE, TASK_UUID)
    print(json.dumps(runners_lingering, indent=2))
    print("==>", len(runners_lingering.keys()), "lingering task(s) found")
