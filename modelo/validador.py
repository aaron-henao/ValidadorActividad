from abc import ABC, abstractmethod
from errores import (ValidadorError, NoCumpleLongitudMinimaError, NoTieneLetraMayusculaError,
                     NoTieneLetraMinusculaError, NoTieneNumeroError, NoTieneCaracterEspecialError,
                     NoTienePalabraSecretaError)


class ReglaValidacion(ABC):
    def __init__(self, longitud_esperada):
        self._longitud_esperada = longitud_esperada

    @abstractmethod
    def es_valida(self, clave):
        pass

    def _validar_longitud(self, clave):
        if len(clave) <= self._longitud_esperada:
            raise NoCumpleLongitudMinimaError()

    def _contiene_mayuscula(self, clave):
        if not any(c.isupper() for c in clave):
            raise NoTieneLetraMayusculaError()

    def _contiene_minuscula(self, clave):
        if not any(c.islower() for c in clave):
            raise NoTieneLetraMinusculaError()

    def _contiene_numero(self, clave):
        if not any(c.isdigit() for c in clave):
            raise NoTieneNumeroError()


class ReglaValidacionGanimedes(ReglaValidacion):
    def contiene_caracter_especial(self, clave):
        if not any(c in '@_#$%' for c in clave):
            raise NoTieneCaracterEspecialError()

    def es_valida(self, clave):
        self._validar_longitud(clave)
        self._contiene_mayuscula(clave)
        self._contiene_minuscula(clave)
        self._contiene_numero(clave)
        self.contiene_caracter_especial(clave)
        return True


class ReglaValidacionCalisto(ReglaValidacion):
    def contiene_palabra_secreta(self, clave):
        if 'calisto' not in clave.lower():
            raise NoTienePalabraSecretaError()

    def es_valida(self, clave):
        self._validar_longitud(clave)
        self._contiene_numero(clave)
        self.contiene_palabra_secreta(clave)
        return True


class Validador:
    def __init__(self, regla):
        self.regla = regla

    def es_valida(self, clave):
        return self.regla.es_valida(clave)

# Crear una instancia del Validador con la regla de Validación Ganimedes
validador_ganimedes = Validador(ReglaValidacionGanimedes(8))

# Validar una clave utilizando la regla de Validación Ganimedes
clave = "ClaveSegura123@"
try:
    resultado = validador_ganimedes.es_valida(clave)
    print("La clave es válida.")
except ValidadorError as e:
    print("La clave no cumple la regla de Validación Ganimedes:", str(e))

# Crear una instancia del Validador con la regla de Validación Calisto
validador_calisto = Validador(ReglaValidacionCalisto(6))

# Validar una clave utilizando la regla de Validación Calisto
clave = "ClaveCalisto123"
try:
    resultado = validador_calisto.es_valida(clave)
    print("La clave es válida.")
except ValidadorError as e:
    print("La clave no cumple la regla de Validación Calisto:", str(e))
