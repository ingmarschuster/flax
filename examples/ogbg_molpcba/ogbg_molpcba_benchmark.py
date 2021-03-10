# Copyright 2021 The Flax Authors.
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

"""Benchmark for the ogbg_molpcba example."""

import time

from absl.testing import absltest
import train
from configs import default
from flax.testing import Benchmark
import jax
import numpy as np

# Parse absl flags test_srcdir and test_tmpdir.
jax.config.parse_flags_with_absl()


class OgbgMolpcbaBenchmark(Benchmark):
  """Benchmarks for the ogbg_molpcba Flax example."""

  def test_cpu(self):
    """Run full training for ogbg_molpcba CPU training."""
    workdir = self.get_tmp_model_dir()
    config = default.get_config()

    start_time = time.time()
    train.train_and_evaluate(config=config, workdir=workdir)
    benchmark_time = time.time() - start_time

    summaries = self.read_summaries(workdir)

    # Summaries contain all the information necessary for
    # the regression metrics.
    wall_time, _, test_accuracy = zip(*summaries['test_accuracy'])
    wall_time = np.array(wall_time)
    sec_per_epoch = np.mean(wall_time[1:] - wall_time[:-1])
    end_test_accuracy = test_accuracy[-1]

    _, _, test_aps = zip(*summaries['test_average_precision'])
    end_test_average_precision = test_aps[-1]

    _, _, validation_accuracy = zip(*summaries['validation_accuracy'])
    end_validation_accuracy = validation_accuracy[-1]

    _, _, validation_aps = zip(*summaries['validation_average_precision'])
    end_validation_average_precision = validation_aps[-1]

    # Use the reporting API to report single or multiple metrics/extras.
    self.report_wall_time(benchmark_time)
    self.report_metrics({
        'sec_per_epoch': sec_per_epoch,
        'test_accuracy': end_test_accuracy,
        'test_average_precision': end_test_average_precision,
        'validation_accuracy': end_validation_accuracy,
        'validation_average_precision': end_validation_average_precision,
    })
    self.report_extras({
        'model_name': 'Graph Network',
        'description': 'CPU test for ogbg_molpcba.',
        'implementation': 'linen',
    })


if __name__ == '__main__':
  absltest.main()