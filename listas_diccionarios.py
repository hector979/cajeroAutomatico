personas = ["Nombre", "Edad", "Ciudad", "Profesión"]
diccionario = {"Nombre": "Hector", "Edad": 30, "Ciudad": "San Martin", "Profesión": "comerciante"}
for p in personas:
    print(p + ": " + str(diccionario[p]))
