from loguru import logger
from pytest import main
from enum import StrEnum


class TestsStatuses(StrEnum):
    """Enum class for tests statuses"""
    FAILED = "failed"
    PASSED = "passed"
    SKIPPED = "skipped"


def run_tests(mark: str = "all"):
    """Function for call tests with using marks"""
    tests: list[dict[str, str]] = []

    class TestResultPlugin:
        """Test plugin for collect test logs"""

        @staticmethod
        def pytest_runtest_logreport(report):
            """Pytest log report hook"""

            status = TestsStatuses.FAILED if report.failed else \
                TestsStatuses.PASSED if report.passed else TestsStatuses.SKIPPED

            if status == TestsStatuses.FAILED:
                logger.debug(f"Test: {report.nodeid} failed.")

            tests.append({
                "test": report.nodeid,
                "status": status
            })

    logger.debug(f"Run tests with mark {mark}.")

    main([r"-v"] + ["-m", mark] if mark != "all" else [], plugins=[TestResultPlugin])

    return tests
