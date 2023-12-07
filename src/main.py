import click
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
import conversion
import preprocessing
import fourier_analysis
import visualization
import dimensionality_reduction
from handlers import ErrorHandler
error_handler = ErrorHandler().error_handler

@click.group(chain=True, help="ElecPhys is a Python package for electrophysiology data analysis. It provides tools for data loading, conversion, preprocessing, and visualization.")
@click.pass_context
def cli(ctx):
    pass

### Conversion ###
@cli.command('convert_rhd_to_mat', help='Converts RHD files to mat files using RHD to MAT converter (needs MATLAB installed')
@click.option('--folder_path', '-f', help='Path to folder containing RHD files', required=True, type=os.PathLike)
@click.option('--output_mat_file', '-o', help='Path to output mat file', required=True, type=os.PathLike, default='output.mat', show_default=True)
@click.option('--ds_factor', '-d', help='Downsample factor', required=False, type=int, default=1, show_default=True)
@click.pass_context
@error_handler
def convert_rhd_to_mat(ctx, folder_path, output_mat_file, ds_factor):
    """ Converts RHD files to mat files using RHD to MAT converter written in MATLAB
    input:
        folder_path: path to folder containing RHD files - type: os.PathLike
        output_mat_file: path to output mat file - type: os.PathLike
        ds_factor: downsample factor - type: int
    output:
    """
    Warning('** This command requires MATLAB to be installed on your system.\n')
    print('\n\n--- Converting RHD files to MAT files...')
    conversion.convert_rhd_to_mat(folder_path, output_mat_file, ds_factor)
    print('\n\n--- Conversion complete.')

@cli.command('convert_mat_to_npz', help='Converts MAT files to NPZ files using MAT to NPZ converter')
@click.option('--mat_file', '-m', help='Path to mat file', required=True, type=os.PathLike)
@click.option('--output_npz_folder', '-o', help='Path to output npz folder', required=True, type=os.PathLike, default='output_npz', show_default=True)
@click.option('--notch_filter_freq', '-n', help='Notch filter frequency in Hz', required=False, type=int, default=50, show_default=True)
@click.pass_context
@error_handler
def convert_mat_to_npz(ctx, mat_file, output_npz_folder, notch_filter_freq):
    """ Converts MAT files to NPZ files
    input:
        mat_file: path to mat file - type: os.PathLike
        output_npz_folder: path to output npz folder - type: os.PathLike
        notch_filter_freq: notch filter frequency - type: int
    output:
    """
    
    print('\n\n--- Converting MAT files to NPZ files...')
    conversion.convert_mat_to_npz(mat_file, output_npz_folder, notch_filter_freq)
    print('\n\n--- Conversion complete.')
### Conversion ###


### Preprocessing ###
@cli.command('zscore_normalize_npz', help='Z-score normalizes NPZ files')
@click.option('--input_npz_folder', '-i', help='Path to input npz folder', required=True, type=os.PathLike)
@click.option('--output_npz_folder', '-o', help='Path to output npz folder', required=True, type=os.PathLike, default='output_npz', show_default=True)
@click.pass_context
@error_handler
def zscore_normalize_npz(ctx, input_npz_folder, output_npz_folder):
    """ Z-score normalizes NPZ files
    input:
        input_npz_folder: path to input npz folder - type: os.PathLike
        output_npz_folder: path to output npz folder - type: os.PathLike
    output:
    """
    print('\n\n--- Z-score normalizing NPZ files...')
    preprocessing.zscore_normalize_npz(input_npz_folder, output_npz_folder)
    print('\n\n--- Normalization complete.')


@cli.command('normalize_npz', help='Normalizes NPZ files')
@click.option('--input_npz_folder', '-i', help='Path to input npz folder', required=True, type=os.PathLike)
@click.option('--output_npz_folder', '-o', help='Path to output npz folder', required=True, type=os.PathLike, default='output_npz', show_default=True)
@click.pass_context
@error_handler
def normalize_npz(ctx, input_npz_folder, output_npz_folder):
    """ Normalizes NPZ files
    input:
        input_npz_folder: path to input npz folder - type: os.PathLike
        output_npz_folder: path to output npz folder - type: os.PathLike
    output:
    """
    print('\n\n--- Normalizing NPZ files...')
    preprocessing.normalize_npz(input_npz_folder, output_npz_folder)
    print('\n\n--- Normalization complete.')
