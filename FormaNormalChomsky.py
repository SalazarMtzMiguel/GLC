"""
Created on Thu Nov  7 13:07:53 2024

Author: SalazarMartinez
"""

class CFGtoCNF:
    def __init__(self, variables, terminals, start_symbol, productions):
        self.variables = variables
        self.terminals = terminals
        self.start_symbol = start_symbol
        self.productions = productions
        self.new_productions = {}
        self.new_variables = set()
        self.new_start_symbol = "S0"
        self.convert_to_cnf()

    def convert_to_cnf(self):
        """Convert the CFG to CNF."""
        self.add_new_start_symbol()
        self.remove_useless_productions()
        self.remove_empty_productions()
        self.remove_unit_productions()
        self.convert_to_binary()

    def add_new_start_symbol(self):
        """Add a new start symbol to the productions."""
        self.new_productions[self.new_start_symbol] = [[self.start_symbol]]
        self.new_variables.add(self.new_start_symbol)
        self.variables.add(self.new_start_symbol)
        self.productions[self.new_start_symbol] = [[self.start_symbol]]

    def remove_useless_productions(self):
        """Remove useless productions from the grammar."""
        generating = set()
        for var, prods in self.productions.items():
            for prod in prods:
                if all(symbol in self.terminals for symbol in prod):
                    generating.add(var)
        
        while True:
            new_generating = generating.copy()
            for var, prods in self.productions.items():
                for prod in prods:
                    if all(symbol in generating or symbol in self.terminals for symbol in prod):
                        new_generating.add(var)
            if new_generating == generating:
                break
            generating = new_generating

        reachable = {self.new_start_symbol}
        while True:
            new_reachable = reachable.copy()
            for var in reachable:
                for prod in self.productions.get(var, []):
                    for symbol in prod:
                        if symbol in self.variables:
                            new_reachable.add(symbol)
            if new_reachable == reachable:
                break
            reachable = new_reachable

        self.productions = {var: prods for var, prods in self.productions.items() if var in generating and var in reachable}

    def remove_empty_productions(self):
        """Remove empty productions from the grammar."""
        nullable = set()
        for var, prods in self.productions.items():
            for prod in prods:
                if not prod:
                    nullable.add(var)

        while True:
            new_nullable = nullable.copy()
            for var, prods in self.productions.items():
                for prod in prods:
                    if all(symbol in nullable for symbol in prod):
                        new_nullable.add(var)
            if new_nullable == nullable:
                break
            nullable = new_nullable

        new_productions = {}
        for var, prods in self.productions.items():
            new_productions[var] = []
            for prod in prods:
                if prod:
                    combinations = [[]]
                    for symbol in prod:
                        if symbol in nullable:
                            combinations += [r + [symbol] for r in combinations]
                        else:
                            combinations = [r + [symbol] for r in combinations]
                    new_productions[var].extend([r for r in combinations if r])
        self.productions = new_productions

    def remove_unit_productions(self):
        """Remove unit productions from the grammar."""
        unit_productions = {var: set() for var in self.variables}
        for var, prods in self.productions.items():
            for prod in prods:
                if len(prod) == 1 and prod[0] in self.variables:
                    unit_productions[var].add(prod[0])

        for var in self.variables:
            to_process = list(unit_productions[var])
            while to_process:
                unit = to_process.pop()
                if unit in unit_productions:
                    for symbol in unit_productions[unit]:
                        if symbol not in unit_productions[var]:
                            unit_productions[var].add(symbol)
                            to_process.append(symbol)

        new_productions = {}
        for var, prods in self.productions.items():
            new_productions[var] = []
            for prod in prods:
                if len(prod) != 1 or prod[0] not in self.variables:
                    new_productions[var].append(prod)
            for unit in unit_productions[var]:
                new_productions[var].extend([p for p in self.productions[unit] if p != [var]])
        self.productions = new_productions

    def convert_to_binary(self):
        """Convert productions to binary form."""
        new_productions = {}
        for var, prods in self.productions.items():
            new_productions[var] = []
            for prod in prods:
                while len(prod) > 2:
                    new_var = self.get_new_variable()
                    self.new_variables.add(new_var)
                    self.variables.add(new_var)
                    new_productions[new_var] = [[prod[0], prod[1]]]
                    prod = [new_var] + prod[2:]
                new_productions[var].append(prod)
        self.productions = new_productions

    def get_new_variable(self):
        """Generate a new variable not in the current set of variables."""
        i = 1
        while f"X{i}" in self.variables or f"X{i}" in self.new_variables:
            i += 1
        return f"X{i}"

    def get_cnf(self):
        """Return the CNF productions."""
        return self.productions

    def display_cnf(self):
        """Display the CNF productions."""
        print("Producciones en Forma Normal de Chomsky (CNF):")
        for var, prods in self.get_cnf().items():
            print(f"{var} -> ", end="")
            for prod in prods:
                print(" ".join(prod), end=" | ")
            print("")


