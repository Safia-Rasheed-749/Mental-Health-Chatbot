import re

def clean_text(text):

    text = str(text).lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


if __name__ == "__main__":

    sample = "Visit https://reddit.com I Feel VERY Depressed"

    print("Original")
    print(sample)

    print("\nCleaned")
    print(clean_text(sample))