import csv
import re

def parse_to_csv(data_string, output_filename):
    # Split the input string into sections for each image
    images = data_string.strip().split('---')

    # Prepare a list to hold the parsed data
    parsed_data = []

    # Define a regex pattern to capture the relevant data
    pattern = re.compile(
        r'Image:\s*(\d+\.jpg)\s*'
        r'NW Corner Lat:\s*([-\d.]+),\s*'
        r'NW Corner Long:\s*([-\d.]+),\s*'
        r'SE Corner Lat:\s*([-\d.]+),\s*'
        r'SE Corner Long:\s*([-\d.]+)'
    )

    for image in images:
        match = pattern.search(image)
        if match:
            image_name = match.group(1)
            nw_lat = match.group(2)
            nw_long = match.group(3)
            se_lat = match.group(4)
            se_long = match.group(5)

            # Append the data to the list
            parsed_data.append({
                'Image': image_name,
                'NW Corner Lat': nw_lat,
                'NW Corner Long': nw_long,
                'SE Corner Lat': se_lat,
                'SE Corner Long': se_long
            })

    # Write the parsed data to a CSV file
    with open(output_filename, mode='w', newline='') as csv_file:
        fieldnames = ['Image', 'NW Corner Lat', 'NW Corner Long', 'SE Corner Lat', 'SE Corner Long']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()  # Write the header
        writer.writerows(parsed_data)  # Write the data rows

