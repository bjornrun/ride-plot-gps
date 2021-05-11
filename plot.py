import sys
import pandas as pd
import folium
import datetime as dt


def _plot_gps_data(src_file: str, dst_file: str) -> None:
    df = pd.read_csv(src_file, index_col='datetime', parse_dates=True).fillna(0)
    print(df.head())
    print(df.info())
    df = df[(df['lat'] != 0) & (df['lon'] != 0)]
    #    lon_max = df['lon'].max()
    #    lon_min = df['lon'].min()
    lon_mean = df['lon'].mean()
    #    lat_max = df['lat'].max()
    #    lat_min = df['lat'].min()
    lat_mean = df['lat'].mean()

    m = folium.Map(width=2048, height=2048, location=[lat_mean, lon_mean], zoom_start=11, min_zoom=5, max_zoom=19)

    oneday = dt.timedelta(1)
    currentday = df.index[0].replace(hour=0, minute=0, second=0, microsecond=0)
    lastday = df.index[-1]
    while currentday < lastday:
        tmp_df = df[(df.index >= currentday) & (df.index <= currentday + oneday)]
        f = folium.FeatureGroup(currentday.strftime('%Y-%02m-%d'))
        track = tmp_df[['lat', 'lon']].drop_duplicates()
        print("{d_str}: track len: {track_len}".format(d_str=currentday.strftime('%Y-%m-%d'), track_len=len(track)))
        if len(track) > 0:
            folium.vector_layers.CircleMarker((track.iloc[0]['lat'], track.iloc[0]['lon']),
                                              popup='<b>Ride day start</b>', tooltip='Ride',
                                              color='red', weight=1, radius=1).add_to(f)
            folium.vector_layers.PolyLine(list(zip(track['lat'], track['lon'])), popup='<b>Ride path</b>',
                                          tooltip='Ride', color='blue',
                                          weight=1).add_to(f)
            f.add_to(m)
        currentday += oneday

    folium.LayerControl().add_to(m)
    m.save(dst_file)


if __name__ == '__main__':
    if sys.argv == 1:
        _plot_gps_data("/mnt/gps.csv", "/mnt/smb/gps_plot.html")
    else:
        print("Src:", sys.argv[1], " Dst:", sys.argv[2])
        _plot_gps_data(sys.argv[1], sys.argv[2])
