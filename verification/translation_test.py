import math
import pandas as pd
import sys
sys.path.append('..')

import config
from lib.io_chem import io
from lib.basic_operations import vector,physics
from source import rotation,translation,shift_origin
from helper_functions import createSystem


def translateAlongAxis():
  test_system_file_path='test_systems/ring.xyz'
  test_system_df=io.readFile(test_system_file_path)
  axis=[1,0,0]
  axis=vector.getUnitVec(axis)
  distance=4.43
  output_df=translation.translateAlongAxis(test_system_df,axis,distance)
  test_system_cords_list=list(test_system_df[['x','y','z']].values)
  output_cords_list=list(output_df[['x','y','z']].values)
  cords_list=[]
  cords_list.extend(test_system_cords_list)
  cords_list.extend(output_cords_list)
  atom_list=[]
  test_system_atom_list=list(test_system_df['atom'].values)
  output_atom_list=list(output_df['atom'].values)
  atom_list.extend(test_system_atom_list)
  atom_list.extend(output_atom_list)
  com1=physics.getCom(test_system_df)
  com2=physics.getCom(output_df)
  cords_list.extend([com1,com2])
  atom_list.extend(['b','b'])
  output_file_path='output/translate_along_axis.xyz'
  createSystem(cords_list,atom_list,output_file_path,add_axes=True)

def getAtomicDisplacement():
  x=[1,0,0]
  y=[0,1,0]
  z=[0,0,1]
  initial_cords=[-5.2,4,0]
  print(initial_cords)
  atom_data={'atom':['c'],'atom_no':[0],'x':initial_cords[0],'y':initial_cords[1],'z':initial_cords[2]}
  initial_df=pd.DataFrame.from_dict(atom_data)
  df=rotation.rotateAlongAxis(initial_df,x,math.radians(40.5))
  df=rotation.rotateAlongAxis(df,y,math.radians(15.5))
  df=rotation.rotateAlongAxis(df,z,math.radians(8.6))
  final_df=translation.translateAlongAxis(df,df[['x','y','z']].values[0],2.45)
  final_cords=final_df[['x','y','z']].values[0]
  print(final_cords)

  rpy=rotation.getRPYAngles(initial_cords,final_cords)
  rpy_d=map(math.degrees,rpy)
  for angle in rpy_d:
    print(angle)
  df=rotation.rotateAlongAxis(initial_df,x,rpy[0])
  df=rotation.rotateAlongAxis(df,y,rpy[1])
  df=rotation.rotateAlongAxis(df,z,rpy[2])
  trans_vec=translation.getAtomicDisplacement(initial_cords,final_cords)
  print(trans_vec)
  distance=vector.getMag(trans_vec)
  print(distance)
  df=translation.translateAlongAxis(df,trans_vec,distance)
  print(df[['x','y','z']].values[0])
 
def trans_atomic_r_t():
  file=open('test_systems/ring_track_two_frames.xyz','r')
  frame1_cords_df=io.readFileMd(file,0,frame_no_pos=config.frame_no_pos)
  frame2_cords_df=io.readFileMd(file,1,frame_no_pos=config.frame_no_pos)
  frame1_cords_df,frame2_cords_df=shift_origin.shiftOrigin(frame1_cords_df,frame2_cords_df)
  _translation=translation.trans_atomic_r_t(frame1_cords_df,frame2_cords_df) 
  file.close()
  print(_translation)

def trans_com():
  file=open('test_systems/ring_track_two_frames.xyz','r')
  frame1_cords_df=io.readFileMd(file,0,frame_no_pos=config.frame_no_pos)
  frame2_cords_df=io.readFileMd(file,1,frame_no_pos=config.frame_no_pos)
  frame1_cords_df,frame2_cords_df=shift_origin.shiftOrigin(frame1_cords_df,frame2_cords_df)
  _translation=translation.trans_com(frame1_cords_df,frame2_cords_df)
  file.close()
  print(_translation)


#translateAlongAxis()
#getAtomicDisplacement()
trans_atomic_r_t()
trans_com()
