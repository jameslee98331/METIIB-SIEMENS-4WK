import numpy as np
from collections import namedtuple
from siecon_cv_metiib import imgproc


class TestImgProc:

    def test_centroid(self):
        test_kp_coord = [(1, 2), (2, 3), (4, 5), (3, 2)]

        assert imgproc.centroid(test_kp_coord) == (2.5, 3)

    def test_mask(self):
        test_img = np.asarray([[(1,2,3),(2,3,4),(3,4,5),(4,5,6),(1,2,3)],
                               [(2,3,4),(5,6,7),(1,2,3),(1,2,3),(4,5,6)],
                               [(4,5,6),(7,8,9),(5,6,7),(7,6,5),(1,2,3)],
                               [(3,4,5),(7,8,5),(1,2,4),(4,5,6),(5,6,7)],
                               [(8,6,7),(9,0,0),(8,6,5),(1,3,4),(1,2,3)]])
        test_start = (1,1)
        test_finish = (3,3)
        rect = namedtuple('rect', 'start, finish')
        mask_rect = rect(test_start, test_finish)

        test_mask = imgproc.mask(test_img, mask_rect)

        assert np.array_equal(test_mask, [[0,0,0,0,0],
                                          [0,255,255,255,0],
                                          [0,255,255,255,0],
                                          [0,255,255,255,0],
                                          [0,0,0,0,0]])


    # TODO: Create new y_centroid_rev function in offset.py when location of reference is known
    # def test_y_centroid_rev(self):
    #     test_centroid = (4, 3)
    #     test_img = np.asarray([[(1,2,3),(2,3,4),(3,4,5),(4,5,6),(1,2,3)],
    #                            [(2,3,4),(5,6,7),(1,2,3),(1,2,3),(4,5,6)],
    #                            [(4,5,6),(7,8,9),(5,6,7),(7,6,5),(1,2,3)],
    #                            [(3,4,5),(7,8,5),(1,2,4),(4,5,6),(5,6,7)],
    #                            [(8,6,7),(9,0,0),(8,6,5),(1,3,4),(1,2,3)]])
    #
    #     assert offset.y_centroid_rev(test_img, test_centroid) == 1
