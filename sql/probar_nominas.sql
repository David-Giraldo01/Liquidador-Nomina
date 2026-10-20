-- Ejemplo manual de inserción y consulta.
-- Requiere que la tabla nominas ya exista con id_nomina de tipo UUID.
-- El UUID fijo es solo para esta demostración.
-- En la aplicación, Python genera los identificadores con uuid4().
-- Ejecutar el bloque completo: ROLLBACK evita conservar el registro.

BEGIN;

INSERT INTO nominas (
    id_nomina,
    salario,
    dias,
    bonificacion,
    comision,
    descuentos
)
VALUES (
    'b8d961b7-62e9-4dab-987c-339bf318f057',
    3000000,
    30,
    0,
    0,
    0
);

SELECT
    id_nomina,
    salario,
    dias,
    bonificacion,
    comision,
    descuentos
FROM nominas
WHERE id_nomina = 'b8d961b7-62e9-4dab-987c-339bf318f057';

ROLLBACK;