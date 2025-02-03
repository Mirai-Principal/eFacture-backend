def Singleton(cls):
    """Decorador para convertir una clase en Singleton."""
    instances = {}  # Diccionario donde guardaremos la instancia única

    def get_instance(*args, **kwargs):
        if cls not in instances:  # Si la clase no está en el diccionario...
            instances[cls] = cls(*args, **kwargs)  # ...creamos y guardamos la instancia
        return instances[cls]  # Retornamos la misma instancia siempre

    return get_instance  # Devolvemos la función que maneja la instancia
