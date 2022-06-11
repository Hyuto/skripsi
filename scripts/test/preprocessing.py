from ..preprocessing import (
    TweetPreprocessing,
    normalize_text,
    remove_noise,
    replace_slang,
    replace_word_elongation,
)


def test_replace_slang():
    assert replace_slang("") == ""
    assert replace_slang("aminn") == "amin"
    assert replace_slang("emg siapa yg nanya") == "memang siapa yang bertanya"


def test_remove_noise():
    assert remove_noise("") == ""
    assert remove_noise("covid-19") == "covid"
    assert remove_noise("seneng 😄") == "seneng"
    assert remove_noise("saya \tmau makan\n") == "saya mau makan"
    assert remove_noise("kenapa emangnya!??....") == "kenapa emangnya"
    assert remove_noise("situs resmi unj https://unj.ac.id") == "situs resmi unj"
    assert remove_noise('<a href="https://google.com">situs google</a>') == "situs google"
    assert (
        remove_noise(
            """@nonacik93 udah kedua kali ini hahaha
            pertama ga mau vaksin, eh Qadarullah kena covid 2-2nya bulan2 lalu dan agak parah.
            eh skrg kena lagi Ama dokter yg katanya udah dicopot itu 😣😣😣
            ketika wa grup keluarga lebih dipercaya drpd peneliti 😅"""
        )
        == (
            "nonacik udah kedua kali ini hahaha pertama ga mau vaksin eh qadarullah kena covid "
            + "nya bulan lalu dan agak parah eh skrg kena lagi ama dokter yg katanya udah dicopot "
            + "itu ketika wa grup keluarga lebih dipercaya drpd peneliti"
        )
    )


def test_replace_word_elongation():
    assert replace_word_elongation("") == ""
    assert replace_word_elongation("kenapaa?") == "kenapa?"
    assert replace_word_elongation("kenapaaa?") == "kenapa?"
    assert replace_word_elongation("kenapaaaa?") == "kenapa?"
    assert replace_word_elongation("kenapaaaaa?") == "kenapa?"


def test_normalize_text():
    assert normalize_text("") == ""
    assert (
        normalize_text("Perekonomian Indonesia sedang dalam pertumbuhan yang membanggakan")
        == "ekonomi indonesia tumbuh bangga"
    )


def test_TweetPreprocessing():
    preprocessing = TweetPreprocessing()
    assert preprocessing.run("") == ""
    assert (
        preprocessing.run(
            """@nonacik93 udah kedua kali ini hahaha
            pertama ga mau vaksin, eh Qadarullah kena covid 2-2nya bulan2 lalu dan agak parah.
            eh skrg kena lagi Ama dokter yg katanya udah dicopot itu 😣😣😣
            ketika wa grup keluarga lebih dipercaya drpd peneliti 😅"""
        )
        == (
            "nonacik hahaha engak vaksin qadarulah covid parah dokter copot wa grup keluarga "
            + "percaya teliti"
        )
    )
