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
    if task_uuid:  # we only check this specific task
        with open(stdout_file, "r") as stdout_fp:
            for line in stdout_fp:
                event = json.loads(line)
                if (
                    "event" in event
                    and event["event"] in RUNNER_START
                    and event["event_data"]["task_uuid"] == task_uuid
                ):
                    runners_started[event["event_data"]["host"]] = event
                elif (
                    "event" in event
                    and event["event"] in RUNNER_STOP
                    and event["event_data"]["task_uuid"] == task_uuid
                ):
                    del_runner(runners_started, event["event_data"]["host"])
    else:  # we check all tasks
        with open(stdout_file, "r") as stdout_fp:
            for line in stdout_fp:
                event = json.loads(line)
                if "event" in event and event["event"] in RUNNER_START:
                    key = (
                        event["event_data"]["host"]
                        + "/"
                        + event["event_data"]["task_uuid"]
                    )
                    runners_started[key] = event
                elif "event" in event and event["event"] in RUNNER_STOP:
                    key = (
                        event["event_data"]["host"]
                        + "/"
                        + event["event_data"]["task_uuid"]
                    )
                    del_runner(runners_started, key)
    return runners_started


if __name__ == "__main__":
    if not os.path.isfile(STDOUT_FILE):
        sys.exit(f"File '{STDOUT_FILE}' doesn't exist or isn't readable")
    runners_lingering = get_lingering_runners(STDOUT_FILE, TASK_UUID)
    # print the remaining events without finishing one...
    print(json.dumps(runners_lingering, indent=2))
    print("==>", len(runners_lingering.keys()), "lingering task(s) found")
