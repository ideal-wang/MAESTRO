# from HazardField import *
from pydantic import BaseModel, Field
from typing import Type
import numpy as np
from langchain.tools import BaseTool

import numpy as np
import netCDF4 as nc
import pandas as pd
import matplotlib.pyplot as plt
# import pymysql
import os
import glob
from osgeo import gdal
# from geopandas. import gdal
from datetime import datetime
from numba import jit
from math import radians, cos, sin, asin, sqrt
import time
import matplotlib.colors as col
import geopandas as gpd
from shapely.geometry import Point


@jit(nopython=True)
def interpIDW(lonlat, knownData):   # 插值点， 已知点
    R = 6372.8
    ''' IDW '''
    # interp = IDW(rainData[:, 0], rainData[:, 1], rainData[:, 2], lonlat[:, 0], lonlat[:, 1])
    interp = []
    for p in range(len(lonlat)):
        lstdist = np.zeros(shape=(len(knownData)))
        # 计算插值点到已知点的距离
        for s in range(len(knownData)):
            # d = (haversine(rainData[s, 0], rainData[s, 1], lonlat[p, 0], lonlat[p, 1]))
            lon1 = knownData[s, 0]
            lat1 = knownData[s, 1]
            lon2 = lonlat[p, 0]
            lat2 = lonlat[p, 1]
            dLon = radians(lon2 - lon1)
            dLat = radians(lat2 - lat1)
            lat1 = radians(lat1)
            lat2 = radians(lat2)
            a = sin(dLat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dLon / 2) ** 2
            c = 2 * asin(sqrt(a))
            d = R * c
            lstdist[s] = d
        sumsup = 1 / np.power(lstdist, 2.5)
        suminf = sumsup.sum()
        sumsup = np.sum(sumsup * knownData[:, 2])
        u = sumsup / suminf
        interp.append(u)
    return interp


def getTiffAttr(name):
    dataset = gdal.Open(name)
    im_width = dataset.RasterXSize  # 栅格列数
    im_height = dataset.RasterYSize  # 栅格行数
    im_bands = dataset.RasterCount  # 波段

    im_geotrans = dataset.GetGeoTransform()  # 地图投影信息
    minx = im_geotrans[0]
    miny = im_geotrans[3] + im_width * im_geotrans[4] + im_height * im_geotrans[5]
    maxx = im_geotrans[0] + im_width * im_geotrans[1] + im_height * im_geotrans[2]
    maxy = im_geotrans[3]
    step = [im_geotrans[1], im_geotrans[5]]
    extent = [minx, maxx, miny, maxy]
    im_datas = np.zeros(shape=(dataset.RasterCount, im_height, im_width))
    for i in range(0, dataset.RasterCount):
        band = dataset.GetRasterBand(i + 1)
        im_datas[i, :, :] = band.ReadAsArray(0, 0, im_width, im_height)
    if dataset.RasterCount == 1:
        im_datas = im_datas.squeeze(0)
    return extent, im_datas, step


def intp_hazardMap(df):
    [left, right, down, up], step = [117, 124, 26, 32], 0.05
    xgrid, ygrid = np.meshgrid(np.arange(left, right + step, step), np.arange(down, up + step, step))
    lonlatGrid = np.hstack((xgrid.reshape(-1, 1), ygrid.reshape(-1, 1)))

    '''-----------   下面开始插值   ----------------------------'''
    rainStation = df[['经度', '纬度', 'precipitation']].values.astype(float)
    windStation = df[['经度', '纬度', 'wind_speed']].values.astype(float)
    rainStation = rainStation[rainStation[:, 2] >= 0]                    # 排除异常值
    windStation = windStation[windStation[:, 2] >= 0]                    # 排除异常值

    rainIntp = interpIDW(lonlatGrid, rainStation)
    rainIntp = np.array(rainIntp).reshape(xgrid.shape[0], xgrid.shape[1])
    windIntp = interpIDW(lonlatGrid, windStation)
    windIntp = np.array(windIntp).reshape(xgrid.shape[0], xgrid.shape[1])
    return windIntp, rainIntp



