import os

import pandas as pd

from camels_serv.core.loader import BaseLoader


class CamelsDataset(BaseLoader):
    """
    Data Loader for the CAMELS-DE dataset.

    The camels-de dataset is not yet published, hence this API
    interface has to be considered instable.
    """
    def get_data(self, camels_id: str, date_index: bool = False, not_exists: str = 'raise') -> pd.DataFrame:
        """
        Load the timeseries for a given camels_id.

        Parameters
        ----------
        camels_id : str
            The unique identifier of the CAMELS-DE station.
        date_index : bool, optional
            If True, the 'date' column will be set as index, otherwise
            the date is returned as data column, which is the default
            behaviour.
        not_exists : str, optional
            Can be 'raise' or 'empty'. If 'raise' (default), the function
            will raise a FileNotFoundError if the datafile does not exist.
            If 'empty', an empty pandas.DataFrame with the correct column
            names is returned.
        
        Returns
        -------
        df : pandas.DataFrame
            The data time series of given camels_id

        """
        # get the federal state
        fed = camels_id[:3]

        # build the filename
        fname = os.path.join(self.base_path, fed, self.filename_template.format(camels_id=camels_id, nuts_lvl2=fed))

        # check if the file exists
        if not os.path.exists(fname):
            if not_exists == 'raise':
                raise FileNotFoundError(f"The station {camels_id} has no data file at {fname}")
            else:
                # TODO: change the column names as needed
                df = pd.DataFrame(columns=['date', 'q',  'q_flag', 'w', 'w_flag'])
        else:
            df = pd.read_csv(fname)
        
        # handle index
        if date_index:
            df.set_index('date', inplace=True)
        
        return df
