import os

import pandas

import features_database
import dssp
import psiblast
from pconpy import pconpy


def add_structure_to_db(db, structure_id, filename):
	dssp_result = dssp.assign(filename)
	pssm = psiblast.pssm(dssp_result.sequence)
	residues = pconpy.get_residues(filename)
	distance_map = pconpy.calc_dist_matrix(residues).filled(0)
	db.save(structure_id, dssp_result, pssm, distance_map)

def add_structure(db, structure_id):
	filename = astral + structure_id[2:4]  + "/" + structure_id + ".ent"
	if not os.path.isfile(filename):
		print('File not found: ' + filename)
		for i in range(1, 10):
			filename = list(filename)
			filename[-5] = str(i)
			filename = "".join(filename)
			print('Trying to use ' + filename)
			if os.path.isfile(filename):
				add_structure_to_db(db, structure_id, filename)
				print('Added structure ' + structure_id)
				return

		filename = list(filename)
		filename[-5] ="_"
		filename = "".join(filename)
		print('Trying to use ' + filename)
	if os.path.isfile(filename):
		add_structure_to_db(db, structure_id, filename)
		print('Added structure ' + structure_id)
	else:
		print('File not found: ' + filename)

db = features_database.SpatialFeaturesDatabase("spatial_features.db")
db.create()

dataset = pandas.read_csv('astral/dataset.xls', sep='\s+')
structures = dataset['DOMAIN'].tolist()
astral = "astral/pdbstyle-2.06/" 

for structure_id in structures:
	add_structure(db, structure_id)

