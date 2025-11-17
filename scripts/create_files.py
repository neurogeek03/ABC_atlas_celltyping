import argparse
import pathlib
import json
import os
from cell_type_mapper.cli.from_specified_markers import (
    FromSpecifiedMarkersRunner
)

os.environ['NUMEXPR_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'

# Argumet parsing
parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", type=str, required=True)
parser.add_argument("--scratch_dir", type=str, required=True)
parser.add_argument("--nodes_to_drop", type=str, required=False)
parser.add_argument("--query", type=str, required=True)
args = parser.parse_args()

# Paths
input_path = pathlib.Path(args.input_dir)
scratch_path = pathlib.Path(args.scratch_dir)
query_path =  pathlib.Path(args.query)
stem = query_path.stem
print("Using path:", input_path, "for input") 
print("Using path:", scratch_path, "to find the test_set.h5ad and save the output")

baseline_json_output_path = scratch_path / f'{stem}_baseline_json_mapping_output.json'
baseline_csv_output_path = scratch_path / f'{stem}baseline_csv_mapping_output.csv'

test_h5ad_path = scratch_path / "test_set.h5ad"

baseline_marker_path = input_path / 'mouse_markers_230821.json'
baseline_precompute_path = input_path / 'precomputed_stats_ABC_revision_230821.h5'


nodes_to_drop = json.loads(args.nodes_to_drop)

# nodes_to_drop =[('class', 'CS20230722_CLAS_27')]

# config 
baseline_mapping_config = {
    'query_path': str(query_path),
    'extended_result_path': str(baseline_json_output_path),
    'csv_result_path': str(baseline_csv_output_path),
    'tmp_dir': str(scratch_path),
    'max_gb': 10,
    'cloud_safe': False,
    'verbose_stdout': False,
    'type_assignment': {
        'normalization': 'raw',
        'n_processors': 4,
        'chunk_size': 10000,
        'bootstrap_iteration': 100,
        'bootstrap_factor': 0.5,
        'rng_seed': 233211
    },
    'precomputed_stats': {
        'path': str(baseline_precompute_path)
    },
    'query_markers': {
        'serialized_lookup': str(baseline_marker_path)
    },
    'nodes_to_drop': nodes_to_drop,
    'drop_level': 'CCN20230722_SUPT'
}

# running
mapping_runner = FromSpecifiedMarkersRunner(
    args=[],
    input_data=baseline_mapping_config
)

mapping_runner.run()