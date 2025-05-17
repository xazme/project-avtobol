def romanToInt(s: str) -> int:
    romanian = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
    }

    for index_of_char in range(len(s) - 1):
        print(f"{s[index_of_char]} and {index_of_char}")
        print(f"{s[index_of_char +1]} and {index_of_char+1}")
        print("&&&&&&&&&&&&&")


print(romanToInt("MCMXCIV"))
