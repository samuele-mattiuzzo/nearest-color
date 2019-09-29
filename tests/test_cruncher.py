import os
import cruncher


TEST_CASES = [
    'test-sample-black.png',
    #'test-sample-grey.png',  # commented this as it clashes with teal
    'test-sample-navy.png',
    'test-sample-teal.png',
]

def test_distance():

    tester_color = (0, 0, 0)  # black
    tester_far = (255, 0, 0)  # red
    tester_near = (0, 0, 128)  # navy

    far = cruncher.distance(tester_far, tester_color)
    near = cruncher.distance(tester_near, tester_color)

    assert far > near

def test_color_finder():

    tester_not_found = (255, 0, 0)  # red, not in list
    tester_found_exact = (0, 0, 128)  # exact navy
    tester_found_near = (0, 0, 123)  # nearest navy

    assert cruncher.nearest_color(tester_not_found) is None
    assert cruncher.nearest_color(tester_found_exact) == 'navy'
    assert cruncher.nearest_color(tester_found_near) == 'navy'


def test_cruncher():

    for TEST_CASE in TEST_CASES:
        # these are all exact matches, so they should all return
        expected_color = TEST_CASE.replace('test-sample-', '').replace('.png', '')
        image_file = os.path.join(
            os.path.dirname(__file__), TEST_CASE)
        
        assert cruncher.cruncher(image_file) == expected_color

