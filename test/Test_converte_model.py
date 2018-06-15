#!/usr/bin/env python
# coding: utf-8
import gc
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
# from nose.tools import *
import sys
sys.path.append('./')

from imagedt.converters import caffe_tfmodel
from imagedt.converters import caffe_coreml
from imagedt.converters import tfmodel_lite
from imagedt.decorator import time_cost

class Test_Model_Converte(object):
    def __init__(self):
        super(Test_Model_Converte, self).__init__()

    @time_cost
    def caffe_tfmodel_convert(self, proto_def_path, caffemodel_path, output_model_name='freeze_graph_model.pb'):
        caffe_tfmodel.convert(proto_def_path, caffemodel_path)

    def test_caffe_tfmodel_convert(self):
        proto_def_path = '/data/models/erroe_detect/deploy.prototxt'
        caffemodel_path = '/data/models/erroe_detect/resnet50_snapshot_iter_4000.caffemodel'
        self.caffe_tfmodel_convert(proto_def_path, caffemodel_path)

    @time_cost
    def caffe_coreml_convert(self, model_path, prototxt_path, label_path):
        caffe_coreml.convert(model_path, prototxt_path, label_path, red=-123, green=-117, blue=-104, 
                scale=1.0, bgr=True, output_model_name='sku_cls_model_noise.mlmodel')

    def test_caffe_coreml_convert(self):
        prototxt_path = '/data/models/classify/liby_0531_resnet50/deploy.prototxt'
        model_path = '/data/models/classify/liby_0531_resnet50/resnet50_snapshot_iter_100000.caffemodel'
        label_path = '/data/models/classify/liby_0531_resnet50/sku_labels.txt'
        self.caffe_coreml_convert(model_path, prototxt_path, label_path)

    def tfmodel_lite_convert(self, graph_def_file, output_file):
        tfmodel_lite.convert(graph_def_file, output_file, output_format='TFLITE', inference_type='FLOAT', inference_input_type='FLOAT',
            input_array='data', input_shape='1,224,224,3', output_arrays='softmax')

    @time_cost
    def test_tfmodel_lite_convert(self):
        # TODO fix bug: pipeline excu program
        graph_def_file = '/data/models/erroe_detect/freeze_graph_model.pb'
        output_file = '/data/models/erroe_detect/py_sku_classify.tflite'
        self.tfmodel_lite_convert(graph_def_file, output_file)


if __name__ == '__main__':
    Converte_init = Test_Model_Converte()
    Converte_init.test_caffe_coreml_convert()
    Converte_init.test_caffe_tfmodel_convert()
    Converte_init.test_tfmodel_lite_convert()
