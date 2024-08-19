from itertools import combinations
TRUE, FALSE, UNKNOWN = 2, 0, 1

class Sentence():

    def evaluate(self, model): raise NotImplementedError # Evaluates the logical sentence.
    def formula(self): raise NotImplementedError # Returns string formula representing logical sentence.
    def symbols(self): raise NotImplementedError # Returns a set of all symbols in the logical sentence.
    def parenthesize(self):return self.formula() if self.formula().startsWith('(') and self.formula().endsWith(')') else f"({self.formula()})"

    @classmethod
    def validate(cls, sentence):
        if not isinstance(sentence, Sentence): raise TypeError("must be a logical sentence")

class Symbol(Sentence):

    def __init__(self, name): self.name = name
    def __eq__(self, other): return isinstance(other, Symbol) and self.name == other.name
    def __hash__(self): return hash(("symbol", self.name))
    def __repr__(self): return self.name
    def evaluate(self, model): return model.get(self.name, UNKNOWN)
    def formula(self): return self.name
    def symbols(self): return {self.name}

class Not(Sentence):
    def __init__(self, operand):
        Sentence.validate(operand)
        self.operand = operand

    def __eq__(self, other): return isinstance(other, Not) and self.operand == other.operand
    def __hash__(self): return hash(("not", hash(self.operand)))
    def __repr__(self): return f"Not({self.operand})"
    def evaluate(self, model): return (TRUE, UNKNOWN, FALSE)[self.operand.evaluate(model)]
    def formula(self): return "¬" + Sentence.parenthesize(self.operand.formula())
    def symbols(self): return self.operand.symbols()

class And(Sentence):
    def __init__(self, *conjuncts):
        for conjunct in conjuncts:
            Sentence.validate(conjunct)
        self.conjuncts = list(conjuncts)

    def __eq__(self, other): return isinstance(other, And) and self.conjuncts == other.conjuncts
    def __hash__(self): return hash(("and", tuple(hash(conjunct) for conjunct in self.conjuncts)))
    def __repr__(self): 
        conjunctions = ", ".join([str(conjunct) for conjunct in self.conjuncts])
        return f"And({conjunctions})"
    def add(self, *conjuncts):
        for conjunct in conjuncts:
            Sentence.validate(conjunct)
            self.conjuncts.append(conjunct)

    def evaluate(self, model): return min(conjunct.evaluate(model) for conjunct in self.conjuncts)

    def formula(self):
        if len(self.conjuncts) == 1: return self.conjuncts[0].formula()
        return " ∧ ".join([Sentence.parenthesize(conjunct.formula()) for conjunct in self.conjuncts])

    def symbols(self): return set() if not self.conjuncts else set.union(*[conjunct.symbols() for conjunct in self.conjuncts])


class Or(Sentence):
    def __init__(self, *disjuncts):
        for disjunct in disjuncts:
            Sentence.validate(disjunct)
        self.disjuncts = tuple(disjuncts)

    def __eq__(self, other): return isinstance(other, Or) and self.disjuncts == other.disjuncts
    def __hash__(self): return hash(("or", tuple(hash(disjunct) for disjunct in self.disjuncts)))
    def __repr__(self):
        disjuncts = ", ".join([str(disjunct) for disjunct in self.disjuncts])
        return f"Or({disjuncts})"

    def evaluate(self, model): return max(disjunct.evaluate(model) for disjunct in self.disjuncts)

    def formula(self):
        if len(self.disjuncts) == 1:
            return self.disjuncts[0].formula()
        return " ∨ ".join([Sentence.parenthesize(disjunct.formula()) for disjunct in self.disjuncts])

    def symbols(self): return set.union(*[disjunct.symbols() for disjunct in self.disjuncts])


class Implication(Sentence):
    def __init__(self, antecedent, consequent):
        Sentence.validate(antecedent)
        Sentence.validate(consequent)
        self.antecedent = antecedent
        self.consequent = consequent

    def __eq__(self, other): return isinstance(other, Implication) and self.antecedent == other.antecedent and self.consequent == other.consequent
    def __hash__(self): return hash(("implies", hash(self.antecedent), hash(self.consequent)))
    def __repr__(self): return f"Implication({self.antecedent}, {self.consequent})"

    def evaluate(self, model):
        if self.antecedent.evaluate(model) == FALSE or self.consequent.evaluate(model) == TRUE: return TRUE
        elif self.antecedent.evaluate(model) == TRUE and self.consequent.evaluate(model) == FALSE: return FALSE
        else: return UNKNOWN

    def formula(self):
        antecedent = Sentence.parenthesize(self.antecedent.formula())
        consequent = Sentence.parenthesize(self.consequent.formula())
        return f"{antecedent} => {consequent}"

    def symbols(self): return set.union(self.antecedent.symbols(), self.consequent.symbols())


