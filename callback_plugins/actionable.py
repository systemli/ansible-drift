# (c) 2012-2014, Michael DeHaan <michael.dehaan@gmail.com>
# (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    name: actionable
    type: stdout
    short_description: actionable Ansible screen output
    version_added: historical
    description:
        - This is the actionable output callback for ansible-playbook.
    extends_documentation_fragment:
      - default_callback
      - result_format_callback
    requirements:
      - set as stdout in configuration
'''


from ansible import constants as C
from ansible import context
from ansible.playbook.task_include import TaskInclude
from ansible.plugins.callback import CallbackBase
from ansible.utils.color import colorize, hostcolor
from ansible.utils.fqcn import add_internal_fqcns


class CallbackModule(CallbackBase):

    '''
    This is the actionable callback interface, which simply prints actionable
    messages to stdout when new callback events are received.
    '''

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'actionable'

    def __init__(self):

        self._play = None
        self._last_task_banner = None
        self._last_task_name = None
        self._task_type_cache = {}
        super(CallbackModule, self).__init__()

    def v2_runner_on_failed(self, result, ignore_errors=False):

        host_label = self.host_label(result)
        self._clean_results(result._result, result._task.action)

        if self._last_task_banner != result._task._uuid:
            self._print_task_banner(result._task)

        self._handle_exception(result._result, use_stderr=self.get_option('display_failed_stderr'))
        self._handle_warnings(result._result)

        if result._task.loop and 'results' in result._result:
            self._process_items(result)

        else:
            if self._display.verbosity < 2 and self.get_option('show_task_path_on_failure'):
                self._print_task_path(result._task)
            msg = "fatal: [%s]: FAILED! => %s" % (host_label, self._dump_results(result._result))
            self._display.display(msg, color=C.COLOR_ERROR, stderr=self.get_option('display_failed_stderr'))

        if ignore_errors:
            self._display.display("...ignoring", color=C.COLOR_SKIP)

    def v2_runner_on_ok(self, result):

        host_label = self.host_label(result)

        if result._result.get('changed', False):
            if self._last_task_banner != result._task._uuid:
                self._print_task_banner(result._task)

            msg = "changed: [%s]" % (host_label,)
            color = C.COLOR_CHANGED

        else:
            if not self.get_option('display_ok_hosts'):
                return

            if self._last_task_banner != result._task._uuid:
                self._print_task_banner(result._task)

            msg = "ok: [%s]" % (host_label,)
            color = C.COLOR_OK

        self._handle_warnings(result._result)

        if result._task.loop and 'results' in result._result:
            self._process_items(result)
        else:
            self._clean_results(result._result, result._task.action)

            if self._run_is_verbose(result):
                msg += " => %s" % (self._dump_results(result._result),)
            self._display.display(msg, color=color)

    def v2_runner_on_skipped(self, result):
        pass

    def v2_runner_on_unreachable(self, result):
        if self._last_task_banner != result._task._uuid:
            self._print_task_banner(result._task)

        host_label = self.host_label(result)
        msg = "fatal: [%s]: UNREACHABLE! => %s" % (host_label, self._dump_results(result._result))
        self._display.display(msg, color=C.COLOR_UNREACHABLE, stderr=self.get_option('display_failed_stderr'))

        if result._task.ignore_unreachable:
            self._display.display("...ignoring", color=C.COLOR_SKIP)

    def v2_playbook_on_no_hosts_matched(self):
        pass

    def v2_playbook_on_no_hosts_remaining(self):
        pass

    def v2_playbook_on_task_start(self, task, is_conditional):
        pass

    def _task_start(self, task, prefix=None):
        # Cache output prefix for task if provided
        # This is needed to properly display 'RUNNING HANDLER' and similar
        # when hiding skipped/ok task results
        if prefix is not None:
            self._task_type_cache[task._uuid] = prefix

        self._last_task_name = task.get_name().strip()

        # Display the task banner immediately if we're not doing any filtering based on task result
        if self.get_option('display_skipped_hosts') and self.get_option('display_ok_hosts'):
            self._print_task_banner(task)

    def _print_task_banner(self, task):
        # args can be specified as no_log in several places: in the task or in
        # the argument spec.  We can check whether the task is no_log but the
        # argument spec can't be because that is only run on the target
        # machine and we haven't run it thereyet at this time.
        #
        # So we give people a config option to affect display of the args so
        # that they can secure this if they feel that their stdout is insecure
        # (shoulder surfing, logging stdout straight to a file, etc).
        args = ''
        if not task.no_log and C.DISPLAY_ARGS_TO_STDOUT:
            args = u', '.join(u'%s=%s' % a for a in task.args.items())
            args = u' %s' % args

        prefix = self._task_type_cache.get(task._uuid, 'TASK')

        # Use cached task name
        task_name = self._last_task_name
        if task_name is None:
            task_name = task.get_name().strip()

        checkmsg = ""

        self._display.banner(u"%s [%s%s]%s" % (prefix, task_name, args, checkmsg))

        self._last_task_banner = task._uuid

    def v2_playbook_on_cleanup_task_start(self, task):
        pass

    def v2_playbook_on_handler_task_start(self, task):
        pass

    def v2_runner_on_start(self, host, task):
        pass

    def v2_playbook_on_play_start(self, play):
        pass

    def v2_on_file_diff(self, result):
        if result._task.loop and 'results' in result._result:
            for res in result._result['results']:
                if 'diff' in res and res['diff'] and res.get('changed', False):
                    diff = self._get_diff(res['diff'])
                    if diff:
                        if self._last_task_banner != result._task._uuid:
                            self._print_task_banner(result._task)
                        self._display.display(diff)
        elif 'diff' in result._result and result._result['diff'] and result._result.get('changed', False):
            diff = self._get_diff(result._result['diff'])
            if diff:
                if self._last_task_banner != result._task._uuid:
                    self._print_task_banner(result._task)
                self._display.display(diff)

    def v2_runner_item_on_ok(self, result):

        host_label = self.host_label(result)
        if isinstance(result._task, TaskInclude):
            return
        elif result._result.get('changed', False):
            if self._last_task_banner != result._task._uuid:
                self._print_task_banner(result._task)

            msg = 'changed'
            color = C.COLOR_CHANGED
        else:
            if not self.get_option('display_ok_hosts'):
                return

            if self._last_task_banner != result._task._uuid:
                self._print_task_banner(result._task)

            msg = 'ok'
            color = C.COLOR_OK

        msg = "%s: [%s] => (item=%s)" % (msg, host_label, self._get_item_label(result._result))
        self._clean_results(result._result, result._task.action)
        self._display.display(msg, color=color)

    def v2_runner_item_on_failed(self, result):
        if self._last_task_banner != result._task._uuid:
            self._print_task_banner(result._task)

        host_label = self.host_label(result)
        self._clean_results(result._result, result._task.action)
        self._handle_exception(result._result, use_stderr=self.get_option('display_failed_stderr'))

        msg = "failed: [%s]" % (host_label,)
        self._handle_warnings(result._result)
        self._display.display(
            msg + " (item=%s) => %s" % (self._get_item_label(result._result), self._dump_results(result._result)),
            color=C.COLOR_ERROR,
            stderr=self.get_option('display_failed_stderr')
        )

    def v2_runner_item_on_skipped(self, result):
        pass

    def v2_playbook_on_include(self, included_file):
        pass

    def v2_playbook_on_stats(self, stats):
        pass

    def v2_playbook_on_start(self, playbook):
        pass

    def v2_runner_retry(self, result):
        task_name = result.task_name or result._task
        host_label = self.host_label(result)
        msg = "FAILED - RETRYING: [%s]: %s (%d retries left)." % (host_label, task_name, result._result['retries'] - result._result['attempts'])
        if self._run_is_verbose(result, verbosity=2):
            msg += "Result was: %s" % self._dump_results(result._result)
        self._display.display(msg, color=C.COLOR_DEBUG)

    def v2_runner_on_async_poll(self, result):
        pass

    def v2_runner_on_async_ok(self, result):
        pass

    def v2_runner_on_async_failed(self, result):
        host = result._host.get_name()

        # Attempt to get the async job ID. If the job does not finish before the
        # async timeout value, the ID may be within the unparsed 'async_result' dict.
        jid = result._result.get('ansible_job_id')
        if not jid and 'async_result' in result._result:
            jid = result._result['async_result'].get('ansible_job_id')
        self._display.display("ASYNC FAILED on %s: jid=%s" % (host, jid), color=C.COLOR_DEBUG)

    def v2_playbook_on_notify(self, handler, host):
        pass
