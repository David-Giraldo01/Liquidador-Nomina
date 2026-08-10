import unittest
from src import logica_nomina

class TestsNomina(unittest.TestCase):

    def test_normal_1(self):

        # ENTRADAS
        salario = 3000000
        dias = 30
        bonificacion = 0
        comision = 0
        descuentos = 0

        # SALIDA ESPERADA
        neto_esperado = 2760000

        # INVOCAR LA FUNCIONALIDAD
        neto_calculado = logica_nomina.calcular_nomina(
            salario,
            dias,
            bonificacion,
            comision,
            descuentos
        )

        # VERIFICAR EL RESULTADO
        self.assertAlmostEqual(
            neto_esperado,
            neto_calculado,
            2
        )

    def test_normal_2(self):

        # ENTRADAS
        salario = 2500000
        dias = 30
        bonificacion = 200000
        comision = 300000
        descuentos = 0

        # SALIDA ESPERADA
        neto_esperado = 2760000

        # INVOCAR LA FUNCIONALIDAD
        neto_calculado = logica_nomina.calcular_nomina(
            salario,
            dias,
            bonificacion,
            comision,
            descuentos
        )

        # VERIFICAR EL RESULTADO
        self.assertAlmostEqual(
            neto_esperado,
            neto_calculado,
            2
        )

    def test_normal_3(self):

        # ENTRADAS
        salario = 4000000
        dias = 30
        bonificacion = 500000
        comision = 0
        descuentos = 100000

        # SALIDA ESPERADA
        neto_esperado = 4040000

        # INVOCAR LA FUNCIONALIDAD
        neto_calculado = logica_nomina.calcular_nomina(
            salario,
            dias,
            bonificacion,
            comision,
            descuentos
        )

        # VERIFICAR EL RESULTADO
        self.assertAlmostEqual(
            neto_esperado,
            neto_calculado,
            2
        )

    def test_extraordinario_1(self):

        # ENTRADAS
        salario = 80000000
        dias = 30
        bonificacion = 0
        comision = 0
        descuentos = 0

        # SALIDA ESPERADA
        neto_esperado = 73600000

        # INVOCAR LA FUNCIONALIDAD
        neto_calculado = logica_nomina.calcular_nomina(
            salario,
            dias,
            bonificacion,
            comision,
            descuentos
        )

        # VERIFICAR EL RESULTADO
        self.assertAlmostEqual(
            neto_esperado,
            neto_calculado,
            2
        )

    def test_extraordinario_2(self):

        # ENTRADAS
        salario = 3000000
        dias = 15
        bonificacion = 0
        comision = 0
        descuentos = 0

        # SALIDA ESPERADA
        neto_esperado = 1380000

        # INVOCAR LA FUNCIONALIDAD
        neto_calculado = logica_nomina.calcular_nomina(
            salario,
            dias,
            bonificacion,
            comision,
            descuentos
        )

        # VERIFICAR EL RESULTADO
        self.assertAlmostEqual(
            neto_esperado,
            neto_calculado,
            2
        )

if __name__ == "__main__":
    unittest.main()