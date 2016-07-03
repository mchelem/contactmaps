import multiprocessing
import subprocess
import shutil
import tempfile
import os


class Prediction:
    """
    Hold information regarding predictions
    """
    secondary_structure = None
    solvent_accessibility = None

    def __repr__(self):
        return "{}\n{}\n".format(
            self.secondary_structure,
            self.solvent_accessibility
        )


def _read_prediction(sequence, prediction_dir):
    prediction = Prediction()

    with open(os.path.join(prediction_dir, 'tmp.pred.ss')) as ss8:
        for line in ss8:
            prediction.secondary_structure = line[:-1]
    with open(os.path.join(prediction_dir, 'tmp.pred.acc')) as acc:
        for line in acc:
            prediction.solvent_accessibility = line[:-1]
    return prediction


def predict(sequence=None, filename=None):
    prediction_dir = tempfile.mkdtemp(prefix='ss_prediction_')

    if sequence is not None:
        filename = os.path.join(prediction_dir, 'tmp.fasta')
        with open(filename, 'w') as fasta_file:
            fasta_file.write('>Seq\n')
            fasta_file.write(sequence)

    subprocess.check_call([
        'libs/SCRATCH-1D_1.0/bin/run_SCRATCH-1D_predictors.sh',
        filename,
        os.path.join(prediction_dir, 'tmp.pred'),
        str(multiprocessing.cpu_count()),  # number of threads
    ])
    prediction = _read_prediction(sequence, prediction_dir)

    try:
        shutil.rmtree(prediction_dir)
    except OSError:
        print('Could not remove prediction dir ' + prediction_dir)

    return prediction
