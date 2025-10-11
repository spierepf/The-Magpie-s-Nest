import unittest
from unittest.mock import Mock

from sequencer import Sequencer, MINUTE


class SequencerTestCase(unittest.TestCase):
    def test_sequencer_calls_task_when_invoked_after_time_elapsed(self):
        clock = Mock(return_value=0)
        sequencer = Sequencer(clock)

        task = Mock()
        sequencer.after(10 * MINUTE, task)

        clock.return_value = 10 * MINUTE
        sequencer()
        task.assert_called()

    def test_sequencer_does_not_call_task_before_time_elapsed(self):
        clock = Mock(return_value=0)
        sequencer = Sequencer(clock)

        task = Mock()
        sequencer.after(10 * MINUTE, task)

        clock.return_value = (10 * MINUTE) - 1
        sequencer()
        task.assert_not_called()

    def test_sequencer_calls_elapsed_tasks_but_not_pending_ones(self):
        clock = Mock(return_value=0)
        sequencer = Sequencer(clock)

        task1 = Mock()
        sequencer.after(10 * MINUTE, task1)

        task2 = Mock()
        sequencer.after(12 * MINUTE, task2)

        clock.return_value = (11 * MINUTE)
        sequencer()
        task1.assert_called()
        task2.assert_not_called()

    def test_the_order_in_which_tasks_are_added_is_irrelevant(self):
        clock = Mock(return_value=0)
        sequencer = Sequencer(clock)

        task2 = Mock()
        sequencer.after(12 * MINUTE, task2)

        task1 = Mock(
        sequencer.after(10 * MINUTE, task1)

        clock.return_value = (11 * MINUTE)
        sequencer()
        task1.assert_called()
        task2.assert_not_called()

    def test_tasks_should_only_be_called_once(self):
        clock = Mock(return_value=0)
        sequencer = Sequencer(clock)

        task = Mock()
        sequencer.after(10 * MINUTE, task)

        clock.return_value = 10 * MINUTE
        sequencer()

        clock.return_value = 10 * MINUTE + 1
        sequencer()

        task.assert_called_once()


if __name__ == '__main__':
    unittest.main()
