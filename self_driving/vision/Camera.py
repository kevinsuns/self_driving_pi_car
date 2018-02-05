import cv2
from image_manipulation import binarize_image, grayscale_image


class Camera(object):
    """
    Class to take pictures.

    :param height_size: camera's image height
    :type height_size: int
    :param width_size: camera's image width
    :type width_size: int
    :param input_cam_device: param to control camera's input
    :type input_cam_device: int
    :param height_param: param to set height on camera
    :type height_param: int
    :param width_param: param to set width on camera
    :type width_param: int
    :param mode: param to control type of image
    :type mode: str
    """
    def __init__(self,
                 width_size=160,
                 height_size=90,
                 input_cam_device=0,
                 height_param=4,
                 width_param=3,
                 mode="pure"):
        self.cam = cv2.VideoCapture(input_cam_device)
        self.cam.set(width_param, width_size)
        self.cam.set(height_param, height_size)
        assert mode == "pure" or mode == "green" or mode == "bin" or mode == "gray" # noqa
        self.mode = mode

    def save_image(self, path, img):
        """
        Save image in path "path".

        :param path: path to save image
        :type path: str
        :param img: image
        :type img: np.ndarray
        """
        cv2.imwrite(path, img)

    def take_picture(self):
        """
        Take picture according to the mode param.
        :rtype: np.ndarray
        """
        if self.mode == "pure":
            return self.take_picture_rgb()
        elif self.mode == "green":
            return self.take_picture_green()
        elif self.mode == "bin":
            return self.take_picture_bin()
        elif self.mode == "gray":
            return self.take_picture_gray()

    def take_picture_rgb(self):
        """
        Take picture with no transformation.

        :rtype: np.ndarray
        """
        _, img = self.cam.read()
        return img

    def take_picture_gray(self):
        """
        Take grayscale picture.

        :rtype: np.ndarray
        """
        _, img = self.cam.read()
        img = grayscale_image(img)
        return img

    def take_picture_bin(self):
        """
        Take binarized picture.

        :rtype: np.ndarray
        """
        _, img = self.cam.read()
        img = binarize_image(img)
        return img

    def take_picture_green(self):
        """
        Take picture with only the green channel.

        :rtype: np.ndarray
        """
        _, img = self.cam.read()
        return img[1]
