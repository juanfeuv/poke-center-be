# Define una función para la clave de ordenamiento
def criterios_orden(objeto):
    hp = objeto.get('hp')
    cambio_estado = objeto.get('cambioEstado')
    nivel = objeto.get('nivel')
    created_at = objeto.get('createdAt')

    # Menor valor de hp tiene más prioridad
    # Si hp es igual, el cambioEstado tiene más prioridad
    # Si hp y cambioEstado son iguales, menor nivel tiene más prioridad
    # Si hp, cambioEstado y nivel son iguales, menor createdAt tiene más prioridad

    return (hp, not cambio_estado, nivel, created_at)
