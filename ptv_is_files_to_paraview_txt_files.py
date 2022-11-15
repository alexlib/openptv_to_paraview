# Example notebook translating OpenPTV files for Paraview using flowtracks
import numpy as np
import scipy
import pandas as pd
from flowtracks.io import trajectories_ptvis


dataset = trajectories_ptvis('./openptv_results/ptv_is.%d',xuap=False)


dataframes = []
for traj in dataset:
    dataframes.append(
        pd.DataFrame.from_records(
            traj,
            columns=['x','y','z','Vx','Vy','Vz','frame','Particle']
        )
    )


df = pd.concat(dataframes,ignore_index=True)


df['Particle'] = df['Particle'].astype(np.int32)

# Paraview does not recognize it as a set without _000001.txt, so we the first 10000
# ptv_is.10001 is becoming ptv_00001.txt

df['frame'] = df['frame'].astype(np.int32) - 10000


df.reset_index(inplace=True, drop=True)
df.head()


df_grouped = df.reset_index().groupby('frame')
for index, group in df_grouped:
    group.to_csv(
        f'./paraview_output/ptv_{int(index):05d}.txt',
        mode='w',
        columns=['Particle','x','y','z','Vx','Vy','Vz'], 
        index=False
        )


