from backend.langchain_workflows.qa_chain import create_qa_chain


def test_create_qa_chain():
    chain = create_qa_chain()
    assert chain is not None
