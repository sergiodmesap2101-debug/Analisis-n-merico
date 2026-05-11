"""
temple.py - Metodo de Biseccion (Busqueda de Raices) para el Desafio del Templo.

Funcion:    f(x) = x^3 - 4x - 2
Intervalo:  [2, 3]
Tolerancia: 0.001
Max Iter:   50

El Metodo de Biseccion se implementa manualmente sin librerias externas.
Este metodo numerico es el requisito academico central del proyecto.
"""


def funcion_templo(x):
    """Evaluar f(x) = x^3 - 4x - 2."""
    return x ** 3 - 4 * x - 2


def metodo_biseccion(a=2.0, b=3.0, tol=0.001, max_iter=50):
    """
    Metodo de Biseccion para busqueda de raices.

    Encuentra la raiz de f(x) = x^3 - 4x - 2 en el intervalo [a, b].

    Algoritmo:
        1. Verificar cambio de signo: f(a) * f(b) < 0
        2. Calcular punto medio c = (a + b) / 2
        3. Evaluar f(c)
        4. Actualizar intervalo: si f(a)*f(c) < 0 entonces b = c, sino a = c
        5. Repetir hasta que |f(c)| < tol o (b - a)/2 < tol

    Retorna:
        tupla: (raiz, convergio, iteraciones, pasos)
            - raiz (float o None): valor aproximado de la raiz
            - convergio (bool): si el metodo convergio
            - iteraciones (int): numero de iteraciones realizadas
            - pasos (list[dict]): detalles de cada iteracion para visualizacion
    """
    fa = funcion_templo(a)
    fb = funcion_templo(b)

    # Paso 1: Verificar cambio de signo en el intervalo
    if fa * fb > 0:
        return None, False, 0, []

    pasos = []

    for i in range(1, max_iter + 1):
        # Paso 2: Calcular punto medio
        c = (a + b) / 2.0
        # Paso 3: Evaluar funcion en el punto medio
        fc = funcion_templo(c)

        # Registrar detalles del paso
        pasos.append({
            "iter": i,
            "a": round(a, 6),
            "b": round(b, 6),
            "c": round(c, 6),
            "fc": round(fc, 6),
        })

        # Paso 5: Verificar convergencia
        if abs(fc) < tol or (b - a) / 2.0 < tol:
            return round(c, 4), True, i, pasos

        # Paso 4: Actualizar limites del intervalo
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    # No convergio dentro del maximo de iteraciones
    return round(c, 4), False, max_iter, pasos
