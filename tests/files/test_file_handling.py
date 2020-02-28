import file_handling


class TestFileHandling:

    def test_dir_empty(tmpdir):
        file_handling.dir_empty(tmpdir)
        pass

    def test_first_img(tmpdir):
        file_handling.first_img(tmpdir)
        pass

