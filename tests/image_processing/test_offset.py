from siecon_cv_metiib.image_processing import offset

class TestOffset:

    def test_centroid(self):
        test_kp_coord = [(1,2), (2,3), (4,5), (3,2)]

        assert offset.centroid(test_kp_coord) == (2.5, 3)
