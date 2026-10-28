"""Heap binario manual (TP6) — indexación basada en 1."""
class HeapBinario:
    def __init__(self, es_max=True):
        self._datos = [None]
        self._n = 0
        self._es_max = es_max

    def __len__(self):
        return self._n

    def esta_vacio(self):
        return self._n == 0

    def _comparar(self, i, j):
        a = self._datos[i]
        b = self._datos[j]
        if self._es_max:
            if a > b: return True
            if a < b: return False
            return True
        else:
            if a < b: return True
            if a > b: return False
            return True

    def _subir(self, i):
        while i > 1:
            padre = i // 2
            if self._comparar(i, padre):
                self._datos[i], self._datos[padre] = self._datos[padre], self._datos[i]
                i = padre
            else:
                break

    def _bajar(self, i):
        while True:
            izq = 2 * i
            der = 2 * i + 1
            mejor = i
            if izq <= self._n and self._comparar(izq, mejor):
                mejor = izq
            if der <= self._n and self._comparar(der, mejor):
                mejor = der
            if mejor != i:
                self._datos[i], self._datos[mejor] = self._datos[mejor], self._datos[i]
                i = mejor
            else:
                break

    def insertar(self, valor):
        self._n += 1
        if len(self._datos) <= self._n:
            self._datos.append(valor)
        else:
            self._datos[self._n] = valor
        self._subir(self._n)

    def extraer_raiz(self):
        if self._n < 1:
            raise IndexError("Heap vacío")
        raiz = self._datos[1]
        if self._n == 1:
            self._datos[1] = None
            self._n = 0
            return raiz
        ultimo = self._datos[self._n]
        self._datos[1] = ultimo
        self._datos[self._n] = None
        self._n -= 1
        self._bajar(1)
        return raiz

    def ver_raiz(self):
        if self._n < 1:
            return None
        return self._datos[1]

    def top_n(self, n):
        if n <= 0:
            return []
        copia = HeapBinario(es_max=self._es_max)
        copia._datos = list(self._datos)
        copia._n = self._n
        resultado = []
        cantidad = min(n, copia._n)
        for _ in range(cantidad):
            resultado.append(copia.extraer_raiz())
        return resultado

