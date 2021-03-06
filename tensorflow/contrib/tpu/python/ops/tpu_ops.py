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
# =============================================================================

"""Operations for TPUs."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import platform

from tensorflow.python.framework import ops

if platform.system() != "Windows":
  # pylint: disable=wildcard-import,unused-import,g-import-not-at-top
  from tensorflow.contrib.tpu.ops import gen_tpu_ops
  from tensorflow.contrib.tpu.ops.gen_tpu_ops import *

  from tensorflow.contrib.util import loader
  from tensorflow.python.platform import resource_loader
  # pylint: enable=wildcard-import,unused-import,g-import-not-at-top

  _tpu_ops = loader.load_op_library(
      resource_loader.get_path_to_datafile("_tpu_ops.so"))

  @ops.RegisterGradient("CrossReplicaSum")
  def _cross_replica_sum_grad(op, grad):
    del op  # Unused
    # The gradient of a cross replica sum is also a cross-replica sum.
    return gen_tpu_ops.cross_replica_sum(grad)
else:
  # We have already built the appropriate libraries into the binary via CMake
  # if we have built contrib, so we don't need this
  pass
