from siecon_cv_metiib import file_handling


class TestFileHandling:

    def test_dir_empty(self):
        # TODO: use tmpdir in pytest to test the first two cases
        file_path = 'HAS IMAGE'
        assert file_handling.img_exists(file_path) == False

        file_path = 'EMPTY DIRECTORY'
        assert file_handling.img_exists(file_path) == True

        file_path = 'dummy_directory//fake_image.jpg'
        assert file_handling.img_exists(file_path) == True
