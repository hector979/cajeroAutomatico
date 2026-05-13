personas = ["Nombre", "Edad", "Ciudad", "Profesión"]
diccionario1 = {"Nombre": "Hector", "Edad": 45, "Ciudad": "San Martin", "Profesión": "comerciante"}
diccionario2 = {"Nombre": "Maria", "Edad": 25, "Ciudad": "Bogota", "Profesión": "abogada"}
diccionario3 = {"Nombre": "Juan", "Edad": 40, "Ciudad": "Villavicencio", "Profesión": "medico"}
diccionario4 = {"Nombre": "Ana", "Edad": 35, "Ciudad": "Granada", "Profesión": "Meretris"}
lista_diccionarios = [diccionario1, diccionario2, diccionario3, diccionario4]
for d in lista_diccionarios:
    for p in personas:
        print(p + " : " + str(d[p]))
#print("el nombre de la persona que esta en la posicion 4 es: " + str(lista_diccionarios[3]["Nombre"]) + " y su profesion " + lista_diccionarios[3]["Profesión"])


