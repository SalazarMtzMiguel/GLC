"""
Created on Thu Nov  7 13:07:53 2024

Author: SalazarMartinez
"""

from collections import defaultdict

class GLC:
    def __init__(self, terminales, no_terminales, producciones, simbolo_inicial):
        self.terminales = set(terminales)
        self.no_terminales = set(no_terminales)
        self.producciones = producciones
        self.simbolo_inicial = simbolo_inicial

    def eliminar_no_generativos(self):
        """Eliminar simbolos no generativos."""
        generativos = set()
        while True:
            nuevo_generativo = False
            for nt, reglas in self.producciones.items():
                if nt not in generativos:
                    for regla in reglas:
                        if all(simbolo in generativos or simbolo in self.terminales for simbolo in regla):
                            generativos.add(nt)
                            nuevo_generativo = True
                            break
            if not nuevo_generativo:
                break
        self.no_terminales &= generativos
        self.producciones = {nt: [r for r in reglas if all(s in generativos or s in self.terminales for s in r)]
                            for nt, reglas in self.producciones.items() if nt in generativos}

    def eliminar_inaccesibles(self):
        """Eliminar simbolos inaccesibles."""
        accesibles = set([self.simbolo_inicial])
        cola = [self.simbolo_inicial]
        while cola:
            nt = cola.pop(0)
            for regla in self.producciones.get(nt, []):
                for simbolo in regla:
                    if simbolo in self.no_terminales and simbolo not in accesibles:
                        accesibles.add(simbolo)
                        cola.append(simbolo)
        self.no_terminales &= accesibles
        self.producciones = {nt: reglas for nt, reglas in self.producciones.items() if nt in accesibles}

    def eliminar_unitarias(self):
        """Eliminar producciones unitarias."""
        unitarias = defaultdict(set)
        for nt in self.no_terminales:
            for regla in self.producciones.get(nt, []):
                if len(regla) == 1 and regla[0] in self.no_terminales:
                    unitarias[nt].add(regla[0])

        for nt in self.no_terminales:
            por_procesar = list(unitarias[nt])
            while por_procesar:
                unitario = por_procesar.pop()
                if unitario in unitarias:
                    for simbolo in unitarias[unitario]:
                        if simbolo not in unitarias[nt]:
                            unitarias[nt].add(simbolo)
                            por_procesar.append(simbolo)

        nuevas_producciones = defaultdict(list)
        for nt, reglas in self.producciones.items():
            for regla in reglas:
                if len(regla) != 1 or regla[0] not in self.no_terminales:
                    nuevas_producciones[nt].append(regla)
            for unitario in unitarias[nt]:
                nuevas_producciones[nt].extend([r for r in self.producciones[unitario] if r != [nt]])

        self.producciones = nuevas_producciones

    def eliminar_vacias(self):
        """Eliminar producciones vacias."""
        nullable = set()
        for nt, reglas in self.producciones.items():
            for regla in reglas:
                if not regla:
                    nullable.add(nt)

        while True:
            nuevo_nullable = False
            for nt, reglas in self.producciones.items():
                if nt not in nullable:
                    for regla in reglas:
                        if all(s in nullable for s in regla):
                            nullable.add(nt)
                            nuevo_nullable = True
                            break
            if not nuevo_nullable:
                break

        nuevas_producciones = defaultdict(list)
        for nt, reglas in self.producciones.items():
            for regla in reglas:
                if regla:
                    combinaciones = [[]]
                    for simbolo in regla:
                        if simbolo in nullable:
                            combinaciones += [r + [simbolo] for r in combinaciones]
                        else:
                            combinaciones = [r + [simbolo] for r in combinaciones]
                    nuevas_producciones[nt].extend([r for r in combinaciones if r])

        self.producciones = nuevas_producciones

    def eliminar_inutiles(self):
        """Eliminar simbolos y producciones inutiles."""
        self.eliminar_no_generativos()
        self.eliminar_inaccesibles()

    def mostrar_gramatica(self):
        """Mostrar la gramatica."""
        print("Terminales:", self.terminales)
        print("No terminales:", self.no_terminales)
        print("Producciones:")
        for nt, reglas in self.producciones.items():
            produccion = " | ".join(" ".join(regla) for regla in reglas)
            print(f"{nt} -> {produccion}")
        print("Simbolo inicial:", self.simbolo_inicial)


