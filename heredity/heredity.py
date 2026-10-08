import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return the joint probability of all of the events
    described by the sets one_gene, two_genes, and have_trait.
    """

    probability = 1

    for person in people:

        # Determine number of genes.
        if person in two_genes:
            genes = 2
        elif person in one_gene:
            genes = 1
        else:
            genes = 0

        # Determine whether person has the trait.
        trait = person in have_trait

        # Calculate probability of this person's genes.
        mother = people[person]["mother"]
        father = people[person]["father"]

        if mother is None and father is None:
            # No parents: use the unconditional gene probabilities.
            gene_probability = PROBS["gene"][genes]

        else:
            # Probability mother passes the gene.
            mother_genes = (
                2 if mother in two_genes
                else 1 if mother in one_gene
                else 0
            )

            if mother_genes == 2:
                mother_pass = 1 - PROBS["mutation"]
            elif mother_genes == 1:
                mother_pass = 0.5
            else:
                mother_pass = PROBS["mutation"]

            # Probability father passes the gene.
            father_genes = (
                2 if father in two_genes
                else 1 if father in one_gene
                else 0
            )

            if father_genes == 2:
                father_pass = 1 - PROBS["mutation"]
            elif father_genes == 1:
                father_pass = 0.5
            else:
                father_pass = PROBS["mutation"]

            # Calculate probability of child's gene count.
            if genes == 2:
                gene_probability = mother_pass * father_pass

            elif genes == 1:
                gene_probability = (
                    mother_pass * (1 - father_pass)
                    + (1 - mother_pass) * father_pass
                )

            else:
                gene_probability = (
                    (1 - mother_pass) * (1 - father_pass)
                )

        # Probability of having/not having the trait.
        trait_probability = PROBS["trait"][genes][trait]

        # Multiply this person's probability into the joint probability.
        probability *= gene_probability * trait_probability

    return probability



def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add a new joint probability p to the existing probability distributions.
    """

    for person in probabilities:

        # Determine number of genes.
        if person in two_genes:
            genes = 2
        elif person in one_gene:
            genes = 1
        else:
            genes = 0

        # Add probability to the appropriate gene distribution.
        probabilities[person]["gene"][genes] += p

        # Determine whether person has the trait.
        trait = person in have_trait

        # Add probability to the appropriate trait distribution.
        probabilities[person]["trait"][trait] += p


def normalize(probabilities):
    """
    Normalize each probability distribution so that
    the values sum to 1.
    """

    for person in probabilities:

        # Normalize gene probabilities.
        gene_total = sum(probabilities[person]["gene"].values())

        for genes in probabilities[person]["gene"]:
            probabilities[person]["gene"][genes] /= gene_total

        # Normalize trait probabilities.
        trait_total = sum(probabilities[person]["trait"].values())

        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] /= trait_total



if __name__ == "__main__":
    main()
