import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import shutil
import unittest
import elecphys.conversion as conversion
import elecphys.preprocessing as preprocessing
import elecphys.fourier_analysis as fourier_analysis
import elecphys.visualization as visualization
import elecphys.data_io as data_io

class TestCases_0_autopep8(unittest.TestCase):
    def test_1_autopep8(self):
        elecphys_path = os.path.join(os.path.dirname(__file__), '..', 'elecphys')
        os.system(f'autopep8 --in-place -a -a -a -a --recursive --max-line-length 128 "{elecphys_path}" --exclude "{os.path.join(elecphys_path, "matlab_scripts")}" --verbose')


class TestCases_0_conversion(unittest.TestCase):
    def test_1_rhd_to_mat(self):
        if not MATLAB_TEST:
            self.assertTrue(True)
            return
        folder_path = os.path.join(os.path.dirname(__file__), 'data', 'rhd')
        output_mat_file = os.path.join(
            os.path.dirname(__file__), 'data', 'mat', 'sample.mat')
        for ds_factor in [1, 20]:
            if os.path.exists(output_mat_file):
                os.remove(output_mat_file)
            conversion.convert_rhd_to_mat(
                folder_path, output_mat_file, ds_factor)
            self.assertTrue(os.path.exists(output_mat_file))

        os.remove(output_mat_file)
        command_prompt = f'python3 -m elecphys.main convert_rhd_to_mat --folder_path {folder_path} --output_mat_file {output_mat_file} --ds_factor {ds_factor}'
        for _ in range(2):
            os.system(command_prompt)
        self.assertTrue(os.path.exists(output_mat_file))

    def test_2_mat_to_npz(self):
        mat_file = os.path.join(
            os.path.dirname(__file__),
            'data',
            'mat',
            'sample.mat')
        output_npz_folder = os.path.join(
            os.path.dirname(__file__), 'data', 'npz')
        for notch_filter_freq in [0, 50, 60]:
            if os.path.exists(output_npz_folder):
                shutil.rmtree(output_npz_folder)
            conversion.convert_mat_to_npz(
                mat_file, output_npz_folder, notch_filter_freq)
            self.assertTrue(os.path.exists(output_npz_folder))

        shutil.rmtree(output_npz_folder)
        command_prompt = f'python3 -m elecphys.main convert_mat_to_npz --mat_file {mat_file} --output_npz_folder {output_npz_folder} --notch_filter_freq {notch_filter_freq}'
        for _ in range(2):
            os.system(command_prompt)
        self.assertTrue(os.path.exists(output_npz_folder))


