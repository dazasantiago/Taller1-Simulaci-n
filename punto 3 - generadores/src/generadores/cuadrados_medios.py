def cuadrados_medios(semilla: int, n_digitos: int, cantidad: int) -> list[int]:

    if type(semilla) != int or type(n_digitos) != int or type(cantidad) != int:
        raise TypeError("La semilla, el número de dígitos y la cantidad deben ser enteros.")

    if n_digitos < 3:
        raise ValueError("El número de dígitos debe ser mayor o igual a 3.")
    
    limite_maximo = 10 ** n_digitos
    if semilla < 0 or semilla >= limite_maximo:
        raise ValueError(f"La semilla debe estar entre 0 y {limite_maximo - 1}.")
        
    if cantidad < 0:
        raise ValueError("La cantidad no puede ser negativa.")

    valores = []
    semilla_actual = semilla
    longitud_esperada = 2 * n_digitos

    for _ in range(cantidad):
        cuadrado = semilla_actual ** 2
        cuadrado_str = str(cuadrado)
        
        cuadrado_str = cuadrado_str.zfill(longitud_esperada)
       
        inicio = (len(cuadrado_str) - n_digitos) // 2
        fin = inicio + n_digitos
        
        semilla_actual = int(cuadrado_str[inicio:fin])
        valores.append(semilla_actual)

    return valores