class Path(object):
    @staticmethod
    def db_dir(database):

        # folder that contains class labels
        root_dir = '.\\data\\UCF-101_1'

        # Save preprocess data into output_dir
        output_dir = '.\\data\\var\\ucf101'

        return root_dir, output_dir


    @staticmethod
    def model_dir():
        return '/path/to/Models/c3d-pretrained.pth'