# Ejemplo de uso con la gramatica aseada dada
if __name__ == "__main__":
    # Ejemplo 1
    variables1 = {"S", "A", "B", "C"}
    terminals1 = {"a", "b", "c"}
    start_symbol1 = "S"
    productions1 = {
        "S": [["A", "B", "C"]],
        "A": [["a"]],
        "B": [["b"]],
        "C": [["c"]]
    }

    cfg_to_cnf1 = CFGtoCNF(variables1, terminals1, start_symbol1, productions1)
    print("CNF para Ejemplo 1:")
    cfg_to_cnf1.display_cnf()

    # Ejemplo 2
    variables2 = {"S", "A", "B"}
    terminals2 = {"0", "1"}
    start_symbol2 = "S"
    productions2 = {
        "S": [["A", "B"], ["B"]],
        "A": [["0"]],
        "B": [["1"], ["A", "S"], ["A"]]
    }

    cfg_to_cnf2 = CFGtoCNF(variables2, terminals2, start_symbol2, productions2)
    print("\nCNF para Ejemplo 2:")
    cfg_to_cnf2.display_cnf()

    # Ejemplo 3
    variables3 = {"S", "X", "Y", "Z"}
    terminals3 = {"x", "y"}
    start_symbol3 = "S"
    productions3 = {
        "S": [["X", "Y"], ["Y"]],
        "X": [["x"]],
        "Y": [["y"], ["X", "S"], []],
        "Z": [["x", "y"]]
    }

    cfg_to_cnf3 = CFGtoCNF(variables3, terminals3, start_symbol3, productions3)
    print("\nCNF para Ejemplo 3:")
    cfg_to_cnf3.display_cnf()

    # Ejemplo 4
    variables4 = {"S", "A", "B", "C"}
    terminals4 = {"a", "b"}
    start_symbol4 = "S"
    productions4 = {
        "S": [["A", "B"], ["B"]],
        "A": [["a"]],
        "B": [["b"], ["A", "S"], []],
        "C": [["a", "b"]]
    }

    cfg_to_cnf4 = CFGtoCNF(variables4, terminals4, start_symbol4, productions4)
    print("\nCNF para Ejemplo 4:")
    cfg_to_cnf4.display_cnf()

    # Ejemplo 5
    variables5 = {"S", "A", "B", "C", "D"}
    terminals5 = {"a", "b", "c"}
    start_symbol5 = "S"
    productions5 = {
        "S": [["A", "B"], ["C", "D"]],
        "A": [["a"]],
        "B": [["b"]],
        "C": [["c"]],
        "D": [["A", "B"]]
    }

    cfg_to_cnf5 = CFGtoCNF(variables5, terminals5, start_symbol5, productions5)
    print("\nCNF para Ejemplo 5:")
    cfg_to_cnf5.display_cnf()
