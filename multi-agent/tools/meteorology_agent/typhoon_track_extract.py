import csv

# Open the input text file and output CSV file
with open('../../数据文件/动态数据/台风路径/CH2022BST.txt', 'r') as txt_file, open(
        '../../数据文件/动态数据/台风路径/CH2022BST.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Write the header for the CSV
    writer.writerow(['Header_Indicator', 'International_ID', 'Data_Lines', 'Cyclone_Serial', 'Chinese_ID',
                     'Flag', 'Time_Interval', 'Storm_Name', 'Date', 'Intensity', 'Lat', 'Long',
                     'Pressure', 'Wind', 'OWD'])

    for line in txt_file:
        if line.startswith('66666'):
            # Header line
            header_indicator = line[0:5].strip()
            international_id = line[6:10].strip()
            data_lines = line[11:14].strip()
            cyclone_serial = line[15:19].strip()
            chinese_id = line[20:24].strip()
            flag = line[25:26].strip()
            time_interval = line[27:28].strip()
            storm_name = line[30:50].strip()
            date = line[51:59].strip()

        else:
            # Data lines
            date = line[0:10].strip()
            intensity = line[11:12].strip()
            lat = line[13:16].strip()
            lon = line[17:21].strip()
            pressure = line[22:26].strip()
            wind = line[27:30].strip()
            owd = line[31:].strip()

            # Write the row to the CSV file
            writer.writerow([header_indicator, international_id, data_lines, cyclone_serial, chinese_id,
                             flag, time_interval, storm_name, date, intensity, lat, lon, pressure, wind, owd])

print("Conversion complete. The data has been saved to output.csv.")
