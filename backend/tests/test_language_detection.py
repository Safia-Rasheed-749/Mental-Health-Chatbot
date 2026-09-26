from app.ai.llm.prompt import detect_language


def test_supported_language_detection():
    assert detect_language("I feel sad today") == "english"
    assert detect_language("Mujhe bohat udaas mehsoos ho raha hai") == "roman_urdu"
    assert detect_language("مجھے آج بہت اداس محسوس ہو رہا ہے") == "urdu"