def observedIntp(alarmTime, currentTime):
    t1 = time.time()
    ''' 数据库读取输入数据 '''
    # conn = pymysql.connect(host='rm-bp11161odccsh8gopfo.mysql.rds.aliyuncs.com', user='projectEF',
    #                        passwd='renke2022', port=3306, db='project_linan')
    # precipitation = pd.read_sql('select * from 实测降雨', conn)

    ''' &&&&&&& 输入文件 1 '''
    stationInfo = pd.read_csv('../../数据文件/静态数据/ZJ_station_feature.csv')

    ''' &&&&&&& 输入文件 2 '''
    ncFilePath = '../数据文件/动态数据/meteorological_forecast_data/'
    ncData = nc.Dataset(ncFilePath + 'OHF.' + str(currentTime) + '.nc')

    # ''' &&&&&&& 输入文件 3 '''
    weatherStation = pd.read_csv('../数据文件/动态数据/实测降雨.csv')
    weatherStation = pd.merge(weatherStation, stationInfo[['站号', '经度', '纬度']], left_on='station_code', right_on='站号')

    '''处理时间段信息'''
    alarmTime = str(alarmTime)
    currentTime = str(currentTime)
    startTime = datetime.strptime(alarmTime, '%Y%m%d%H').strftime('%Y-%m-%d %H')
    endTime = datetime.strptime(currentTime, '%Y%m%d%H').strftime('%Y-%m-%d %H')
    totalTimeRange = [x.strftime('%Y%m%d%H') for x in list(pd.date_range(start=startTime, end=endTime, freq='H'))]

    '''-----------------插值实测风雨场------------------'''
    obserPath = '../数据文件/输出数据/实测风雨场/'
    obsNameList = glob.glob(os.path.join(obserPath, "*.txt"))
    obsDate = [i[19:29] for i in obsNameList]

    windObser_seq = np.zeros(shape=(len(totalTimeRange), 121, 141))
    rainObser_seq = np.zeros(shape=(len(totalTimeRange), 121, 141))
    for idx, timeStep in enumerate(totalTimeRange):
        # 实测气象站数据插值
        if timeStep not in obsDate:
            newData = weatherStation[weatherStation['observe_time'] == int(timeStep)]
            if len(newData) != 0:
                windObs, rainObs = intp_hazardMap(newData)

            np.savetxt(f'{obserPath}{timeStep}_windMap.txt', windObs)
            np.savetxt(f'{obserPath}{timeStep}_rainMap.txt', rainObs)
            windObser_seq[idx] = windObs
            rainObser_seq[idx] = rainObs
            print(f'interpolate {timeStep} data')

        # 如果已经插值过，直接从数据库中提取
        else:
            print(f'loading {timeStep} data')
            windObs = np.loadtxt(f'{obserPath}{timeStep}_windMap.txt')
            rainObs = np.loadtxt(f'{obserPath}{timeStep}_rainMap.txt')
            windObser_seq[idx], rainObser_seq[idx] = windObs, rainObs

    print('finished loading observation data')

    '''-----------------插值实测风雨场------------------'''
    windNC_seq = np.zeros(shape=(24, 121, 141))
    rainNC_seq = np.zeros(shape=(24, 121, 141))
    timeNC = ncData.variables['time']
    for i in timeNC[:]:
        rainNC = ncData.variables['Pr'][i - 1, :, :]
        windU = ncData.variables['UM'][i - 1, :, :]
        windV = ncData.variables['VM'][i - 1, :, :]
        windNC = np.sqrt(windU.reshape(-1, 1) ** 2 + windV.reshape(-1, 1) ** 2).reshape(windU.shape[0], windU.shape[1])
        windNC_seq[i-1] = windNC
        rainNC_seq[i-1] = rainNC

    print('finished loading forecasting data')
    windField = np.concatenate((windObser_seq, windNC_seq / 2.3), axis=0)
    rainField = np.concatenate((rainObser_seq, rainNC_seq), axis=0)

    t2 = time.time()
    print('运行时间:{:.2f}'.format(t2 - t1))
    return windField, rainField


