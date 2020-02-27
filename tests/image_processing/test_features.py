import numpy as np
from siecon_cv_metiib.image_processing import features


class TestFeatures:

    def test_mask(self):
        test_img = np.asarray([[(1,2,3),(2,3,4),(3,4,5),(4,5,6),(1,2,3)],
                               [(2,3,4),(5,6,7),(1,2,3),(1,2,3),(4,5,6)],
                               [(4,5,6),(7,8,9),(5,6,7),(7,6,5),(1,2,3)],
                               [(3,4,5),(7,8,5),(1,2,4),(4,5,6),(5,6,7)],
                               [(8,6,7),(9,0,0),(8,6,5),(1,3,4),(1,2,3)]])
        test_start = (1,1)
        test_finish = (3,3)
        test_mask = features.mask(test_img, test_start, test_finish)

        assert np.array_equal(test_mask, [[0,0,0,0,0],
                                          [0,255,255,255,0],
                                          [0,255,255,255,0],
                                          [0,255,255,255,0],
                                          [0,0,0,0,0]])
