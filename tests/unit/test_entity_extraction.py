from backend.langchain_workflows.entity_extraction import extract_names, extract_dates, extract_amounts


def test_extract_names():
    text = "John Doe met with Jane Smith in New York."
    names = extract_names(text)
    assert "John Doe" in names
    assert "Jane Smith" in names


def test_extract_dates():
    text = "The event happened on 2024-01-15 and ended March 1, 2024."
    dates = extract_dates(text)
    assert len(dates) >= 2


def test_extract_amounts():
    text = "The total cost is $1,500.00 and the budget is 10000 USD."
    amounts = extract_amounts(text)
    assert len(amounts) >= 2
