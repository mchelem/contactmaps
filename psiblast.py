import os
import shutil
import subprocess
import tempfile

import pandas


def _read_pssm(pssm_dir):
    column_names = ['idx'] + 'A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V'.split()
    pssm_table = pandas.read_csv(
        os.path.join(pssm_dir, 'pssm.txt'),
        engine='python',
        sep='\s+',
        usecols=[0] + list(range(2, 22)),  # skip column with the sequence
        names=column_names,
        index_col=0,
        skiprows=3,
        skipfooter=5,
    )
    return pssm_table.as_matrix()


def pssm(sequence=None, filename=None):
    pssm_dir = tempfile.mkdtemp(prefix='pssm_psiblast__')

    if sequence is not None:
        filename = os.path.join(pssm_dir, 'tmp.fasta')
        with open(filename, 'w') as fasta_file:
            fasta_file.write('>Seq\n')
            fasta_file.write(sequence)
            filename = os.path.join(pssm_dir, 'tmp.fasta')

    subprocess.check_call([
        'psiblast',
        '-db', 'blastdb/pdbseqres',
        '-evalue', '0.01',
        '-query', filename,
        '-out_ascii_pssm', pssm_dir + '/pssm.txt',
        '-num_iterations', '3',
        '-out', 'output.txt',
        '-comp_based_stats', '0',
    ])
    pssm = _read_pssm(pssm_dir)

    try:
        shutil.rmtree(pssm_dir)
    except OSError:
        print('Could not remove pssm dir ' + pssm_dir)

    return pssm