class TestCases_1_preprocessing(unittest.TestCase):
    def test_apply_notch(self):
        npz_files_folder = os.path.join(
            os.path.dirname(__file__), 'data', 'npz')
        npz_files = os.listdir(npz_files_folder)
        npz_file = npz_files[0]
        _signal_chan, fs = data_io.load_npz(
            os.path.join(npz_files_folder, npz_file))
        output = preprocessing.apply_notch(
            _signal_chan, {'Q': 60, 'fs': fs, 'f0': 50})
        self.assertTrue(output.shape == _signal_chan.shape)

    def test_zscore_normalize_npz(self):
        npz_files_folder = os.path.join(
            os.path.dirname(__file__), 'data', 'npz')
        output_npz_folder = os.path.join(
            os.path.dirname(__file__), 'data', 'npz_zscore')
        if os.path.exists(output_npz_folder):
            shutil.rmtree(output_npz_folder)
        preprocessing.zscore_normalize_npz(npz_files_folder, output_npz_folder)
        self.assertTrue(os.path.exists(output_npz_folder))

        shutil.rmtree(output_npz_folder)
        command_prompt = f'python3 -m elecphys.main zscore_normalize_npz --input_npz_folder {npz_files_folder} --output_npz_folder {output_npz_folder}'
        for _ in range(2):
            os.system(command_prompt)
        self.assertTrue(os.path.exists(output_npz_folder))

    def test_normalize_npz(self):
        npz_files_folder = os.path.join(
            os.path.dirname(__file__), 'data', 'npz')
        output_npz_folder = os.path.join(
            os.path.dirname(__file__), 'data', 'npz_normalized')
        if os.path.exists(output_npz_folder):
            shutil.rmtree(output_npz_folder)
        preprocessing.normalize_npz(npz_files_folder, output_npz_folder)
        self.assertTrue(os.path.exists(output_npz_folder))

        shutil.rmtree(output_npz_folder)
        command_prompt = f'python3 -m elecphys.main normalize_npz --input_npz_folder {npz_files_folder} --output_npz_folder {output_npz_folder}'
        for _ in range(2):
            os.system(command_prompt)
        self.assertTrue(os.path.exists(output_npz_folder))

    def test_re_reference_npz(self):
        npz_files_folder = os.path.join(
            os.path.dirname(__file__), 'data', 'npz')
        output_npz_folder = os.path.join(
            os.path.dirname(__file__), 'data', 'npz_avg_reref')
        for ignore_channels in [[1, 2], "[1,4,6]", None]:
            for rr_channel in [1, 4]:
                if os.path.exists(output_npz_folder):
                    shutil.rmtree(output_npz_folder)
                preprocessing.re_reference_npz(
                    npz_files_folder, output_npz_folder, ignore_channels, rr_channel)
                self.assertTrue(os.path.exists(output_npz_folder))

                shutil.rmtree(output_npz_folder)
                command_prompt = f'python3 -m elecphys.main re_reference_npz --input_npz_folder {npz_files_folder} --output_npz_folder {output_npz_folder} --ignore_channels "{ignore_channels}" --rr_channel {rr_channel}'
                for _ in range(2):
                    os.system(command_prompt)
                self.assertTrue(os.path.exists(output_npz_folder))
        shutil.rmtree(output_npz_folder)
        command_prompt = f'python3 -m elecphys.main re_reference_npz --input_npz_folder {npz_files_folder} --output_npz_folder {output_npz_folder}'
        for _ in range(2):
            os.system(command_prompt)
        self.assertTrue(os.path.exists(output_npz_folder))


