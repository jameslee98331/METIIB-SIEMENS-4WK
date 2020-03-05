import numpy as np
from collections import namedtuple
from siecon_cv_metiib import imgproc


class TestImgProc:

    def test_draw_rect(self):
        test_start = (2, 2)
        test_finish = (5, 5)

        test_rect = imgproc.draw_rect(test_start, test_finish)

        assert test_rect.start == (2, 2)
        assert test_rect.finish == (5, 5)

    def test_crop(self):
        test_img = np.asarray([[(1,2,3),(2,3,4),(3,4,5),(4,5,6),(1,2,3)],
                               [(2,3,4),(5,6,7),(1,2,3),(1,2,3),(4,5,6)],
                               [(4,5,6),(7,8,9),(5,6,7),(7,6,5),(1,2,3)],
                               [(3,4,5),(7,8,5),(1,2,4),(4,5,6),(5,6,7)],
                               [(8,6,7),(9,0,0),(8,6,5),(1,3,4),(1,2,3)]])
        test_start = (2, 2)
        test_finish = (4, 4)
        test_rect = namedtuple('rect', 'start, finish')
        test_corner = test_rect(test_start, test_finish)

        assert np.array_equal(imgproc.crop(test_img, test_corner), np.asarray([[(5,6,7),(7,6,5)],
                                                                               [(1,2,4),(4,5,6)]]))

    def test_draw_mask(self):
        test_img = np.asarray([[(1,2,3),(2,3,4),(3,4,5),(4,5,6),(1,2,3)],
                               [(2,3,4),(5,6,7),(1,2,3),(1,2,3),(4,5,6)],
                               [(4,5,6),(7,8,9),(5,6,7),(7,6,5),(1,2,3)],
                               [(3,4,5),(7,8,5),(1,2,4),(4,5,6),(5,6,7)],
                               [(8,6,7),(9,0,0),(8,6,5),(1,3,4),(1,2,3)]])
        test_start = (1,1)
        test_finish = (3,3)
        rect = namedtuple('rect', 'start, finish')
        mask_rect = rect(test_start, test_finish)

        test_mask = imgproc.draw_mask(test_img, mask_rect)

        assert np.array_equal(test_mask, [[0,0,0,0,0],
                                          [0,255,255,255,0],
                                          [0,255,255,255,0],
                                          [0,255,255,255,0],
                                          [0,0,0,0,0]])

    def test_centroid(self):
        test_kp_coord = [(1, 2), (2, 3), (4, 5), (3, 2)]

        assert imgproc.centroid(test_kp_coord) == (2.5, 3)

    def test_find_scale(self):
        test_loc = [(5, 10), (10, 10), (5, 20), (10, 20)]
        test_col_const = 2.5
        test_row_const = 4

        assert imgproc.find_scale(test_loc, test_col_const, test_row_const) == 2.25
