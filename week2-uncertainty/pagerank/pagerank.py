import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page
    a random surfer would visit next.
    """

    probabilities = {}

    total_pages = len(corpus)
    links = corpus[page]

    # If the page has no outgoing links, treat it as
    # linking to every page in the corpus.
    if not links:
        for p in corpus:
            probabilities[p] = 1 / total_pages

        return probabilities

    # Probability of randomly jumping to any page.
    random_probability = (1 - damping_factor) / total_pages

    # Start every page with the random-jump probability.
    for p in corpus:
        probabilities[p] = random_probability

    # Add the probability of following a link.
    link_probability = damping_factor / len(links)

    for linked_page in links:
        probabilities[linked_page] += link_probability

    return probabilities



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling.
    """

    # Initialize visit counts.
    counts = {}

    for page in corpus:
        counts[page] = 0

    # Choose the first page randomly.
    page = random.choice(list(corpus.keys()))

    # Take n samples.
    for _ in range(n):

        # Count the current page.
        counts[page] += 1

        # Get the transition probabilities from this page.
        probabilities = transition_model(
            corpus,
            page,
            damping_factor
        )

        # Choose the next page based on the probabilities.
        pages = list(probabilities.keys())
        weights = list(probabilities.values())

        page = random.choices(
            pages,
            weights=weights,
            k=1
        )[0]

    # Convert counts into probabilities.
    pageranks = {}

    for page in corpus:
        pageranks[page] = counts[page] / n

    return pageranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively
    calculating PageRank values.
    """

    num_pages = len(corpus)

    # Start with every page having equal PageRank.
    pagerank = {}

    for page in corpus:
        pagerank[page] = 1 / num_pages

    while True:

        new_pagerank = {}

        for page in corpus:

            # Random jump contribution.
            rank = (1 - damping_factor) / num_pages

            # Calculate contribution from every page
            # that could link to this page.
            for source in corpus:

                links = corpus[source]

                # A page with no outgoing links is treated
                # as linking to every page.
                if not links:
                    num_links = num_pages

                    if page in corpus:
                        rank += (
                            damping_factor
                            * pagerank[source]
                            / num_links
                        )

                # Normal page with outgoing links.
                elif page in links:
                    rank += (
                        damping_factor
                        * pagerank[source]
                        / len(links)
                    )

            new_pagerank[page] = rank

        # Check whether all values have converged.
        converged = True

        for page in corpus:
            if abs(new_pagerank[page] - pagerank[page]) > 0.001:
                converged = False
                break

        pagerank = new_pagerank

        if converged:
            break

    return pagerank



if __name__ == "__main__":
    main()