# Example input string
data_string = """
Image: 1.jpg
NW Corner Lat: 42.88093888888889,
NW Corner Long: -85.41462222222223,
SE Corner Lat: 42.87416666666667,
SE Corner Long: -85.40518055555556

---
Image: 2.jpg
NW Corner Lat: 43.02781111111111,
NW Corner Long: -85.79115833333333,
SE Corner Lat: 43.02106944444444,
SE Corner Long: -85.78165277777778

---
Image: 3.jpg
NW Corner Lat: 43.299680555555554,
NW Corner Long: -85.38419166666667,
SE Corner Lat: 43.292905555555556,
SE Corner Long: -85.37468888888888

---
Image: 4.jpg
NW Corner Lat: 43.12829166666667,
NW Corner Long: -85.37199722222222,
SE Corner Lat: 43.12151388888889,
SE Corner Long: -85.36252222222221

---
Image: 5.jpg
NW Corner Lat: 42.76871666666666,
NW Corner Long: -85.65483611111112,
SE Corner Lat: 42.76196111111111,
SE Corner Long: -85.64538611111112

---
Image: 6.jpg
NW Corner Lat: 43.17207222222222,
NW Corner Long: -85.77574722222222,
SE Corner Lat: 43.165330555555556,
SE Corner Long: -85.76621944444445

---
Image: 7.jpg
NW Corner Lat: 43.13812222222222,
NW Corner Long: -85.74686666666666,
SE Corner Lat: 43.131375,
SE Corner Long: -85.73734722222223

---
Image: 8.jpg
NW Corner Lat: 42.80146666666666,
NW Corner Long: -85.78595555555556,
SE Corner Lat: 42.794725,
SE Corner Long: -85.77648611111111

---
Image: 9.jpg
NW Corner Lat: 43.15206111111111,
NW Corner Long: -85.72843888888869,
SE Corner Lat: 43.145313888886806,
SE Corner Long: -85.71891944444445

---
Image: 10.jpg
NW Corner Lat: 43.179608333333364,
NW Corner Long: -85.71967222222223,
SE Corner Lat: 43.17285893333333,
SE Corner Long: -85.71015

---
Image: 11.jpg
NW Corner Lat: 42.857350000000004,
NW Corner Long: -85.70330883833334,
SE Corner Lat: 42.8506,
SE Corner Long: -85.69363611111111

---
Image: 12.jpg
NW Corner Lat: 42.812925,
NW Corner Long: -85.34824444444445,
SE Corner Lat: 42.80614444444444,
SE Corner Long: -85.33881944444444

---
Image: 13.jpg
NW Corner Lat: 43.09066388888889,
NW Corner Long: -85.699,
SE Corner Lat: 43.083913888888804,
SE Corner Long: -85.68949444444445

---
Image: 14.jpg
NW Corner Lat: 42.8028,
NW Corner Long: -85.67417777777779,
SE Corner Lat: 42.79604722222222,
SE Corner Long: -85.66471944444444

---
Image: 15.jpg
NW Corner Lat: 42.83106666666667,
NW Corner Long: -85.60020277777777,
SE Corner Lat: 42.82430555555556,
SE Corner Long: -85.59075

---
Image: 16.jpg
NW Corner Lat: 43.269730555555554,
NW Corner Long: -85.63715388886869,
SE Corner Lat: 43.262975,
SE Corner Long: -85.6276361111111

---
Image: 17.jpg
NW Corner Lat: 42.874658333333336,
NW Corner Long: -85.34922222222222,
SE Corner Lat: 42.86788055555556,
SE Corner Long: -85.33978888888889

---
Image: 18.jpg
NW Corner Lat: 43.19438888888889,
NW Corner Long: -85.62623333333333,
SE Corner Lat: 43.19438888888889,
SE Corner Long: -85.61685833333333

---
Image: 19.jpg
NW Corner Lat: 42.83146111111112,
NW Corner Long: -85.56292499999999,
SE Corner Lat: 42.8247,
SE Corner Long: -85.55347499999999

---
Image: 20.jpg
NW Corner Lat: 42.79040277777778,
NW Corner Long: -85.55281944444444,
SE Corner Lat: 42.78363888888889,
SE Corner Long: -85.543375

---
Image: 21.jpg
NW Corner Lat: 43.08953888888889,
NW Corner Long: -85.79258333333333,
SE Corner Lat: 43.082797222222226,
SE Corner Long: -85.78306666666667

---
Image: 22.jpg
NW Corner Lat: 43.215260444444445,
NW Corner Long: -85.59852222222221,
SE Corner Lat: 43.208511111111115,
SE Corner Long: -85.58900883833333

---
Image: 23.jpg
NW Corner Lat: 42.893483333333336,
NW Corner Long: -85.53613333333332,
SE Corner Lat: 42.886719444444445,
SE Corner Long: -85.526675

---
Image: 24.jpg
NW Corner Lat: 42.89367222222222,
NW Corner Long: -85.517475,
SE Corner Lat: 42.88690833333333,
SE Corner Long: -85.50801944444444

---
Image: 25.jpg
NW Corner Lat: 42.89555277777778,
NW Corner Long: -85.31223333333332,
SE Corner Lat: 42.88876944444444,
SE Corner Long: -85.30279999999999

---
Image: 26.jpg
NW Corner Lat: 42.79210277777778,
NW Corner Long: -85.3758611111111,
SE Corner Lat: 42.785325,
SE Corner Long: -85.3664361111111

---
Image: 27.jpg
NW Corner Lat: 42.768505555555556,
NW Corner Long: -85.67345555555556,
SE Corner Lat: 42.76175277777778,
SE Corner Long: -85.66400277777778

---
Image: 28.jpg
NW Corner Lat: 43.18117465197748,
NW Corner Long: -85.57909078876155,
SE Corner Lat: 43.17441427726903,
SE Corner Long: -85.56958449893962

---
Image: 29.jpg
NW Corner Lat: 42.89474379865728,
NW Corner Long: -85.40552609503916,
SE Corner Lat: 42.88796867007531,
SE Corner Long: -85.39608276301134

---
Image: 30.jpg
NW Corner Lat: 43.25089444444444,
NW Corner Long: -85.46784722222222,
SE Corner Lat: 43.244125000000004,
SE Corner Long: -85.45834166666667

---
"""

# Output CSV filename
output_filename = 'parsed_coordinates.csv'

# Run the parser
parse_to_csv(data_string, output_filename)
