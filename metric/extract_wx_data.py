__author__ = "jwely"

from datetime import datetime

from metric import time_series
from metric.textio.read_ds3505 import read_DS3505


def extract_wx_data(time_obj, wx_path):
    """
    This function was writen to reenstate wx file parsing for tha greed upon NOAA
    obsgrid data format for any study area within the USA. This is THE function
    that should be used for reading obsgrid data, the others will not be supported.

    It expects data in the format as retrieved from this URL:
        [http://gis.ncdc.noaa.gov/map/viewer/#app=cdo&cfg=cdo&theme=hourly&layers=1&node=gi]
    
    Please see the readme for more detailed instructions on data download.

    Inputs:
        time_obj    A datetime object representing the image data aquisition datetime
        wx_path     filepath to the obsgrid data. (hourly data)

    Returns:
        an array with specific ordering of climate variables.
    """

    # format obsgrid (daily and hourly) as a time series object
    wx = time_series.time_series("wx_data")
    tdo = read_DS3505(wx_path, has_headers=True)
    wx.from_tdo(tdo)
    time_lable = "YR--MODAHRMN"
    time_format = "%Y%m%d%H%M"
    start_time = "200001010000"
    wx.define_time(time_lable, time_format, start_time)

    # bin the data into days pull out the one we want.
    wx.make_subsets("%j", cust_center_time=time_obj)

    day_name = time_obj.strftime("%Y-%m-%d")
    wx.interrogate()

    # if it cant find a subset in wx with the input dates name, wx data is for wrong time.
    try:
        wx_day = wx[day_name]
    except:
        raise Exception("wx data has no entries for date of landsat acquisition ({0})".format(time_obj))

    # get min/max temperatures and convert to Celcius (statistical operations clean up NoData)
    print("Centered statistics around {0}".format(wx_day.center_time))
    Tstats = wx_day.column_stats("TEMP")
    temp_C_min = (Tstats["TEMP_min_v"] - 32) * (5.0 / 9)  # F --> C
    temp_C_max = (Tstats["TEMP_max_v"] - 32) * (5.0 / 9)  # F --> C

    # get instantaneous variables at input @param time_obj by interpolating between nearest values
    temp_C_mid = (wx_day.interp_col(time_obj, "TEMP") - 32) * (5.0 / 9)  # F --> C
    P_air = wx_day.interp_col(time_obj, "STP")  # in millibars
    wind_speed = wx_day.interp_col(time_obj, "SPD") * 0.51444  # knots --> meters / second
    dewp_C = (wx_day.interp_col(time_obj, "DEWP") - 32) * (5.0 / 9)  # F --> C

    # this format is for legacy support, just an array of values, not a dict.
    print("Temperature is {0}C".format(temp_C_mid))
    return [temp_C_min, temp_C_max, temp_C_mid, P_air, wind_speed, dewp_C]


# testing
if __name__ == "__main__":
    wx_filepath = r"E:\DEVELOP\Team_Projects\2015_Spring_METRIC\code_current_dev\input_weather\2013_July_CravenCountyAirport.txt"
    time = datetime(2013, 7, 17, 11, 43, 24)
    wx = extract_wx_data(time, wx_filepath)
    print wx

# =======================================================================================
