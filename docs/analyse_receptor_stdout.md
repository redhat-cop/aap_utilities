# Analyse receptor stdout

## Introduction

The script `analyse_receptor_stdout.py` can be used to detect on which tasks and which hosts a playbook/job might be stuck.

Assume that you have a playbook with thousands of hosts, and potentially `free` strategy.
It becomes very difficult to identify which host is stuck on which task from the information available in the AAP WebUI.

Luckily, assuming you have access to the OS of the responsible execution host, you can find this information, with the help of the script.

## Instructions

1. Connect to the execution host as the user with which AAP has been installed.
  We'll assume you're in its home directory and have copied there the script `analyse_receptor_stdout.py`.
1. Call `journalctl -f -t automation-controller-task` and identify the journal entry with the `task_id` equal to the job ID in the UI, and containing a non-null `work_unit_id`, something like (`aap26.example.com` being your execution node`):

    `Feb 25 08:29:24 aap26.example.com automation-controller-task[2247]: 2026-02-25 08:29:24,085 INFO     [3502db8631534ed9aaf66b31c345ee15] awx.analytics.job_lifecycle job-26 work unit id assigned {"type": "job", "task_id": 26, "state": "work_unit_id_assigned", "work_unit_id": "aap26examplecomNklO1HBi", "task_name": "jt_skip_sleep"}`

1. You can then call the script with `./analyse_receptor_stdout.py ./.local/share/containers/storage/volumes/receptor_data/_data/aap26.example.com/aap26examplecomNklO1HBi/stdout`.
It will show you one JSON object per task/host lingering, i.e. where the task started but never ended.
This output is followed by a summary of the number of tasks/hosts impacted like `==> 2 lingering task(s) found`.
1. If there are too many of those, you can limit the output to a specific task by calling the script again with its UUID, as in `./analyse_receptor_stdout.py .../stdout 8ed877b6-e959-9042-525a-000000000007`.
1. Once the culprit host and task are identified, it becomes more easily possible to troubleshoot the reason, e.g. on the host itself.

## Notes

1. even if the above instructions are made for AAP 2.6 containerized, the script works similarly since AAP 2.4 as RPM, just with different users and paths (`sudo find / -name stdout 2>/dev/null` can do miracles there).
1. Receptor's stdout file disappears once the job is finished, so don't forget to save it if you want to analyse it later (or have your customer attach it to a ticket).
The analysis of the saved `stdout` file can be done on any computer.

## Example

When `27` is the job ID, and `localhost1` the identified culprit host:

```console
$ journalctl -f -t automation-controller-task
[...]
Feb 25 08:58:13 aap26.example.com automation-controller-task[2247]: 2026-02-25 08:58:13,178 INFO     [a3c673a9f7544d7da3684682d38f1c8d] awx.analytics.job_lifecycle job-27 work unit id assigned {"type": "job", "task_id": 27, "state": "work_unit_id_assigned", "work_unit_id": "aap26examplecomcdaQPr3R", "task_name": "jt_skip_sleep"}

$ ./analyse_receptor_stdout.py ./.local/share/containers/storage/volumes/receptor_data/_data/aap26.example.com/aap26examplecomcdaQPr3R/stdout
{
  "localhost1/4a6d4f97-0cbc-0ba3-16a6-000000000005": {
    "uuid": "e1e7ec9d-94ab-4f83-9f75-429572e75e6e",
    "counter": 5,
    "stdout": "",
    "start_line": 5,
    "end_line": 5,
    "runner_ident": "27",
    "event": "runner_on_start",
    "job_id": 27,
    "pid": 19,
    "created": "2026-02-25T08:58:15.154488+00:00",
    "parent_uuid": "4a6d4f97-0cbc-0ba3-16a6-000000000005",
    "event_data": {
      "playbook": "pb_skip_sleep.yml",
      "playbook_uuid": "823260e5-e598-477d-8f3b-7d95879f9360",
      "play": "skip or not some sleeping tasks",
      "play_uuid": "4a6d4f97-0cbc-0ba3-16a6-000000000003",
      "play_pattern": "all",
      "task": "sleep 60 seconds unless asked to skip",
      "task_uuid": "4a6d4f97-0cbc-0ba3-16a6-000000000005",
      "task_action": "ansible.builtin.command",
      "resolved_action": "ansible.builtin.command",
      "task_args": "",
      "task_path": "/runner/project/pb_skip_sleep.yml:10",
      "host": "localhost1",
      "uuid": "e1e7ec9d-94ab-4f83-9f75-429572e75e6e"
    }
  }
}
==> 1 lingering task(s) found
```
