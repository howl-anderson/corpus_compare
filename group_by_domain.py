import collections
from pathlib import Path

from tokenizer_tools.tagset.offset.corpus import Corpus


def group_by_domain(input_file, output_dir):
    output_dir = Path(output_dir)

    corpus = Corpus.read_from_file(input_file)

    domain_doc = collections.defaultdict(list)
    for doc in corpus:
        domain_doc[doc.domain].append(doc)

    for domain, doc_list in domain_doc.items():
        output_file = output_dir / "{}.conllx".format(domain)

        corpus = Corpus(doc_list)
        corpus.write_to_file(output_file)


if __name__ == "__main__":
    group_by_domain("data.conllx", "domain_data")