# Ejemplo de uso
if __name__ == "__main__":
    # Caso de prueba 1
    terminales1 = ['a', 'b', 'c']
    no_terminales1 = ['S', 'A', 'B', 'C']
    producciones1 = {
        'S': [['A', 'B'], ['B']],
        'A': [['a']],
        'B': [['b'], ['A', 'S'], []],
        'C': [['c']]
    }
    simbolo_inicial1 = 'S'

    gramatica1 = GLC(terminales1, no_terminales1, producciones1, simbolo_inicial1)
    print("Gramatica original 1:")
    gramatica1.mostrar_gramatica()

    # Aplicar eliminaciones
    gramatica1.eliminar_inutiles()
    gramatica1.eliminar_unitarias()
    gramatica1.eliminar_vacias()

    print("\nGramatica 1 sin simbolos y producciones inutiles, unitarias y vacias:")
    gramatica1.mostrar_gramatica()

    # Caso de prueba 2
    terminales2 = ['0', '1']
    no_terminales2 = ['S', 'A', 'B']
    producciones2 = {
        'S': [['A', 'B'], ['B']],
        'A': [['0']],
        'B': [['1'], ['A', 'S'], ['A']]
    }
    simbolo_inicial2 = 'S'

    gramatica2 = GLC(terminales2, no_terminales2, producciones2, simbolo_inicial2)
    print("\nGramatica original 2:")
    gramatica2.mostrar_gramatica()

    # Aplicar eliminaciones
    gramatica2.eliminar_inutiles()
    gramatica2.eliminar_unitarias()
    gramatica2.eliminar_vacias()

    print("\nGramatica 2 sin simbolos y producciones inutiles, unitarias y vacias:")
    gramatica2.mostrar_gramatica()

    # Caso de prueba 3
    terminales3 = ['x', 'y']
    no_terminales3 = ['S', 'X', 'Y', 'Z']
    producciones3 = {
        'S': [['X', 'Y'], ['Y']],
        'X': [['x']],
        'Y': [['y'], ['X', 'S'], []],
        'Z': [['x', 'y']]
    }
    simbolo_inicial3 = 'S'

    gramatica3 = GLC(terminales3, no_terminales3, producciones3, simbolo_inicial3)
    print("\nGramatica original 3:")
    gramatica3.mostrar_gramatica()

    # Aplicar eliminaciones
    gramatica3.eliminar_inutiles()
    gramatica3.eliminar_unitarias()
    gramatica3.eliminar_vacias()

    print("\nGramatica 3 sin simbolos y producciones inutiles, unitarias y vacias:")
    gramatica3.mostrar_gramatica()

    # Caso de prueba 4
    terminales4 = ['a', 'b']
    no_terminales4 = ['S', 'A', 'B', 'C']
    producciones4 = {
        'S': [['A', 'B'], ['B']],
        'A': [['a']],
        'B': [['b'], ['A', 'S'], []],
        'C': [['a', 'b']]
    }
    simbolo_inicial4 = 'S'

    gramatica4 = GLC(terminales4, no_terminales4, producciones4, simbolo_inicial4)
    print("\nGramatica original 4:")
    gramatica4.mostrar_gramatica()

    # Aplicar eliminaciones
    gramatica4.eliminar_inutiles()
    gramatica4.eliminar_unitarias()
    gramatica4.eliminar_vacias()

    print("\nGramatica 4 sin simbolos y producciones inutiles, unitarias y vacias:")
    gramatica4.mostrar_gramatica()

