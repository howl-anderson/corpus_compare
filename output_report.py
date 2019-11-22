import pickle

from output_format.mismatched_human_annotation import write_compare_to_file


def output_report(compare_result_file):
    with open(compare_result_file, "rb") as fd:
        compare_result_data = pickle.load(fd)

    for (
        corpus_count,
        mismatch_count,
        mismatch_pair,
        output_file_without_ext,
    ) in compare_result_data:

        write_compare_to_file(
            corpus_count, mismatch_count, mismatch_pair, output_file_without_ext
        )


if __name__ == "__main__":
    output_report("compare_result.pkl")