### Preprocessing ###


### Fourier Analysis ###
@cli.command('stft_numeric_output_from_npz', help='Computes STFT and saves results as NPZ files')
@click.option('--input_npz_folder', '-i', help='Path to input npz folder', required=True, type=os.PathLike)
@click.option('--output_npz_folder', '-o', help='Path to output npz folder to save STFT results', required=True, type=os.PathLike, show_default=True)
@click.option('--window_size', '-w', help='Window size in seconds', required=True, type=float)
@click.option('--overlap', '-ov', help='Overlap in seconds', required=True, type=float)
@click.option('--window_type', '-wt', help='Window type', required=True, type=str, default='hann', show_default=True)
@click.pass_context
@error_handler
def stft_numeric_output(ctx, input_npz_folder, output_npz_folder, window_size, overlap, window_type):
    """ Computes STFT and saves results as NPZ files
    input:
        input_npz_folder: path to input npz folder - type: os.PathLike
        output_npz_folder: path to output npz folder to save STFT results - type: os.PathLike
        window_size: window size in seconds - type: float
        overlap: overlap in seconds - type: float
        window_type: window type - type: str
    output:
    """
    print('\n\n--- Computing STFT and saving results as NPZ files...')
    fourier_analysis.stft_numeric_output_from_npz(input_npz_folder, output_npz_folder, window_size, overlap, window_type)
    print('\n\n--- STFT computation complete.')

@cli.command('dft_numeric_output_from_npz', help='Computes DFT and saves results as NPZ files')
@click.option('--input_npz_folder', '-i', help='Path to input npz folder', required=True, type=os.PathLike)
@click.option('--output_npz_folder', '-o', help='Path to output npz folder to save DFT results', required=True, type=os.PathLike, show_default=True)
@click.pass_context
@error_handler
def dft_numeric_output(ctx, input_npz_folder, output_npz_folder):
    """ Computes DFT and saves results as NPZ files
    input:
        input_npz_folder: path to input npz folder - type: os.PathLike
        output_npz_folder: path to output npz folder to save DFT results - type: os.PathLike
    output:
    """
    print('\n\n--- Computing DFT and saving results as NPZ files...')
    fourier_analysis.dft_numeric_output_from_npz(input_npz_folder, output_npz_folder)
    print('\n\n--- DFT computation complete.')
### Fourier Analysis ###


### Visualization ###
@cli.command('plot_stft', help='Plots STFT from NPZ file')
@click.option('--input_npz_file', '-i', help='Path to input npz file', required=True, type=os.PathLike)
@click.option('--output_plot_file', '-o', help='Path to output plot file', required=True, type=os.PathLike, default=None, show_default=True)
@click.option('--f_min', '-fmin', help='Minimum frequency to plot in Hz', required=True, type=float, default=None, show_default=True)
@click.option('--f_max', '-fmax', help='Maximum frequency to plot in Hz', required=True, type=float, default=None, show_default=True)
@click.option('--t_min', '-tmin', help='Minimum time to plot in seconds', required=True, type=float, default=None, show_default=True)
@click.option('--t_max', '-tmax', help='Maximum time to plot in seconds', required=True, type=float, default=None, show_default=True)
@click.option('--db_min', '-dbmin', help='Minimum dB to plot', required=True, type=float, default=None, show_default=True)
@click.option('--db_max', '-dbmax', help='Maximum dB to plot', required=True, type=float, default=None, show_default=True)
@click.pass_context
@error_handler
def plot_stft(ctx, input_npz_file, output_plot_file, f_min, f_max, t_min, t_max, db_min, db_max):
    """ Plots STFT from NPZ file
    input:
        input_npz_file: path to input npz file - type: os.PathLike
        output_plot_file: path to output plot file - type: os.PathLike
        f_min: minimum frequency to plot in Hz - type: float
        f_max: maximum frequency to plot in Hz - type: float
        t_min: minimum time to plot in seconds - type: float
        t_max: maximum time to plot in seconds - type: float
        db_min: minimum dB to plot - type: float
        db_max: maximum dB to plot - type: float
    output:
    """
    print('\n\n--- Plotting STFT...')
    visualization.plot_stft(input_npz_file, output_plot_file, f_min, f_max, t_min, t_max, db_min, db_max)
    print('\n\n--- Plotting complete.')


