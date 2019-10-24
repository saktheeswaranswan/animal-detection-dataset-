# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Tests for oid_tfrecord_creation.py."""

import os
import contextlib2
import pandas as pd
import tensorflow as tf

from tf_api.dataset_tools import oid_tfrecord_creation


def create_test_data():
  data = {
      'ImageID': ['i1', 'i1', 'i1', 'i1', 'i2', 'i2'],
      'LabelName': ['a', 'a', 'b', 'b', 'b', 'c'],
      'YMin': [0.3, 0.6, 0.8, 0.1, 0.0, 0.0],
      'XMin': [0.1, 0.3, 0.7, 0.0, 0.1, 0.1],
      'XMax': [0.2, 0.3, 0.8, 0.5, 0.9, 0.9],
      'YMax': [0.3, 0.6, 1, 0.8, 0.8, 0.8],
      'IsOccluded': [0, 1, 1, 0, 0, 0],
      'IsTruncated': [0, 0, 0, 1, 0, 0],
      'IsGroupOf': [0, 0, 0, 0, 0, 1],
      'IsDepiction': [1, 0, 0, 0, 0, 0],
  }
  df = pd.DataFrame(data=data)
  label_map = {'a': 0, 'b': 1, 'c': 2}
  return label_map, df


class TfExampleFromAnnotationsDataFrameTests(tf.test.TestCase):

  def test_simple(self):
    label_map, df = create_test_data()

    tf_example = oid_tfrecord_creation.tf_example_from_annotations_data_frame(
        df[df.ImageID == 'i1'], label_map, 'encoded_image_test')
    self.assertProtoEquals("""
        features {
          feature {
            key: "image/encoded"
            value { bytes_list { value: "encoded_image_test" } } }
          feature {
            key: "image/filename"
            value { bytes_list { value: "i1.jpg" } } }
          feature {
            key: "image/object/bbox/ymin"
            value { float_list { value: [0.3, 0.6, 0.8, 0.1] } } }
          feature {
            key: "image/object/bbox/xmin"
            value { float_list { value: [0.1, 0.3, 0.7, 0.0] } } }
          feature {
            key: "image/object/bbox/ymax"
            value { float_list { value: [0.3, 0.6, 1.0, 0.8] } } }
          feature {
            key: "image/object/bbox/xmax"
            value { float_list { value: [0.2, 0.3, 0.8, 0.5] } } }
          feature {
            key: "image/object/class/label"
            value { int64_list { value: [0, 0, 1, 1] } } }
          feature {
            key: "image/object/class/text"
            value { bytes_list { value: ["a", "a", "b", "b"] } } }
          feature {
            key: "image/source_id"
            value { bytes_list { value: "i1" } } }
          feature {
            key: "image/object/depiction"
            value { int64_list { value: [1, 0, 0, 0] } } }
          feature {
            key: "image/object/group_of"
            value { int64_list { value: [0, 0, 0, 0] } } }
          feature {
            key: "image/object/occluded"
            value { int64_list { value: [0, 1, 1, 0] } } }
          feature {
            key: "image/object/truncated"
            value { int64_list { value: [0, 0, 0, 1] } } } }
    """, tf_example)

  def test_no_attributes(self):
    label_map, df = create_test_data()

    del df['IsDepiction']
    del df['IsGroupOf']
    del df['IsOccluded']
    del df['IsTruncated']

    tf_example = oid_tfrecord_creation.tf_example_from_annotations_data_frame(
        df[df.ImageID == 'i2'], label_map, 'encoded_image_test')
    self.assertProtoEquals("""
        features {
          feature {
            key: "image/encoded"
            value { bytes_list { value: "encoded_image_test" } } }
          feature {
            key: "image/filename"
            value { bytes_list { value: "i2.jpg" } } }
          feature {
            key: "image/object/bbox/ymin"
            value { float_list { value: [0.0, 0.0] } } }
          feature {
            key: "image/object/bbox/xmin"
            value { float_list { value: [0.1, 0.1] } } }
          feature {
            key: "image/object/bbox/ymax"
            value { float_list { value: [0.8, 0.8] } } }
          feature {
            key: "image/object/bbox/xmax"
            value { float_list { value: [0.9, 0.9] } } }
          feature {
            key: "image/object/class/label"
            value { int64_list { value: [1, 2] } } }
          feature {
            key: "image/object/class/text"
            value { bytes_list { value: ["b", "c"] } } }
          feature {
            key: "image/source_id"
           value { bytes_list { value: "i2" } } } }
    """, tf_example)

  def test_label_filtering(self):
    label_map, df = create_test_data()

    label_map = {'a': 0}

    tf_example = oid_tfrecord_creation.tf_example_from_annotations_data_frame(
        df[df.ImageID == 'i1'], label_map, 'encoded_image_test')
    self.assertProtoEquals("""
        features {
          feature {
            key: "image/encoded"
            value { bytes_list { value: "encoded_image_test" } } }
          feature {
            key: "image/filename"
            value { bytes_list { value: "i1.jpg" } } }
          feature {
            key: "image/object/bbox/ymin"
            value { float_list { value: [0.3, 0.6] } } }
          feature {
            key: "image/object/bbox/xmin"
            value { float_list { value: [0.1, 0.3] } } }
          feature {
            key: "image/object/bbox/ymax"
            value { float_list { value: [0.3, 0.6] } } }
          feature {
            key: "image/object/bbox/xmax"
            value { float_list { value: [0.2, 0.3] } } }
          feature {
            key: "image/object/class/label"
            value { int64_list { value: [0, 0] } } }
          feature {
            key: "image/object/class/text"
            value { bytes_list { value: ["a", "a"] } } }
          feature {
            key: "image/source_id"
            value { bytes_list { value: "i1" } } }
          feature {
            key: "image/object/depiction"
            value { int64_list { value: [1, 0] } } }
          feature {
            key: "image/object/group_of"
            value { int64_list { value: [0, 0] } } }
          feature {
            key: "image/object/occluded"
            value { int64_list { value: [0, 1] } } }
          feature {
            key: "image/object/truncated"
            value { int64_list { value: [0, 0] } } } }
    """, tf_example)


class OpenOutputTfrecordsTests(tf.test.TestCase):

  def test_sharded_tfrecord_writes(self):
    with contextlib2.ExitStack() as tf_record_close_stack:
      output_tfrecords = oid_tfrecord_creation.open_sharded_output_tfrecords(
          tf_record_close_stack,
          os.path.join(tf.test.get_temp_dir(), 'test.tfrec'), 10)
      for idx in range(10):
        output_tfrecords[idx].write('test_{}'.format(idx))

    for idx in range(10):
      tf_record_path = '{}-{:05d}-of-00010'.format(
          os.path.join(tf.test.get_temp_dir(), 'test.tfrec'), idx)
      records = list(tf.python_io.tf_record_iterator(tf_record_path))
      self.assertAllEqual(records, ['test_{}'.format(idx)])


if __name__ == '__main__':
  tf.test.main()