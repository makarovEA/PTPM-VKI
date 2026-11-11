import unittest
from unittest.mock import Mock, patch

import app as app_module
from calculator import TriangleCalculator, compute_vertices
from controller import Controller
from database import TriangleDatabase
from external import EmailServerStub, ExternalDependency
from user_io import ConsoleUserInteraction, UserInteraction


class TestCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.calc = TriangleCalculator()

    def test_valid_triangle_and_types(self) -> None:
        result = self.calc.calculate("3", "4", "5")
        self.assertEqual(result.triangle_type, "разносторонний")
        self.assertIsNone(result.error_message)
        self.assertEqual(len(result.coords), 3)
        self.assertEqual(
            (result.length1, result.length2, result.length3),
            ("3", "4", "5"),
        )
        self.assertEqual(
            self.calc.calculate("2", "2", "2").triangle_type,
            "равносторонний",
        )
        self.assertEqual(
            self.calc.calculate("2", "2", "3").triangle_type,
            "равнобедренный",
        )

    def test_invalid_and_non_numeric(self) -> None:
        not_triangle = self.calc.calculate("1", "1", "3")
        self.assertEqual(not_triangle.error_message, "не треугольник")
        self.assertEqual(not_triangle.coords, [(-1, -1)] * 3)

        non_numeric = self.calc.calculate("x", "2", "3")
        self.assertEqual(non_numeric.error_message, "НЕЧИСЛОВЫЕ данные")
        self.assertEqual(non_numeric.coords, [(-2, -2)] * 3)

        zero_side = self.calc.calculate("0", "2", "2")
        self.assertEqual(zero_side.error_message, "не треугольник")

    def test_compute_vertices_branches(self) -> None:
        self.assertEqual(len(compute_vertices(3, 4, 5)), 3)
        self.assertEqual(len(compute_vertices(10, 1, 2)), 3)
        self.assertEqual(len(compute_vertices(1, 1, 2)), 3)


class TestDatabase(unittest.TestCase):
    def test_crud(self) -> None:
        db = TriangleDatabase(":memory:")
        try:
            result = TriangleCalculator().calculate("3", "4", "5")
            db.add_record(result)

            loaded = db.get_record("3", "4", "5")
            self.assertIsNotNone(loaded)
            assert loaded is not None
            self.assertEqual(loaded.triangle_type, "разносторонний")
            self.assertEqual(loaded.coords, result.coords)

            self.assertTrue(db.delete_record("3", "4", "5"))
            self.assertIsNone(db.get_record("3", "4", "5"))
            self.assertFalse(db.delete_record("3", "4", "5"))
        finally:
            db.close()


class TestUserIO(unittest.TestCase):
    @patch("builtins.input", side_effect=["3", "4", "5"])
    def test_console_input(self, _mock_input: Mock) -> None:
        ui = ConsoleUserInteraction()
        self.assertEqual(ui.get_triangle_sides(), ("3", "4", "5"))

    @patch("builtins.input", return_value="")
    def test_console_empty_input(self, _mock_input: Mock) -> None:
        ui = ConsoleUserInteraction()
        self.assertIsNone(ui.get_triangle_sides())

    @patch("builtins.input", side_effect=EOFError)
    def test_console_eof(self, _mock_input: Mock) -> None:
        ui = ConsoleUserInteraction()
        self.assertIsNone(ui.get_triangle_sides())


class TestExternal(unittest.TestCase):
    def test_email_server_stub(self) -> None:
        stub = EmailServerStub()
        stub.send_result("ok")
        self.assertEqual(stub.sent_messages, ["ok"])


class TestIntegration(unittest.TestCase):
    def test_controller_computes_saves_and_sends(self) -> None:
        db = TriangleDatabase(":memory:")
        try:
            user = Mock(spec=UserInteraction)
            user.get_triangle_sides.return_value = ("3", "4", "5")
            external = Mock(spec=ExternalDependency)

            controller = Controller(
                calculator=TriangleCalculator(),
                database=db,
                user_io=user,
                external=external,
            )

            result = controller.process_one()

            self.assertIsNotNone(result)
            assert result is not None
            self.assertEqual(result.triangle_type, "разносторонний")
            self.assertIsNotNone(db.get_record("3", "4", "5"))
            external.send_result.assert_called_once()
            self.assertIn("разносторонний", external.send_result.call_args[0][0])
        finally:
            db.close()

    def test_controller_uses_db_cache(self) -> None:
        db = TriangleDatabase(":memory:")
        try:
            user = Mock(spec=UserInteraction)
            user.get_triangle_sides.side_effect = [
                ("3", "4", "5"),
                ("3", "4", "5"),
            ]
            external = Mock(spec=ExternalDependency)

            real_calc = TriangleCalculator()
            calc = Mock()
            calc.calculate = Mock(wraps=real_calc.calculate)

            controller = Controller(
                calculator=calc,
                database=db,
                user_io=user,
                external=external,
            )

            controller.process_one()
            controller.process_one()

            self.assertEqual(calc.calculate.call_count, 1)
            self.assertEqual(external.send_result.call_count, 2)
        finally:
            db.close()

    @patch("builtins.input", side_effect=["3", "4", "5"])
    def test_controller_with_console_input(self, _mock_input: Mock) -> None:
        db = TriangleDatabase(":memory:")
        try:
            external = Mock(spec=ExternalDependency)
            controller = Controller(
                calculator=TriangleCalculator(),
                database=db,
                user_io=ConsoleUserInteraction(),
                external=external,
            )

            result = controller.process_one()

            self.assertIsNotNone(result)
            assert result is not None
            self.assertEqual(result.triangle_type, "разносторонний")
            external.send_result.assert_called_once()
        finally:
            db.close()

    @patch("builtins.input", return_value="")
    def test_controller_empty_input(self, _mock_input: Mock) -> None:
        db = TriangleDatabase(":memory:")
        try:
            external = Mock(spec=ExternalDependency)
            controller = Controller(
                calculator=TriangleCalculator(),
                database=db,
                user_io=ConsoleUserInteraction(),
                external=external,
            )

            self.assertIsNone(controller.process_one())
            external.send_result.assert_not_called()
        finally:
            db.close()

    def test_format_error_branch(self) -> None:
        result = TriangleCalculator().calculate("a", "b", "c")
        text = Controller._format_result(result)
        self.assertIn("НЕЧИСЛОВЫЕ", text)


class TestApp(unittest.TestCase):
    @patch("app.EmailServerStub")
    @patch("app.ConsoleUserInteraction")
    @patch("app.TriangleCalculator")
    @patch("app.Controller")
    @patch("app.TriangleDatabase")
    def test_main_loop(
        self,
        db_cls: Mock,
        controller_cls: Mock,
        _calc_cls: Mock,
        _ui_cls: Mock,
        _external_cls: Mock,
    ) -> None:
        db = db_cls.return_value
        controller = controller_cls.return_value

        valid_result = TriangleCalculator().calculate("3", "4", "5")
        controller.process_one.side_effect = [valid_result, None]

        app_module.main()

        self.assertEqual(controller.process_one.call_count, 2)
        db.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()