def hazardPlot(wind, rain, ZJ_shp):
    mask = np.load('../数据文件/静态数据/districtMask.npy')
    [left, right, down, up], step = [117, 124, 26, 32], 0.05
    xgrid, ygrid = np.meshgrid(np.arange(left, right + step, step), np.arange(down, up + step, step))
    wind[mask == 0] = np.nan
    rain[mask == 0] = np.nan
    colors1 = ['#471769', '#3D508B', '#20A77F', '#7ACE52', '#C6EB24', '#FFFC05', '#FFC000', '#ED7D31', '#F35056',
              '#FF0000', '#C00000']
    colors2 = ['#223144', '#5E3177', '#9A1F73', '#D13532', '#E56737', '#F1E14B', '#D2F850', '#85D442', '#6AAC3B', '#346D2D']
    cmap1 = col.ListedColormap(colors1)
    cmap2 = col.ListedColormap(colors2)
    background = plt.imread('../数据文件/静态数据/background/back2.png')
    fig, axes = plt.subplots(2, 2, figsize=(9, 8))
    for i in range(2):
        for j in range(2):
            axes[i, j].imshow(background, extent=[left, right, down, up])
            axes[i, j].set_xticks([])
            axes[i, j].set_yticks([])
            axes[i, j].set_xlim(117.5, 123.5)
            axes[i, j].set_ylim(26.5, 31.5)
    c = axes[0, 0].contourf(xgrid, ygrid, wind, cmap=cmap1, vmax=40)
    cbar_ax = fig.add_axes([0.15, 0.05, 0.3, 0.018])
    cbar_ax.set_title('wind(m/s)')
    fig.colorbar(c, cax=cbar_ax, orientation='horizontal', ticks=range(0, 40, 5))
    axes[0, 0].set_title('Wind Map')
    c = axes[0, 1].contourf(xgrid, ygrid, rain, cmap=cmap2, vmax=80)
    cbar_ax = fig.add_axes([0.57, 0.05, 0.3, 0.018])
    cbar_ax.set_title('rain(mm)')
    fig.colorbar(c, cax=cbar_ax, orientation='horizontal', ticks=range(0, 100, 10))
    axes[0, 1].set_xticks([])
    axes[0, 1].set_yticks([])
    axes[0, 1].set_title('Rain Map')
    ZJ_shp.plot(ax=axes[0, 0], edgecolor='black', lw=0.3, facecolor='none')
    ZJ_shp.plot(ax=axes[0, 1], edgecolor='black', lw=0.3, facecolor='none')
    ZJ_shp.plot(ax=axes[1, 0], column='windMax', cmap=cmap1, vmax=40, edgecolor='black', lw=0.3)
    ZJ_shp.plot(ax=axes[1, 1], column='rain_1h', cmap=cmap2, vmax=80, edgecolor='black', lw=0.3)
    plt.subplots_adjust(hspace=0.1)


def find_polygon_index(point, gdf):
    for idx, poly in gdf.iterrows():
        if poly['geometry'].contains(point):
            print('point is in SHP')
            return idx + 1
    # print('point is not in SHP')
    return 0


def makeMask():
    ZJ_shp = gpd.read_file('../数据文件/静态数据/SHP/ZJ_boundary_学报版.shp', encoding='utf-8')
    [left, right, down, up], step = [117, 124, 26, 32], 0.05
    xgrid, ygrid = np.meshgrid(np.arange(left, right + step, step), np.arange(down, up + step, step))
    lonlatGrid = np.hstack((xgrid.reshape(-1, 1), ygrid.reshape(-1, 1)))

    points_gdf = gpd.GeoDataFrame(geometry=[Point(x, y) for x, y in lonlatGrid], crs=ZJ_shp.crs)
    index = [find_polygon_index(point, ZJ_shp) for point in points_gdf.geometry]
    index = np.array(index).reshape(xgrid.shape[0], xgrid.shape[1])
    np.save('../数据文件/静态数据/districtMask.npy', index)


