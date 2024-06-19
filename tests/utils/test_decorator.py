import logging

from ragnarok.utils.decorator import timer_func, a_timer_func

logger = logging.getLogger(__name__)


def test_timer_func(capsys):
    """
    Test case for timer_func decorator.
    """

    @timer_func
    def example_function():
        pass

    example_function()
    captured = capsys.readouterr()
    assert "executed in" in captured.out


def test_a_timer_func(capsys):
    """
    Test case for a_timer_func decorator.
    """
    import asyncio

    async def example_async_function():
        await asyncio.sleep(0)

    @a_timer_func
    async def example_async():
        await example_async_function()

    asyncio.run(example_async())
    captured = capsys.readouterr()
    assert "executed in" in captured.out
