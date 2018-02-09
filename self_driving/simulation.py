#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import cv2
import numpy as np
import tensorflow as tf
from ml_training.DataHolder import DataHolder
from ml_training.Config import Config
from ml_training.Trainer import Trainer
from ml_training.DFN import DFN
from vision.image_manipulation import binarize_image, grayscale_image
from vision.util import write_img


def simulate_run(folder_path,
                 output_path,
                 mode,
                 trainer,
                 verbose):
    """
    Function to simulate one driving using one of folder images.

    :param folder_path: path to folder containing images
    :type folder_path: str
    :param output_path: path to save the images with the respective probability
    :type output_path: str
    :param mode: image mode
    :type mode: str
    :param trainer: trainer object to run prediction
    :type trainer: ml_training.Trainer
    :param verbose: param to control print
    :type verbose: bool
    """
    if verbose:
        print("Trying to run simulator in images from {} \n".format(folder_path))  # noqa
    for filename in os.listdir(folder_path):
        if verbose:
            print(filename)
        image_path = os.path.join(folder_path, filename)
        image_path_output = os.path.join(output_path, filename)
        image_raw = cv2.imread(image_path)
        image = image2float(image_raw, mode)
        prob = trainer.predict_prob(image)[0]
        commands = ['up', 'down', 'left', 'right']
        commands_prob = []
        for i, com in enumerate(commands):
            commands_prob.append(com + ":{0:.2f}".format(prob[i]))
        write_img(image_raw, commands_prob, image_path_output)


def image2float(img, mode="pure"):
    """
    Change type and shape of the image's array
    according to self.mode.

    :param img: image
    :type img: np.array
    :rtype: np.array
    """
    if mode == "pure":
        img = img.astype(np.float32) / 255
        img = img.reshape((1, img.shape[0] * img.shape[1] * img.shape[2]))
        return img
    else:
        if mode == "green":
            img = img[1]
        elif mode == "bin":
            img = binarize_image(img)
        elif mode == "gray":
            img = grayscale_image(img)
        img = img.astype(np.float32) / 255
        img = img.reshape((1, img.shape[0] * img.shape[1]))
        return img


def main():
    """
    Script to run one simmulation on a trained model.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('img_folder_path',
                        type=str, help='path to image folder')
    parser.add_argument('output_path',
                        type=str, help='path to simulate data to be saved')
    parser.add_argument('-a',
                        '--architecture',
                        type=int,
                        nargs='+',
                        help='sizes for hidden layers and output layer, should end with "4" !, (default=[4])',  # noqa
                        default=[4])
    parser.add_argument('-ac',
                        '--activations',
                        type=str,
                        nargs='+',
                        help='activations: relu, sigmoid, tanh (defaul=None)',
                        default=None)
    parser.add_argument("-m",
                          "--mode",
                          type=str,
                          default="bin",
                          help="mode for data: pure, flip, aug, bin, gray, green (default=pure)")  # noqa
    parser.add_argument("-v",
                        "--verbose",
                        action="store_true",
                        default=False,
                        help="print training results and calculate confusion matrix (default=False)")  # noqa
    args = parser.parse_args()

    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    if args.mode == "bin" or args.mode == "gray" or args.mode == "green":
        channels = 1
    else:
        channels = 3

    activations_dict = {"relu": tf.nn.relu,
                        "sigmoid": tf.nn.sigmoid,
                        "tanh": tf.nn.tanh}

    if args.activations is not None:
        activations = [activations_dict[act] for act in args.activations]
    else:
        activations = args.activations

    config = Config(channels=channels,
                    architecture=args.architecture,
                    activations=activations)

    data = DataHolder(config)
    graph = tf.Graph()
    network = DFN(graph, config)
    trainer = Trainer(graph, config, network, data)
    print("\nSimulating in the {} data\n".format(args.mode))
    print("params:\n{}\n".format(config.get_status()))
    if not os.path.exists("checkpoints"):
        print("===Simmulation of a non trained model===")
    simulate_run(args.img_folder_path,
                 args.output_path,
                 args.mode,
                 trainer,
                 args.verbose)


if __name__ == '__main__':
    main()