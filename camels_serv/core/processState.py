import os

import geopandas as gpd

from camels_serv.core.loader import BaseLoader


class ProcessState(BaseLoader):
    def has_output(self, base_df: gpd.GeoDataFrame = None) -> gpd.GeoDataFrame:
        """
        Return the pegel GeoDataFrame enhanced with info about existing output
        """
        if base_df is None:
            # create a copy
            base_df = self.metadata.copy()

        # go for each name
        base_df['has_out'] = [os.path.exists(os.path.join(self.base_path, p)) for p in self.metadata.camels_path]

        return base_df
        
    def describe(self) -> gpd.GeoDataFrame:
        """
        Return a described GeoDataFrame for all pegel.
        """
        # add output
        gdf = self.has_output()

        return gdf
    