@cli.command('plot_avg_stft', help='Plots average STFT from NPZ files')
@click.option('--input_npz_folder', '-i', help='Path to input npz folder containing STFT NPZ files', required=True, type=os.PathLike)
@click.option('--output_plot_file', '-o', help='Path to output plot file', required=True, type=os.PathLike, default=None, show_default=True)
@click.option('--f_min', '-fmin', help='Minimum frequency to plot in Hz', required=True, type=float, default=None, show_default=True)
@click.option('--f_max', '-fmax', help='Maximum frequency to plot in Hz', required=True, type=float, default=None, show_default=True)
@click.option('--t_min', '-tmin', help='Minimum time to plot in seconds', required=True, type=float, default=None, show_default=True)
@click.option('--t_max', '-tmax', help='Maximum time to plot in seconds', required=True, type=float, default=None, show_default=True)
@click.option('--db_min', '-dbmin', help='Minimum dB to plot', required=True, type=float, default=None, show_default=True)
@click.option('--db_max', '-dbmax', help='Maximum dB to plot', required=True, type=float, default=None, show_default=True)
@click.option('channels_list', '-cl', help='List of channels to plot, if None then all of the channels will be plotted', required=False, type=list, default=None, show_default=True)
@click.pass_context
@error_handler
def plot_avg_stft(ctx, input_npz_folder, output_plot_file, f_min, f_max, t_min, t_max, db_min, db_max, channels_list):
    """ Plots average STFT from NPZ files
    input:
        input_npz_folder: path to input npz folder - type: os.PathLike
        output_plot_file: path to output plot file - type: os.PathLike
        f_min: minimum frequency to plot in Hz - type: float
        f_max: maximum frequency to plot in Hz - type: float
        t_min: minimum time to plot in seconds - type: float
        t_max: maximum time to plot in seconds - type: float
        db_min: minimum dB to plot - type: float
        db_max: maximum dB to plot - type: float
        channels_list: list of channels to plot - type: list
    output:
    """
    print('\n\n--- Plotting average STFT...')
    visualization.plot_avg_stft(input_npz_folder, output_plot_file, f_min, f_max, t_min, t_max, db_min, db_max, channels_list)
    print('\n\n--- Plotting complete.')


@cli.command('plot_signal', help='Plots signals from NPZ file')
@click.option('--input_npz_folder', '-i', help='Path to input npz folder', required=True, type=os.PathLike)
@click.option('--output_plot_file', '-o', help='Path to output plot file', required=True, type=os.PathLike, default=None, show_default=True)
@click.option('--t_min', '-tmin', help='Minimum time to plot in seconds', required=True, type=float, default=None, show_default=True)
@click.option('--t_max', '-tmax', help='Maximum time to plot in seconds', required=True, type=float, default=None, show_default=True)
@click.option('--channels_list', '-cl', help='List of channels to plot, if None then all of the channels will be plotted', required=False, type=list, default=None, show_default=True)
@click.option('--normalize', '-n', help='Normalize signals. If true, each channel will be normalized', required=False, type=bool, default=False, show_default=True)
@click.pass_context
@error_handler
def plot_signal(ctx, input_npz_folder, output_plot_file, t_min, t_max, channels_list, normalize):
    """ Plots signals from NPZ file
    input:
        input_npz_folder: path to input npz folder - type: os.PathLike
        output_plot_file: path to output plot file - type: os.PathLike
        t_min: minimum time to plot in seconds - type: float
        t_max: maximum time to plot in seconds - type: float
        channels_list: list of channels to plot - type: list
        normalize: normalize signals - type: bool
    output:
    """
    print('\n\n--- Plotting signals...')
    visualization.plot_signal(input_npz_folder, output_plot_file, t_min, t_max, channels_list, normalize)
    print('\n\n--- Plotting complete.')


