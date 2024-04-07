import pytest

from src.infrastructure.sentence_splitter import NltkSentenceSplitter


@pytest.mark.skip("skip")
def test_split_sequence_single_sentence():
    text = "This is a test."
    splitter = NltkSentenceSplitter()
    splitter.sent_tokenize.return_value = [text]
    sentences = splitter.split_sequence(text)
    assert sentences == [text]


@pytest.mark.skip("skip")
def test_split_sequence_multiple_sentences():
    text = "This is a test. This is another test."
    expected_sentences = ["This is a test.", "This is another test."]
    splitter = NltkSentenceSplitter()
    splitter.sent_tokenize.return_value = expected_sentences
    sentences = splitter.split_sequence(text)
    assert sentences == expected_sentences
