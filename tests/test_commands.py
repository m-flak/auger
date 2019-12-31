import io
import pytest

from auger.commands import CommandStack, Command

class BufferWriteCmd(Command):
    def operation(self):
        self.old_data = self.target.getvalue()
        self.target.write(self.data)

    def reverse_operation(self):
        self.target.seek(0, io.SEEK_SET)
        self.target.truncate()
        self.target.write(self.old_data)

@pytest.fixture
def command_and_buffer(request):
    buffer = io.StringIO()
    cmd = BufferWriteCmd(target=buffer, data='TEST')

    request.addfinalizer(lambda b=buffer: b.close())
    return buffer, cmd

class TestCommandStack:
    def test_stack_compare(self):
        fake_cmd1 = Command()
        fake_cmd2 = Command()
        fake_cmd3 = Command()
        fake_cmd4 = Command()
        fake_cmd5 = Command()
        fake_cmd6 = Command()

        stack_1 = CommandStack()
        stack_2 = CommandStack()

        assert stack_1 == stack_2
        assert stack_1 is not stack_2

        stack_1.push(fake_cmd1)
        stack_2.push(fake_cmd2)
        stack_1.push(fake_cmd3)
        stack_2.push(fake_cmd4)
        stack_1.push(fake_cmd5)
        stack_2.push(fake_cmd6)

        assert stack_1 != stack_2
        assert len(stack_1) == len(stack_2)

    def test_stack_pushpop(self):
        fake_cmd1 = Command()
        fake_cmd2 = Command()

        stack_1 = CommandStack()
        stack_2 = CommandStack()

        stack_1.push(fake_cmd1)
        stack_2.push(fake_cmd2)

        pop_1 = stack_1.pop()
        pop_2 = stack_2.pop()

        assert pop_1 is fake_cmd1
        assert pop_2 is fake_cmd2

        stack_1.push(pop_1)
        stack_1.push(pop_2)

        pop_3 = stack_1.pop()
        pop_4 = stack_1.pop()

        assert pop_3 is pop_2
        assert pop_4 is pop_1

    def test_stack_length(self):
        fake_cmd1 = Command()
        fake_cmd2 = Command()
        fake_cmd3 = Command()

        stack_1 = CommandStack()

        stack_1.push(fake_cmd1)
        stack_1.push(fake_cmd2)
        stack_1.push(fake_cmd3)

        assert len(stack_1) == 3

        stack_1.pop()
        stack_1.pop()
        stack_1.pop()

        assert len(stack_1) == 0

class TestCommand:
    def test_command_implementation(self, command_and_buffer):
        the_buffer = command_and_buffer[0]
        the_command = command_and_buffer[1]

        the_command.operation()
        assert the_buffer.getvalue() == the_command.data

        the_command.reverse_operation()
        assert not the_buffer.getvalue()
        assert the_buffer.getvalue() == the_command.old_data

class TestCommandManager:
    def test_command_undo_redo(self, qapp, command_and_buffer):
        the_buffer = command_and_buffer[0]
        the_command = command_and_buffer[1]

        manager = qapp.cmd_mgr
        manager.execute_new_command(the_command)
        assert the_buffer.getvalue() == the_command.data

        manager.undo_last_command()
        assert not the_buffer.getvalue()
        assert the_buffer.getvalue() == the_command.old_data

        manager.redo_last_command()
        assert the_buffer.getvalue() == the_command.data

        # let's try to do this crap thirteen times
        for i in range(0, 13):
            manager.undo_last_command()
            manager.redo_last_command()
