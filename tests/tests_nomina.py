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
        neto_esperado: float = 2760000
        datos = DatosNomina(3000000, 30, 0, 0, 0)
        neto_calculado: float = logica_nomina.calcular_nomina(datos)
        self.assertAlmostEqual(neto_esperado, neto_calculado, 2)

    def test_normal_2(self) -> None:
        neto_esperado: float = 2760000
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
        neto_esperado: float = 1380000
        datos = DatosNomina(3000000, 15, 0, 0, 0)
        neto_calculado: float = logica_nomina.calcular_nomina(datos)
        self.assertAlmostEqual(neto_esperado, neto_calculado, 2)

    def test_extraordinario_3(self) -> None:
        neto_esperado: float = 7360000
        datos = DatosNomina(3000000, 30, 0, 5000000, 0)
        neto_calculado: float = logica_nomina.calcular_nomina(datos)
        self.assertAlmostEqual(neto_esperado, neto_calculado, 2)

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