@cli.command('plot_dft', help='Plots DFT from NPZ file')
@click.option('--input_npz_folder', '-i', help='Path to input npz folder', required=True, type=os.PathLike)
@click.option('--output_plot_file', '-o', help='Path to output plot file', required=True, type=os.PathLike, default=None, show_default=True)
@click.option('--f_min', '-fmin', help='Minimum frequency to plot in Hz', required=True, type=float, default=None, show_default=True)
@click.option('--f_max', '-fmax', help='Maximum frequency to plot in Hz', required=True, type=float, default=None, show_default=True)
@click.option('--channels_list', '-cl', help='List of channels to plot, if None then all of the channels will be plotted', required=True, type=list, default=None, show_default=True)
@click.option('--plot_type', '-pt', help='Plot type', required=True, type=str, default='average_of_channels', show_default=True)
@click.option('--conv_window_size', '-cws', help='Convolution window size in seconds', required=True, type=float, default=None, show_default=True)
@click.pass_context
@error_handler
def plot_dft(ctx, input_npz_folder, output_plot_file, f_min, f_max, channels_list, plot_type, conv_window_size):
    """ Plots DFT from NPZ file
    input:
        input_npz_folder: path to input npz folder - type: os.PathLike
        output_plot_file: path to output plot file - type: os.PathLike
        f_min: minimum frequency to plot in Hz - type: float
        f_max: maximum frequency to plot in Hz - type: float
        channels_list: list of channels to plot - type: list
        plot_type: plot type - type: str
        conv_window_size: convolution window size in seconds - type: float
    output:
    """
    print('\n\n--- Plotting DFT...')
    visualization.plot_dft(input_npz_folder, output_plot_file, f_min, f_max, plot_type, channels_list, conv_window_size)
    print('\n\n--- Plotting complete.')
### Visualization ###


### Dimensionality Reduction ###
@cli.command('pca_from_npz', help='Computes PCA from NPZ files')
@click.option('--input_npz_folder', '-i', help='Path to input npz folder', required=True, type=os.PathLike)
@click.option('--output_npz_folder', '-o', help='Path to output npz folder to save PCA results', required=True, type=os.PathLike, show_default=True)
@click.option('--n_components', '-n', help='Number of components to keep after applying the PCA', required=True, type=int, default=None, show_default=True)
@click.option('--matrix_whitenning', '-mw', help='Matrix whitening boolean. If true, the singular values are divided by n_samples', required=True, type=bool, default=False, show_default=True)
@click.option('--channels_list', '-cl', help='List of channels to apply PCA, if None then all of the channels will be applied', required=False, type=list, default=None, show_default=True)
@click.pass_context
@error_handler
def pca_from_npz(ctx, input_npz_folder, output_npz_folder, n_components, matrix_whitenning, channels_list):
    """ Computes PCA from NPZ files
    input:
        input_npz_folder: path to input npz folder - type: os.PathLike
        output_npz_folder: path to output npz folder to save PCA results - type: os.PathLike
        n_components: number of components to keep after applying the PCA - type: int
        matrix_whitenning: matrix whitening boolean. If true, the singular values are divided by n_samples - type: bool
        channels_list: list of channels to apply PCA, if None then all of the channels will be applied - type: list
    output:
    """
    print('\n\n--- Computing PCA and saving results as NPZ files...')
    dimensionality_reduction.pca_from_npz(input_npz_folder, output_npz_folder, n_components, matrix_whitenning, channels_list)
    print('\n\n--- PCA computation complete.')

if __name__ == '__main__':
    cli()
