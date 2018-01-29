from collections import Counter


def distinct_items(transactions, support):
    c = Counter()
    for trans in transactions:
        c.update(trans)
    return set(item for item in c if c[item] >= support)


def generate_candidates(L, k):
    candidates = set()
    for a in L:
        for b in L:
            union = a | b
            if len(union) == k and a != b:
                candidates.add(union)
    return candidates


def itemsets_support(transactions, itemsets):
    support_set = Counter()
    for trans in transactions:
        subsets = [itemset for itemset in itemsets if itemset < trans]
        support_set.update(subsets)
    return support_set


def apriori(transactions, support):
    candidates = set(frozenset([i]) for i in distinct_items(transactions, support))
    result = list()
    k = 2
    while candidates:
        candidates = generate_candidates(candidates, k)
        supported = itemsets_support(transactions, candidates)
        candidates = set([item for item in supported if supported[item] >= support])
        result += candidates
        k += 1
    return result