class TestCases_2_fourier_analysis(unittest.TestCase):
    def test_stft_numeric_output_from_npz(self):
        npz_files_folder = os.path.join(
            os.path.dirname(__file__), 'data', 'npz')
        output_npz_folder = os.path.join(
            os.path.dirname(__file__), 'data', 'npz_stft')
        if os.path.exists(output_npz_folder):
            shutil.rmtree(output_npz_folder)
        window_size = 1
        overlap = 0.5
        for window_type in ['hann', 'kaiser 5']:
            fourier_analysis.stft_numeric_output_from_npz(
                npz_files_folder, output_npz_folder, window_size, overlap, window_type)
            self.assertTrue(os.path.exists(output_npz_folder))

        shutil.rmtree(output_npz_folder)
        command_prompt = f'python3 -m elecphys.main stft_numeric_output_from_npz --input_npz_folder "{npz_files_folder}" --output_npz_folder {output_npz_folder} --window_size {window_size} --overlap {overlap} --window_type "{window_type}"'
        for _ in range(2):
            os.system(command_prompt)
        self.assertTrue(os.path.exists(output_npz_folder))

    def test_dft_numeric_output_from_npz(self):
        npz_files_folder = os.path.join(
            os.path.dirname(__file__), 'data', 'npz')
        output_npz_folder = os.path.join(
            os.path.dirname(__file__), 'data', 'npz_dft')
        if os.path.exists(output_npz_folder):
            shutil.rmtree(output_npz_folder)
        fourier_analysis.dft_numeric_output_from_npz(
            npz_files_folder, output_npz_folder)
        self.assertTrue(os.path.exists(output_npz_folder))

        shutil.rmtree(output_npz_folder)
        command_prompt = f'python3 -m elecphys.main dft_numeric_output_from_npz --input_npz_folder "{npz_files_folder}" --output_npz_folder {output_npz_folder}'
        for _ in range(2):
            os.system(command_prompt)
        self.assertTrue(os.path.exists(output_npz_folder))

    def test_frequency_filtering(self):
        filter_order = 2
        for filter_args in [{'filter_type': 'LPF', 'freq_cutoff': 100}, {
                'filter_type': 'HPF', 'freq_cutoff': 100}, {'filter_type': 'BPF', 'freq_cutoff': [50, 100]}]:
            filter_args['filter_order'] = filter_order
            npz_files_folder = os.path.join(
                os.path.dirname(__file__), 'data', 'npz')
            output_npz_folder = os.path.join(
                os.path.dirname(__file__), 'data', 'npz_filtered')
            if os.path.exists(output_npz_folder):
                shutil.rmtree(output_npz_folder)

            fourier_analysis.butterworth_filtering_from_npz(
                npz_files_folder, output_npz_folder, filter_args)
            self.assertTrue(os.path.exists(output_npz_folder))

            shutil.rmtree(output_npz_folder)
            command_prompt = f'python3 -m elecphys.main frequncy_domain_filter --input_npz_folder "{npz_files_folder}" --output_npz_folder {output_npz_folder} --filter_type {filter_args["filter_type"]} --filter_order {filter_args["filter_order"]} --freq_cutoff "{filter_args["freq_cutoff"]}"'
            for _ in range(2):
                os.system(command_prompt)
            self.assertTrue(os.path.exists(output_npz_folder))

    def test_freq_bands_power_over_time(self):
        npz_files_folder = os.path.join(
            os.path.dirname(__file__), 'data', 'npz')
        output_csv_file = os.path.join(
            os.path.dirname(__file__), 'data', 'csv', 'test.csv')
        if os.path.exists(output_csv_file):
            os.remove(output_csv_file)
        output_plot_file = os.path.join(
            os.path.dirname(__file__), 'data', 'plots', 'power_over_time.png')
        
        for freq_bands in [([10, 20]), ([0, 4], [44, 80])]:
            for channels_list in [None, [1,2,3,23]]:
                for ignore_channels in [None, [4,5,6,11,12]]:
                    for plot_type in ['avg', 'all']:
                        for t_min in [None, 10]:
                            for t_max in [None, 20]:
                                fourier_analysis.freq_bands_power_over_time(npz_files_folder, freq_bands=freq_bands, channels_list=channels_list, ignore_channels=ignore_channels, output_csv_file=output_csv_file, output_plot_file=output_plot_file, plot_type=plot_type, t_min=t_min, t_max=t_max)
        t_min = 10
        t_max = 20
        freq_bands = '[[44,80]'
        command_prompt = f'python3 -m elecphys.main freq_bands_power_over_time --input_npz_folder {npz_files_folder} --output_csv_file {output_csv_file} --output_plot_file {output_plot_file} --freq_bands "{freq_bands}" --channels_list "{channels_list}" --ignore_channels "{ignore_channels}" --plot_type {plot_type} --t_min {t_min} --t_max {t_max}'
        for _ in range(2):
            os.system(command_prompt)

    def test_cfc_from_npz(self):
        return
        npz_files_folder = os.path.join(
            os.path.dirname(__file__), 'data', 'npz')
        output_npz_folder = os.path.join(
            os.path.dirname(__file__), 'data', 'npz_cfc')
        if os.path.exists(output_npz_folder):
            shutil.rmtree(output_npz_folder)
        freq_phase = list(range(2, 9))
        freq_amp = list(range(35, 46))
        fourier_analysis.calc_cfc_from_npz(
            npz_files_folder, output_npz_folder, freq_amp, freq_phase)
        self.assertTrue(os.path.exists(output_npz_folder))