def max_cummulative(array, window):
    if array.shape[1] < window:
        raise ValueError("数据长度少于滑动窗口大小")
    max_cumulative_array = []
    for row in array:
        cumulative_array = np.convolve(row, np.ones(window), mode='valid')
        max_cumulative_array.append(np.max(cumulative_array))
    return max_cumulative_array


def hazardCounty(windField, rainField, currentTime):
    filePath = '../../数据文件/静态数据/'
    ZJ_shp = gpd.read_file(filePath + 'SHP/ZJ_boundary_学报版.shp', encoding='utf-8')
    mask = np.load(filePath + 'districtMask.npy')
    wind_c, rain_c = [], []
    for i in range(89):
        # 下城区没有值
        if i == 1:
            idx = i
        else:
            idx = i + 1
        wind_c.append(windField[:, mask == idx].mean(axis=1))
        rain_c.append(rainField[:, mask == idx].mean(axis=1))
    wind_c, rain_c = np.array(wind_c), np.array(rain_c)
    # 提取特征变量
    ZJ_shp['windMax'] = wind_c.max(axis=1)
    ZJ_shp['rain_1h'] = rain_c.max(axis=1)
    # np.save(f'../数据文件/输出数据/气象输出/{currentTime}_hx.npy', np.concatenate((wind_c, rain_c), axis=1))
    county_hazard_data = np.concatenate((wind_c, rain_c), axis=1)
    print('区县尺度气象要素计算完成')
    # return ZJ_shp
    return county_hazard_data
