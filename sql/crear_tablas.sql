CREATE TABLE nominas (
    id_nomina UUID PRIMARY KEY,
    salario NUMERIC(15, 2) NOT NULL CHECK (salario >= 0),
    dias INTEGER NOT NULL CHECK (dias BETWEEN 0 AND 30),
    bonificacion NUMERIC(15, 2) NOT NULL CHECK (bonificacion >= 0),
    comision NUMERIC(15, 2) NOT NULL CHECK (comision >= 0),
    descuentos NUMERIC(15, 2) NOT NULL CHECK (descuentos >= 0)
);