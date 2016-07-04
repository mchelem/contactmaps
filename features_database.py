import logging
import pickle
import sqlite3


class Database:
    """
    Wrapper around the database
    """
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)

    def execute(self, query, args=None):
        try:
            cursor = self.conn.cursor()
            if args:
                cursor.execute(query, args)
            else:
                cursor.execute(query)
            self.conn.commit()
        except sqlite3.OperationalError as e:
            logging.info(e)

    def retrieve(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchone()

    def close(self):
        self.conn.close()


class SpatialFeaturesDatabase(Database):
    """
    Cache torsion angles calculation
    """
    def create(self):
        parent = super(SpatialFeaturesDatabase, self)
        parent.execute(
            """
            CREATE TABLE IF NOT EXISTS spatial_features (
                id text, indices blob, sequence text,
                secondary_structure text, solvent_accessibility blob,
                pssm blob,
                distance_map blob
            )
            """
        )
        parent.execute(
            """
            CREATE INDEX IF NOT EXISTS IdxPDB ON spatial_features(id)
            """
        )

    def save(self, structure_id, dssp_result, pssm, distance_map):
        query = """
            INSERT INTO spatial_features VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        args = (
            structure_id.lower(),
            sqlite3.Binary(pickle.dumps(dssp_result.indices)),
            dssp_result.sequence,
            dssp_result.secondary_structure,
            sqlite3.Binary(pickle.dumps(dssp_result.solvent_accessibility)),
            sqlite3.Binary(pickle.dumps(pssm)),
            sqlite3.Binary(pickle.dumps(distance_map)),
        )
        super(SpatialFeaturesDatabase, self).execute(query, args)

    def retrieve(self, structure_id):
        result = super(SpatialFeaturesDatabase, self).retrieve(
            """
            SELECT * from spatial_features WHERE id = '{}' """.format(
                structure_id.lower())
        )
        if result and len(result) == 7:
            result = dict(
                structure_id=result[0],
                indices=pickle.loads(result[1]),
                sequence=result[2],
                secondary_structure=result[3],
                solvent_accessibility=pickle.loads(result[4]),
                pssm=pickle.loads(result[5]),
                distance_map=pickle.loads(result[6]),
            )
        else:
            result = None
        return result

