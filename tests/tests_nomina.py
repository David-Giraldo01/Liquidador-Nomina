import unittest

from src.model import logica_nomina
from src.model.datos_nomina import DatosNomina
from src.model.errores import (
    ErrorDescuentosNegativos,
    ErrorDiasInvalidos,
    ErrorSalarioNegativo,
)


class TestsNomina(unittest.TestCase):

    def test_normal_1(self) -> None:
        # 3.000.000 + 261.000 de auxilio = 3.261.000
        # Menos 8% de salud y pensión (260.880) = 3.000.120
        neto_esperado: float = 3000120
        datos = DatosNomina(3000000, 30, 0, 0, 0)
        neto_calculado: float = logica_nomina.calcular_nomina(datos)
        self.assertAlmostEqual(neto_esperado, neto_calculado, 2)

    def test_normal_2(self) -> None:
        # El total devengado coincide con el caso anterior: 3.261.000
        neto_esperado: float = 3000120
        datos = DatosNomina(2500000, 30, 200000, 300000, 0)
        neto_calculado: float = logica_nomina.calcular_nomina(datos)
        self.assertAlmostEqual(neto_esperado, neto_calculado, 2)

    def test_normal_3(self) -> None:
        neto_esperado: float = 4040000
        datos = DatosNomina(4000000, 30, 500000, 0, 100000)
        neto_calculado: float = logica_nomina.calcular_nomina(datos)
        self.assertAlmostEqual(neto_esperado, neto_calculado, 2)

    def test_extraordinario_1(self) -> None:
        neto_esperado: float = 73600000
        datos = DatosNomina(80000000, 30, 0, 0, 0)
        neto_calculado: float = logica_nomina.calcular_nomina(datos)
        self.assertAlmostEqual(neto_esperado, neto_calculado, 2)

    def test_extraordinario_2(self) -> None:
        # 1.500.000 proporcional + 261.000 de auxilio = 1.761.000
        neto_esperado: float = 1620120
        datos = DatosNomina(3000000, 15, 0, 0, 0)
        neto_calculado: float = logica_nomina.calcular_nomina(datos)
        self.assertAlmostEqual(neto_esperado, neto_calculado, 2)

    def test_extraordinario_3(self) -> None:
        # 3.000.000 + 5.000.000 + 261.000 = 8.261.000
        neto_esperado: float = 7600120
        datos = DatosNomina(3000000, 30, 0, 5000000, 0)
        neto_calculado: float = logica_nomina.calcular_nomina(datos)
        self.assertAlmostEqual(neto_esperado, neto_calculado, 2)

    def test_auxilio_salario_2_000_000(self) -> None:
        detalle = logica_nomina.calcular_detalle(
            DatosNomina(2000000, 30, 0, 0, 0)
        )
        self.assertEqual(detalle.auxilio_transporte, 261000)
        self.assertTrue(detalle.aplica_auxilio_transporte)
        self.assertAlmostEqual(detalle.total_devengado, 2261000, 2)

    def test_auxilio_salario_3_000_000(self) -> None:
        detalle = logica_nomina.calcular_detalle(
            DatosNomina(3000000, 30, 0, 0, 0)
        )
        self.assertEqual(detalle.auxilio_transporte, 261000)
        self.assertAlmostEqual(detalle.total_devengado, 3261000, 2)

    def test_auxilio_salario_3_499_999(self) -> None:
        detalle = logica_nomina.calcular_detalle(
            DatosNomina(3499999, 30, 0, 0, 0)
        )
        self.assertEqual(detalle.auxilio_transporte, 261000)
        self.assertAlmostEqual(detalle.total_devengado, 3760999, 2)

    def test_sin_auxilio_salario_3_500_000(self) -> None:
        detalle = logica_nomina.calcular_detalle(
            DatosNomina(3500000, 30, 0, 0, 0)
        )
        self.assertEqual(detalle.auxilio_transporte, 0)
        self.assertFalse(detalle.aplica_auxilio_transporte)
        self.assertAlmostEqual(detalle.total_devengado, 3500000, 2)

    def test_sin_auxilio_salario_4_000_000(self) -> None:
        detalle = logica_nomina.calcular_detalle(
            DatosNomina(4000000, 30, 0, 0, 0)
        )
        self.assertEqual(detalle.auxilio_transporte, 0)
        self.assertFalse(detalle.aplica_auxilio_transporte)
        self.assertAlmostEqual(detalle.total_devengado, 4000000, 2)

    def test_auxilio_no_se_duplica(self) -> None:
        detalle = logica_nomina.calcular_detalle(
            DatosNomina(2000000, 30, 100000, 50000, 0)
        )
        self.assertEqual(detalle.auxilio_transporte, 261000)
        self.assertAlmostEqual(
            detalle.total_devengado,
            2000000 + 100000 + 50000 + 261000,
            2,
        )

    def test_error_dias_mayores_a_30(self) -> None:
        datos = DatosNomina(3000000, 31, 0, 0, 0)
        with self.assertRaises(ErrorDiasInvalidos):
            logica_nomina.calcular_nomina(datos)

    def test_error_salario_negativo(self) -> None:
        datos = DatosNomina(-3000000, 30, 0, 0, 0)
        with self.assertRaises(ErrorSalarioNegativo):
            logica_nomina.calcular_nomina(datos)

    def test_error_dias_negativos(self) -> None:
        datos = DatosNomina(3000000, -1, 0, 0, 0)
        with self.assertRaises(ErrorDiasInvalidos):
            logica_nomina.calcular_nomina(datos)

    def test_error_descuentos_negativos(self) -> None:
        datos = DatosNomina(3000000, 30, 0, 0, -100000)
        with self.assertRaises(ErrorDescuentosNegativos):
            logica_nomina.calcular_nomina(datos)


if __name__ == "__main__":
    unittest.main()