# # Define input schema for WeatherInterpolationTool
# class WeatherInterpolationInput(BaseModel):
#     alarm_time: str = Field(description="Alarm time in format 'YYYYMMDDHH'")
#     time4forecast: str = Field(description="Current time in format 'YYYYMMDDHH'")
#
# # Define the WeatherInterpolationTool class
# class WeatherInterpolationTool(BaseTool):
#     name = "weather_interpolation_tool"
#     description = "Performs spatial interpolation of observed wind and rain fields."
#     args_schema: Type[BaseModel] = WeatherInterpolationInput
#
#     def _run(self, alarm_time: str, time4forecast: str):
#         print("==========section 0: Performing spatial interpolation of observed wind and rain fields========")
#         windField, rainField = observedIntp(alarm_time, time4forecast)
#
#         # Save the interpolated wind and rain fields as .npy files
#         wind_field_path = f'../数据文件/输出数据/{time4forecast}_windField.npy'
#         rain_field_path = f'../数据文件/输出数据/{time4forecast}_rainField.npy'
#         np.save(wind_field_path, windField)
#         np.save(rain_field_path, rainField)
#         print(f"Saved interpolated wind and rain fields as {wind_field_path} and {rain_field_path}")
#
#         return {
#             "wind_field": windField,
#             "rain_field": rainField
#         }
#
#     def _arun(self, alarm_time: str, time4forecast: str):
#         raise NotImplementedError("weather_interpolation_tool does not support async")
#
# # Example function to run the tool
# def runWeatherInterpolation(alarm_time: str, time4forecast: str):
#     tool = WeatherInterpolationTool()
#     result = tool._run(alarm_time, time4forecast)
#     print(result)
#
#
# # Define input schema for CountyHazardCalculationTool
# class CountyHazardCalculationInput(BaseModel):
#     time4forecast: str = Field(description="Current time in format 'YYYYMMDDHH'")
#
# # Define the CountyHazardCalculationTool class
# class CountyHazardCalculationTool(BaseTool):
#     name = "county_hazard_calculation_tool"
#     description = "Calculates county-scale wind and rain sequences from interpolated fields."
#     args_schema: Type[BaseModel] = CountyHazardCalculationInput
#
#     def _run(self, time4forecast: str):
#
#         wind_field_path =  f'../数据文件/输出数据/{time4forecast}_windField.npy'
#         rain_field_path =  f'../数据文件/输出数据/{time4forecast}_rainField.npy'
#
#         print("==========section 1: Calculating county-scale wind and rain sequences========")
#         # Load the wind and rain fields from the .npy files
#         windField = np.load(wind_field_path)
#         rainField = np.load(rain_field_path)
#
#         # Calculate the county-scale hazard data
#         hazard_np = hazardCounty(windField, rainField, time4forecast)
#
#         # Save the county-scale hazard data
#         hazard_np_path = f'../数据文件/输出数据/气象输出/{currentTime}_hx.npy'
#         hazard_np.save(hazard_np_path)
#         print(f"Saved county-scale hazard data as {hazard_np_path}")
#
#         return hazard_np
#
#     def _arun(self, time4forecast: str, wind_field_path: str, rain_field_path: str):
#         raise NotImplementedError("county_hazard_calculation_tool does not support async")
#
# # Example function to run the tool
# def runCountyHazardCalculation(time4forecast: str, wind_field_path: str, rain_field_path: str):
#     tool = CountyHazardCalculationTool()
#     result = tool._run(time4forecast, wind_field_path, rain_field_path)
#     print(result)
#
# if __name__ == "__main__":
#     # Step 1: Run Weather Interpolation
#     def runWeatherInterpolationExample():
#         # Define the alarm time and current time in the required format
#         alarm_time = '2022091308'  # Example alarm time (YYYYMMDDHH)
#         time4forecast = '2022091320'  # Example current time (YYYYMMDDHH)
#
#         # Create an instance of the tool
#         interpolation_tool = WeatherInterpolationTool()
#
#         # Run the tool with the provided times
#         result = interpolation_tool._run(alarm_time, time4forecast)
#
#         # Print the result paths of the interpolated fields
#         print("Weather Interpolation Result:", result)
#         return result
#
#     # Run the first tool to get interpolated field paths
#     interpolated_result = runWeatherInterpolationExample()



# Define input schema for the tool
class MeteorologicalDataProcessingInput(BaseModel):
    alarm_time: str = Field(description="Alarm time in format 'YYYYMMDDHH'")
    current_time: str = Field(description="Current time in format 'YYYYMMDDHH'")

# Define the tool class
class MeteorologicalDataProcessingTool(BaseTool):
    name: str = "meteorological_data_processing_tool"
    description: str = "Processes meteorological data to generate interpolated wind and rain fields and calculates county-scale hazard data."
    args_schema: Type[BaseModel] = MeteorologicalDataProcessingInput

    def _run(self, alarm_time: str, current_time: str):
        # print("==========section 0: Performing spatial interpolation of observed wind and rain fields========")
        # windField, rainField = observedIntp(alarm_time, time4forecast)
        #
        # print("==========section 1: Calculating county-scale wind and rain sequences========")
        # hazard_df = hazardCounty(windField, rainField, time4forecast)

        return {
            "rainField_path": f'../数据文件/输出数据/{current_time}_windField.npy',
            "windField_path": f'../数据文件/输出数据/{current_time}_rainField.npy',
            "hazard_county_path": f'../数据文件/输出数据/{current_time}_hx.npy'
        }

    def _arun(self, alarm_time: str, current_time: str):
        raise NotImplementedError("weather_data_processing_tool does not support async")

if __name__ == '__main__':
    # Example main function to simulate tool execution
    def mainWeatherDataProcessing(alarm_time: str, current_time: str):
        tool = MeteorologicalDataProcessingTool()
        result = tool._run(alarm_time, current_time)
        print(result)

    mainWeatherDataProcessing(alarm_time='2022091308', current_time='2022091320')

