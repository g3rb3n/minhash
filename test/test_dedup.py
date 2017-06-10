from minhash.dedup import Dedup

def test_dedup():
    dedup = Dedup()
    res = dedup.is_duplicate('This is a test')
    assert res == False, "Initial item can not be a duplicate"
    res = dedup.is_duplicate('This is a test')
    assert res == True, "Same item should be a duplicate"
    res = dedup.is_duplicate('Something completely different')
    assert res == False, "Complete different item should not be a duplicate"
    res = dedup.is_duplicate('Something completely different2')
    assert res == True, "Similar item should be a duplicate"
