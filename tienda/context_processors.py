def carrito_count(request):

    carrito = request.session.get('carrito', [])

    return {
        'carrito_count': len(carrito)
    }