class TestCases_3_visualization(unittest.TestCase):
    def test_plot_stft(self):
        npz_files_folder = os.path.join(
            os.path.dirname(__file__), 'data', 'npz_stft')
        npz_files = os.listdir(npz_files_folder)
        npz_file = npz_files[0]
        output_plot_file = os.path.join(os.path.dirname(
            __file__), 'data', 'plots', 'stft_plot.png')

        f_min = None
        f_max = None
        t_min = None
        t_max = None
        db_min = None
        db_max = None

        for f_min in [None, 50]:
            for f_max in [None, 200]:
                for t_min in [None, 2]:
                    for t_max in [None, 10]:
                        for db_min in [None, -50]:
                            for db_max in [None, 50]:
                                if os.path.exists(output_plot_file):
                                    os.remove(output_plot_file)
                                visualization.plot_stft_from_npz(
                                    os.path.join(
                                        npz_files_folder,
                                        npz_file),
                                    output_plot_file,
                                    f_min,
                                    f_max,
                                    t_min,
                                    t_max,
                                    db_min,
                                    db_max)
                                self.assertTrue(
                                    os.path.exists(output_plot_file))

        os.remove(output_plot_file)
        command_prompt = f'python3 -m elecphys.main plot_stft --input_npz_file "{os.path.join(npz_files_folder, npz_file)}" --output_plot_file {output_plot_file} --f_min {f_min} --f_max {f_max} --t_min {t_min} --t_max {t_max} --db_min {db_min} --db_max {db_max}'
        for _ in range(2):
            os.system(command_prompt)
        self.assertTrue(os.path.exists(output_plot_file))

    def test_plot_avg_stft(self):
        npz_files_folder = os.path.join(
            os.path.dirname(__file__), 'data', 'npz_stft')
        output_plot_file = os.path.join(os.path.dirname(
            __file__), 'data', 'plots', 'avg_stft_plot.png')

        f_min = None
        f_max = None
        t_min = None
        t_max = None
        db_min = None
        db_max = None
        for channels_list in [[1, 2, 3, 4, 5, 6, 7, 12, 15], None]:
            for f_min in [None, 0]:
                for f_max in [None, 200]:
                    for t_min in [None, 2]:
                        for t_max in [None, 10]:
                            for db_min in [None, -50]:
                                for db_max in [None, 50]:
                                    if os.path.exists(output_plot_file):
                                        os.remove(output_plot_file)
                                    visualization.plot_avg_stft_from_npz(
                                        npz_files_folder,
                                        output_plot_file,
                                        f_min,
                                        f_max,
                                        t_min,
                                        t_max,
                                        db_min,
                                        db_max,
                                        channels_list)
                                    self.assertTrue(
                                        os.path.exists(output_plot_file))

        os.remove(output_plot_file)
        command_prompt = f'python3 -m elecphys.main plot_avg_stft --input_npz_folder "{npz_files_folder}" --output_plot_file {output_plot_file} --f_min {f_min} --f_max {f_max} --t_min {t_min} --t_max {t_max} --db_min {db_min} --db_max {db_max} --channels_list "{[1, 2, 3, 4, 5, 6, 7, 12, 15]}"'
        for _ in range(2):
            os.system(command_prompt)
        self.assertTrue(os.path.exists(output_plot_file))

    def test_plot_signal(self):
        npz_folder_path = os.path.join(
            os.path.dirname(__file__), 'data', 'npz')
        output_plot_file = os.path.join(os.path.dirname(
            __file__), 'data', 'plots', 'signal_plot.png')
        t_min = None
        t_max = None
        for channels_list in [None, [1, 2, 3, 4, 5, 6, 7, 12, 15]]:
            if os.path.exists(output_plot_file):
                os.remove(output_plot_file)
            visualization.plot_signals_from_npz(
                npz_folder_path, output_plot_file, t_min, t_max, channels_list)
            self.assertTrue(os.path.exists(output_plot_file))

        os.remove(output_plot_file)
        command_prompt = f'python3 -m elecphys.main plot_signal --input_npz_folder "{npz_folder_path}" --output_plot_file "{output_plot_file}"'
        for _ in range(2):
            os.system(command_prompt)
        self.assertTrue(os.path.exists(output_plot_file))

        os.remove(output_plot_file)
        command_prompt = f'python3 -m elecphys.main plot_signal --input_npz_folder "{npz_folder_path}" --output_plot_file {output_plot_file} --channels_list "{[1, 2, 3, 4, 5, 6, 7, 12, 15]}"'
        for _ in range(2):
            os.system(command_prompt)
        self.assertTrue(os.path.exists(output_plot_file))

        re_reference = True
        for channels_list, ignore_channels in zip(
                [[1, 2, 3, 4, 5, 6, 7, 12, 10, 21, 15], [1, 2, 3, 4, 5]], [[1, 5], [5]]):
            os.remove(output_plot_file)
            command_prompt = f'python3 -m elecphys.main plot_signal --input_npz_folder "{npz_folder_path}" --output_plot_file {output_plot_file} --channels_list "{channels_list}" --ignore_channels "{ignore_channels}" --re_reference {re_reference}'
            for _ in range(2):
                os.system(command_prompt)
            self.assertTrue(os.path.exists(output_plot_file))

        os.remove(output_plot_file)
        command_prompt = f'python3 -m elecphys.main plot_signal --input_npz_folder "{npz_folder_path}" --output_plot_file {output_plot_file} --re_reference {re_reference}'
        for _ in range(2):
            os.system(command_prompt)
        self.assertTrue(os.path.exists(output_plot_file))

        rr_channel = 2

        os.remove(output_plot_file)
        command_prompt = f'python3 -m elecphys.main plot_signal --input_npz_folder "{npz_folder_path}" --output_plot_file {output_plot_file} --re_reference {re_reference} --rr_channel {rr_channel}'
        for _ in range(2):
            os.system(command_prompt)
        self.assertTrue(os.path.exists(output_plot_file))

        for channels_list, ignore_channels in zip(
                [[1, 2, 3, 4, 5, 6, 7, 12, 15], [1, 2, 3, 4, 5]], [[1, 5], [5]]):
            os.remove(output_plot_file)
            command_prompt = f'python3 -m elecphys.main plot_signal --input_npz_folder "{npz_folder_path}" --output_plot_file {output_plot_file} --channels_list "{channels_list}" --ignore_channels "{ignore_channels}" --re_reference {re_reference} --rr_channel {rr_channel}'
            for _ in range(2):
                os.system(command_prompt)
            self.assertTrue(os.path.exists(output_plot_file))

    def test_plot_dft(self):
        npz_files_folder = os.path.join(
            os.path.dirname(__file__), 'data', 'npz_dft')
        output_plot_file = os.path.join(os.path.dirname(
            __file__), 'data', 'plots', 'dft_plot.png')

        f_min = None
        f_max = 150
        for channels_list in [None, [1, 2, 3]]:
            for conv_window_size in [None, 100]:
                for plot_type in ['all_channels', 'average_of_channels']:
                    if os.path.exists(output_plot_file):
                        os.remove(output_plot_file)
                    visualization.plot_dft_from_npz(
                        npz_files_folder,
                        output_plot_file,
                        f_min,
                        f_max,
                        plot_type,
                        conv_window_size=conv_window_size,
                        channels_list=channels_list)
                    self.assertTrue(os.path.exists(output_plot_file))

        os.remove(output_plot_file)
        command_prompt = f'python3 -m elecphys.main plot_dft --input_npz_folder "{npz_files_folder}" --output_plot_file {output_plot_file} --plot_type {plot_type} --conv_window_size {conv_window_size} --channels_list "{[1, 2, 3]}"'
        for _ in range(2):
            os.system(command_prompt)
        self.assertTrue(os.path.exists(output_plot_file))

    def test_plot_filter_freq_response(self):
        output_plot_file = os.path.join(
            os.path.dirname(__file__),
            'data',
            'plots',
            'filter_freq_response_plot.png')
        filter_freq_response_json_file_path = os.path.join(os.path.dirname(
            __file__), 'data', 'npz_filtered', 'filter_freq_response.json')
        if os.path.exists(output_plot_file):
            os.remove(output_plot_file)
        visualization.plot_filter_freq_response_from_json(
            filter_freq_response_json_file_path, output_plot_file)
        self.assertTrue(os.path.exists(output_plot_file))

        os.remove(output_plot_file)
        for filter_type, freq_cutoff in zip(
                ['LPF', 'HPF', 'BPF'], [60, 60, [50, 100]]):
            for filter_order in [2, 4]:
                if os.path.exists(output_plot_file):
                    os.remove(output_plot_file)
                command_prompt = f'python3 -m elecphys.main plot_filter_freq_response --filter_type {filter_type} --filter_order {filter_order} --freq_cutoff "{freq_cutoff}" --output_plot_file {output_plot_file} -fs 1000'
                for _ in range(2):
                    os.system(command_prompt)
                self.assertTrue(os.path.exists(output_plot_file))


class TestCases_4_utils(unittest.TestCase):
    def test_get_matlab_engine(self):
        pass


if __name__ == '__main__':
    os.system('pip3 uninstall elecphys -y')
    MATLAB_TEST = int(sys.argv[1])
    os.environ['ELECPHYS_DEBUG'] = 'True'
    os.environ['ELECPHYS_VERBOSE'] = 'True'
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