class Biconditional(Sentence):
    def __init__(self, left, right):
        Sentence.validate(left)
        Sentence.validate(right)
        self.left = left
        self.right = right

    def __eq__(self, other): return isinstance(other, Biconditional) and self.left == other.left and self.right == other.right
    def __hash__(self): return hash(("biconditional", hash(self.left), hash(self.right)))
    def __repr__(self): return f"Biconditional({self.left}, {self.right})"

    def evaluate(self, model):
        L, R = self.left.evaluate(model), self.right.evaluate(model)
        if UNKNOWN in (L, R): return UNKNOWN
        elif L == R: return TRUE
        else: return FALSE

    def formula(self):
        left = Sentence.parenthesize(str(self.left))
        right = Sentence.parenthesize(str(self.right))
        return f"{left} <=> {right}"

    def symbols(self): return set.union(self.left.symbols(), self.right.symbols())


def model_check(knowledge, debug=False):
    truth_values = {sym: None for sym in sorted(knowledge.symbols())}
    can_be_true_or_false = {FALSE: set(), TRUE: set()}
    modified = True
    while modified:
        modified = False
        unprocessed_syms = {sym: UNKNOWN for sym in truth_values if truth_values[sym] is None}  # get a dict of as-yet-undetermined symbols
        for r in range(len(unprocessed_syms)):  # do 'fast' checks first, i.e. those with more UNKNOWNS.
            for sym in unprocessed_syms:  # pick an undetermined sym
                debug and print(f"Testing {sym}:")
                (other_syms := unprocessed_syms.copy()).pop(sym)  # get a dict of other syms

                # need to do something if other_syms is empty

                for combi in combinations(other_syms, r):  # iterate over all combis of r symbols. If all combis result in FALSE, then symbol must be the opposite.
                    all_models_false = {TRUE: True, FALSE: True}  # record if all models evaluate FALSE
                    conjuncts_causing_false = {TRUE: set(), FALSE: set()}
                    for try_true_false in (TRUE, FALSE):  # try both TRUE and FALSE for the chosen undetermined sym
                        (model := truth_values.copy()).update(unprocessed_syms)
                        model[sym] = try_true_false
                        for binary_num in range(2 ** r):  # for the chosen combi of r symbols, iterate over all TRUE/FALSE permutations
                            model.update({v: (TRUE, FALSE)[(binary_num >> i) & 1] for i, v in enumerate(combi)})  
                            debug and print(f"{model} -> {knowledge.evaluate(model)}")
                            if knowledge.evaluate(model) != FALSE:  # if some model evaluates TRUE for the combi, then we record down possible values for each symbol.
                                all_models_false[try_true_false] = False
                                if UNKNOWN in model.values(): continue
                                for tested_sym in model:
                                    # Now the model has no UNKNOWNS, so syms for which both TRUE/FALSE can produce true models, will be indeterminate.
                                    if model[tested_sym] not in (TRUE, FALSE): continue
                                    can_be_true_or_false[model[tested_sym]].add(tested_sym)
                                    modified = True
                                    if tested_sym in can_be_true_or_false[2 - model[tested_sym]]:
                                        truth_values[tested_sym] = UNKNOWN
                                        modified = True
                                        print(f"{tested_sym} must be indeterminate.")
                                break
                            elif isinstance(knowledge, And):
                                for conjunct in knowledge.conjuncts:
                                    if conjunct.evaluate(model) == FALSE:
                                        conjuncts_causing_false[try_true_false].add(conjunct)
                    if all_models_false[TRUE] and all_models_false[FALSE]:
                        # if all models for a combi evaluate FALSE regardless if the chosen sym is TRUE/FALSE, then we have a paradox.
                        print(f"Paradox detected: {sym} can be neither true nor false!")
                        print(f"- {sym} cannot be True due to: {', '.join([str(c) for c in conjuncts_causing_false[TRUE]])}")
                        print(f"- {sym} cannot be False due to: {', '.join([str(c) for c in conjuncts_causing_false[FALSE]])}")
                        return {s: None for s in truth_values}
                        # raise Exception(f"Paradox detected: {sym} can be neither true nor false!")
                    elif all_models_false[TRUE] ^ all_models_false[FALSE]:          # if all models evaluate FALSE for only one TRUE/FALSE value of the sym, then
                        truth_values[sym] = (FALSE, TRUE)[all_models_false[FALSE]]  # the sym must be the other value.
                        print(f"{sym} must be {('False', '<error>', 'True')[truth_values[sym]]}")
                        modified = True
                        break
                    elif modified:
                        break
                else:
                    continue
                break
            else:
                continue
            break
    return truth_values
