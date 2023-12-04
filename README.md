<div align="center">
  <br/>
<h1>ElecPhys</h1>
  
<br/>
<img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white" alt="built with Python3" />
</div>

----------

ElecPhys: A Python package for electrophysiology data analysis. It provides tools for data loading, analysis, conversion, preprocessing, and visualization.


----------
## Table of contents			
   * [Overview](https://github.com/AminAlam/ElecPhys#overview)
   * [Installation](https://github.com/AminAlam/Zam#ElecPhys)
   * [Usage](https://github.com/AminAlam/ElecPhys#usage)

----------
## Overview
<p align="justify">
 ElecPhys is a Python package for electrophysiology data analysis. It provides tools for data loading, analysis, conversion, preprocessing, and visualization.. ElecPhys can convert .RHD fiels to .mat and .npz, and it can analyze the data in time and fourier domain. Please take a look at <a href="https://github.com/AminAlam/ElecPhys/docs/available_analysis">here</a> for the complete list of available analysis methods. 
</p>

----------
## Installation

### Source code
- Clone the repository or download the source code.
- cd into the repository directory.
- Run `python3 setup.py install`

### PyPi
Run `pip3 install ElecPhys` or `pip install ElecPhys`

## Usage
It's possible to use ElecPhys as a command line tool or as a Python module.

### Command Line
To use ELecPhys from command line, you need to use the following pattern:

```console
➜ elecphys COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]
```
Where each COMMNAD can be one of the supported commands such as convert_rhd_to_mat, plot_stft, and ... .
To learn more about the commnads, you can use the following command:
```console
➜ elecphys --help
Usage: main.py COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

  ElecPhys is a Python package for electrophysiology data analysis. It
  provides tools for data loading, conversion, preprocessing, and
  visualization.

Options:
  --help  Show this message and exit.

Commands:
  convert_mat_to_npz            Converts MAT files to NPZ files using MAT...
  convert_rhd_to_mat            Converts RHD files to mat files using RHD...
  dft_numeric_output_from_npz   Computes DFT and saves results as NPZ files
  normalize_npz                 Normalizes NPZ files
  plot_dft                      Plots DFT from NPZ file
  plot_signal                   Plots signals from NPZ file
  plot_stft                     Plots STFT from NPZ file
  stft_numeric_output_from_npz  Computes STFT and saves results as NPZ files
  zscore_normalize_npz          Z-score normalizes NPZ files
```

### Python module

You need to import ElecPhus and use it's modules inside your python code. For example:

```python
import elecphys

# Path to folder containing RHD files
folder_path = "data/rhd_files"
# Path to the output .mat file
output_mat_file = "output.mat"
# Down sample factor
ds_factor = 5
# call rhd to mat conversoin module
elecphys.conversion.convert_rhd_to_mat_matlab(folder_path, output_mat_file, ds_factor)
```
### Analysis methods
<iframe src="./docs/available_analysis.md" width="600" height="400"></iframe>
