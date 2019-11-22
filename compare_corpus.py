import pickle
from pathlib import Path

from deliverable_model.serving import SimpleModelInference
from tokenizer_tools.tagset.offset.corpus import Corpus

smi = SimpleModelInference("./model/deliverable_model")


def corpus_compare(input_dir, output_dir, compare_result_file):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    compare_result_data = []

    for corpus_file in input_dir.glob("*.conllx"):
        output_file_basename = corpus_file.with_suffix("").name
        output_file_without_ext = output_dir / output_file_basename

        corpus = Corpus.read_from_file(corpus_file)

        corpus_count = len(corpus)
        mismatch_count = 0
        mismatch_pair = []

        text_list = ["".join(i.text) for i in corpus]
        predict_info_list = list(smi.parse(text_list))

        doc_list = [i.sequence for i in predict_info_list]

        predict_corpus = Corpus(doc_list)
        for gold_doc, predict_doc in zip(corpus, predict_corpus):
            if gold_doc.compare_entities(predict_doc):
                continue

            mismatch_count += 1

            mismatch_pair.append((gold_doc, predict_doc))

        compare_result_data.append(
            (corpus_count, mismatch_count, mismatch_pair, output_file_without_ext)
        )

    with open(compare_result_file, "wb") as fd:
        pickle.dump(compare_result_data, fd)


if __name__ == "__main__":
    corpus_compare("./domain_data", "./report", "compare_result.pkl")
