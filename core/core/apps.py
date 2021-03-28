import os
import tensorflow as tf
from django.apps import AppConfig
from django.conf import settings
from django.core.cache import cache
from keras.models import load_model
from tensorflow.python.keras.losses import CategoricalCrossentropy
import numpy as np
from keras.preprocessing import image


class ModelAppConfig(AppConfig):
    name = "coin_model"
    model_path = os.path.join(settings.MODEL, "model_weights.h5")
    classes = ["10_coin", "15_coin", "1_coin", "20_coin", "2_coin", "3_coin", "5_coin"]
    image_size = [224, 224]
    cache_name = "model_cache"

    model_cache = cache.get(cache_name)

    @classmethod
    def _load_model(cls):
        model = load_model(cls.model_path)
        model.compile(
            optimizer=tf.keras.optimizers.Adam(),
            loss=CategoricalCrossentropy(),
            metrics=["accuracy"],
        )
        cache.set(cls.cache_name, model, None)
        return model

    @classmethod
    def make_image_prediction(cls, image_path):
        model = cache.get(cls.cache_name)
        if model is None:
            model = cls._load_model()
        img = image.load_img(image_path, target_size=cls.image_size)
        img = np.expand_dims(img, axis=0)
        classes = np.array(cls.classes)
        prediction = classes[model.predict(img)[0].astype(np.bool)][0]
        return prediction

    # GRAPH = tf.Graph()
    #
    # @classmethod
    # def make_image_prediction(cls, image_path):
    #     with cls.GRAPH.as_default():
    #         model = load_model(cls.model_path)
    #         model.compile(
    #             optimizer=tf.keras.optimizers.Adam(),
    #             loss=CategoricalCrossentropy(),
    #             metrics=["accuracy"],
    #         )
    #         img = image.load_img(image_path, target_size=cls.image_size)
    #         img = np.expand_dims(img, axis=0)
    #         classes = np.array(cls.classes)
    #         prediction = classes[model.predict(img)[0].astype(np.bool)][0]
    #         return prediction
