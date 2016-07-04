import Bio.PDB

class DsspResult:
    sequence = None
    indices = None
    secondary_structure = None
    solvent_acessibility = None

    def __repr__(self):
        "{}\n{}\n".format(
            self.secondary_structure,
            self.solvent_accessibility
        )


def assign(filename=None):
    parser = Bio.PDB.PDBParser()
    structure = parser.get_structure('X', filename)
    model = structure[0]
    dssp = Bio.PDB.DSSP(model, filename)
    results = [properties[0:4] for properties in dssp.property_list]
    results = list(zip(*results))
    dssp_result = DsspResult()
    dssp_result.indices = results[0]
    dssp_result.sequence = ''.join(results[1])
    dssp_result.secondary_structure = ''.join(results[2])
    dssp_result.solvent_accessibility = results[3]
    return dssp_result
