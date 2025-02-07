import math
import pandas as pd
import sys
import numpy as np
sys.path.append('..')
from tqdm import tqdm

import config
from lib.io_chem import io
from lib.basic_operations import vector,physics
from source import rotation,translation,init,shift_origin
from helper_functions import createSystem,getRingDf,getTrackDf


def oneAtomSystemArtificial():
  file_path='test_systems/one_atom_system_artificial_system.xyz'
  cords_list=[[3,0,0]]
  atom_list=['c']
  createSystem(cords_list,atom_list,file_path,add_axes=False)

def multiAtomSystemArtificial():
  file_path='test_systems/multi_atom_system_artificial_system.xyz'
  cords_list=[[3,3,0],[-6,5,-7]]
  atom_list=['c','c']
  createSystem(cords_list,atom_list,file_path,add_axes=False)
 
def ringCordsArtificial():
  file_path='test_systems/ring_at_origin_ideal_artificial_system.xyz'
  n=20
  r=5
  initial_cords=[0,r,0]
  atom_data={'atom':['c'],'atom_no':[0],'x':initial_cords[0],'y':initial_cords[1],'z':initial_cords[2]}
  initial_df=pd.DataFrame.from_dict(atom_data)
  theta=2*math.pi/n
  ring_cords_list=[initial_cords]
  for i in range(1,n): 
    df=rotation.rotateAlongAxis(initial_df,[1,0,0],theta*i)
    ring_cords_list.append(df[['x','y','z']].values[0])
  ring_atom_list=['c']*n
  createSystem(ring_cords_list,ring_atom_list,file_path,add_axes=False)
  return ring_cords_list 
  
def trackCordsArtificial():
  file_path='test_systems/track_artificial_system.xyz'
  n=18
  initial_cords=[0,0,0]
  track_cords_list=[initial_cords]
  x=0
  for i in range(1,n):
    x+=1 
    if i%2==0:
      y=0.5
      z=0
    else:
      y=-0.5
      z=0  
    track_cords_list.append([x,y,z])
  ring_atom_list=['c']*n
  createSystem(track_cords_list,ring_atom_list,file_path,add_axes=False)
  return track_cords_list
 
def ringTrackAtOriginIdealArtificial():
  file_path='test_systems/ring_track_at_origin_ideal_artificial_system.xyz'
  ring_cords_list=ringCordsArtificial()
  track_cords_list=trackCordsArtificial()
  cords_list=[]
  atom_list=[]
  cords_list.extend(ring_cords_list)
  cords_list.extend(track_cords_list)
  atom_list=len(cords_list)*['c']
  total_track_atoms=len(track_cords_list)
  atom_list[-total_track_atoms:]=total_track_atoms*['S']
  createSystem(cords_list,atom_list,file_path,add_axes=False)
  
def ringTrackAtOriginNonIdealArtificial():
  file_path='test_systems/ring_track_at_origin_non_ideal_artificial_system.xyz'
  ring_cords_list=ringCordsArtificial()
  track_cords_list=trackCordsArtificial()
  cords_list=[]
  atom_list=[]
  cords_list.extend(ring_cords_list)
  cords_list.extend(track_cords_list)
  atom_list=len(cords_list)*['c']
  total_ring_atoms=len(ring_cords_list)
  total_track_atoms=len(track_cords_list)
  atom_list[:total_ring_atoms//2]=['Si']*(total_ring_atoms//2)
  atom_list[-total_track_atoms//2:]=['S']*(total_track_atoms//2)
  createSystem(cords_list,atom_list,file_path,add_axes=False)
  
  ring_atom_list=len(ring_cords_list)*['c']
  ring_atom_list[:total_ring_atoms//2]=['Si']*(total_ring_atoms//2)
  ring_file_path='test_systems/ring_at_origin_non_ideal_artificial_system.xyz'
  createSystem(ring_cords_list,ring_atom_list,ring_file_path,add_axes=False)
 
  track_atom_list=len(track_cords_list)*['c']
  track_atom_list[-total_track_atoms//2:]=['S']*(total_track_atoms//2)
  track_file_path='test_systems/track_at_origin_non_ideal_artificial_system.xyz'
  createSystem(track_cords_list,track_atom_list,track_file_path,add_axes=False)

  #frame1_cords=io.readFile(file_path)
  #shifted_cords_df,_=shift_origin.shiftOrigin(frame1_cords,frame1_cords,process='rotation')
  #io.writeFile(file_path,shifted_cords_df)

def ringTrackTwoFramesIdealArtificial():
  output_file_path='test_systems/ring_track_two_frames_ideal_artificial_system.xyz'
  output_file=file=open(output_file_path,'w')
  x=[1,0,0]

  ring_theta=45
  track_theta=35
  ring_distance=2
  track_distance=1

  input_system_file_path='test_systems/ring_track_at_origin_ideal_artificial_system.xyz'
  input_system_cords_df=io.readFile(input_system_file_path)
  frame1_initial_cords_df=input_system_cords_df.copy()
  #ring
  frame1_ring_cords_df=frame1_initial_cords_df[frame1_initial_cords_df['atom_no'].isin(range(config.ring_start_atom_no,config.ring_end_atom_no+1))]
  df=rotation.rotateAlongAxis(frame1_ring_cords_df,x,math.radians(ring_theta)) 
  frame2_initial_ring_cords_df=translation.translateAlongAxis(df,x,ring_distance)
  #track
  frame1_track_cords_df=frame1_initial_cords_df[frame1_initial_cords_df['atom_no'].isin(range(config.track_start_atom_no,config.track_end_atom_no+1))]
  df=rotation.rotateAlongAxis(frame1_track_cords_df,x,math.radians(track_theta))
  frame2_initial_track_cords_df=translation.translateAlongAxis(df,x,track_distance)
  #frame2
  frame2_initial_cords_df=pd.concat([frame2_initial_ring_cords_df,frame2_initial_track_cords_df])

  #transform both frames
  axis=[1,1,1]
  theta=45.24
  distance=1.67
  frame1_final_cords_df=rotation.rotateAlongAxis(frame1_initial_cords_df,axis,math.radians(theta))
  frame2_final_cords_df=rotation.rotateAlongAxis(frame2_initial_cords_df,axis,math.radians(theta))
  frame1_final_cords_df=translation.translateAlongAxis(frame1_final_cords_df,axis,distance)
  frame2_final_cords_df=translation.translateAlongAxis(frame2_final_cords_df,axis,distance)

  io.writeFileMd(output_file,frame1_final_cords_df,0,frame_no_pos=config.frame_no_pos)
  io.writeFileMd(output_file,frame2_final_cords_df,1,frame_no_pos=config.frame_no_pos)
  output_file.close()

def ringTrackTwoFramesNonIdealArtificial(ring_rpy=[60,0,0],track_rpy=[60,0,0],ring_translation=-2,track_translation=2):
  output_file_path='test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz'
  x=[1,0,0]
  y=[0,1,0]
  z=[0,0,1]
  
  input_system_file_path='test_systems/ring_track_at_origin_non_ideal_artificial_system.xyz'
  input_system_cords_df=io.readFile(input_system_file_path)
  frame1_initial_cords_df=input_system_cords_df.copy()
  #ring
  frame1_ring_cords_df=frame1_initial_cords_df[frame1_initial_cords_df['atom_no'].isin(config.ring_atom_no_list)]
  df=rotation.rotateAlongAxis(frame1_ring_cords_df,x,math.radians(ring_rpy[0]))
  df=rotation.rotateAlongAxis(df,y,math.radians(ring_rpy[1]))
  df=rotation.rotateAlongAxis(df,z,math.radians(ring_rpy[2]))
  frame2_initial_ring_cords_df=translation.translateAlongAxis(df,x,ring_translation)
  #track
  frame1_track_cords_df=frame1_initial_cords_df[frame1_initial_cords_df['atom_no'].isin(config.track_atom_no_list)]
  df=rotation.rotateAlongAxis(frame1_track_cords_df,x,math.radians(track_rpy[0]))
  df=rotation.rotateAlongAxis(df,y,math.radians(track_rpy[1]))
  df=rotation.rotateAlongAxis(df,z,math.radians(track_rpy[2]))
  frame2_initial_track_cords_df=translation.translateAlongAxis(df,x,track_translation)
  #frame2
  frame2_initial_cords_df=pd.concat([frame2_initial_ring_cords_df,frame2_initial_track_cords_df])
  
  #transform both frames 
  axis=[-10.2,-42,-6]
  theta=60.5
  distance=5.3
  frame1_final_cords_df=rotation.rotateAlongAxis(frame1_initial_cords_df,axis,math.radians(theta))
  frame2_final_cords_df=rotation.rotateAlongAxis(frame2_initial_cords_df,axis,math.radians(theta))
  frame1_final_cords_df=translation.translateAlongAxis(frame1_final_cords_df,axis,distance)
  frame2_final_cords_df=translation.translateAlongAxis(frame2_final_cords_df,axis,distance)
  
  output_file=open(output_file_path,'w')
  io.writeFileMd(output_file,frame1_initial_cords_df,0,frame_no_pos=config.frame_no_pos)
  io.writeFileMd(output_file,frame2_initial_cords_df,1,frame_no_pos=config.frame_no_pos)
  output_file.close()

def ringTwoFramesArtificial(ring_rpy=[60,0,0],track_rpy=[60,0,0],ring_translation=0,track_translation=2):
  output_file_path='test_systems/ring_two_frames_non_ideal_artificial_system.xyz'
  x=[1,0,0]
  y=[0,1,0]
  z=[0,0,1]

  input_system_file_path='test_systems/ring_at_origin_non_ideal_artificial_system.xyz'
  input_system_cords_df=io.readFile(input_system_file_path)
  frame1_initial_cords_df=input_system_cords_df.copy()
  #ring
  frame1_ring_cords_df=frame1_initial_cords_df#[frame1_initial_cords_df['atom_no'].isin(config.ring_atom_no_list)]
  df=rotation.rotateAlongAxis(frame1_ring_cords_df,x,math.radians(ring_rpy[0]))
  df=rotation.rotateAlongAxis(df,y,math.radians(ring_rpy[1]))
  df=rotation.rotateAlongAxis(df,z,math.radians(ring_rpy[2]))
  frame2_initial_ring_cords_df=translation.translateAlongAxis(df,x,ring_translation)
  #frame2
  frame2_initial_cords_df=frame2_initial_ring_cords_df

  #transform both frames
  axis=[-10.2,-42,-6]
  theta=60.5
  distance=5.3
  frame1_final_cords_df=rotation.rotateAlongAxis(frame1_initial_cords_df,axis,math.radians(theta))
  frame2_final_cords_df=rotation.rotateAlongAxis(frame2_initial_cords_df,axis,math.radians(theta))
  frame1_final_cords_df=translation.translateAlongAxis(frame1_final_cords_df,axis,distance)
  frame2_final_cords_df=translation.translateAlongAxis(frame2_final_cords_df,axis,distance)

  output_file=open(output_file_path,'w')
  io.writeFileMd(output_file,frame1_initial_cords_df,0,frame_no_pos=config.frame_no_pos)
  io.writeFileMd(output_file,frame2_initial_cords_df,1,frame_no_pos=config.frame_no_pos)
  output_file.close()

def ringTrackMultiFrameIdealArtificial():
  output_file_path='test_systems/ring_track_multi_frame_ideal_artificial_system.xyz'
  output_file=open(output_file_path,'w')
  x=[1,0,0]

  total_frames=100
  ring_theta=0
  track_theta=0
  ring_d_theta=0
  track_d_theta=0
  ring_distance=0
  track_distance=0
  ring_d_distance=0.5
  track_d_distance=0

  input_system_file_path='test_systems/ring_track_at_origin_ideal_artificial_system.xyz'
  input_system_cords_df=io.readFile(input_system_file_path)
  for curr_frame_no in range(total_frames):
    #ring
    input_system_ring_cords_df=input_system_cords_df[input_system_cords_df['atom_no'].isin(config.ring_atom_no_list)]
    df=rotation.rotateAlongAxis(input_system_ring_cords_df,x,math.radians(ring_theta))
    #df=rotation.rotateAlongAxis(df,y,math.radians(rpy[1]))
    #df=rotation.rotateAlongAxis(df,z,math.radians(rpy[2]))
    curr_frame_ring_cords_df=translation.translateAlongAxis(df,x,ring_distance)
    #track
    input_system_track_cords_df=input_system_cords_df[input_system_cords_df['atom_no'].isin(config.track_atom_no_list)]
    df=rotation.rotateAlongAxis(input_system_track_cords_df,x,math.radians(track_theta))
    #df=rotation.rotateAlongAxis(df,y,math.radians(rpy[1]))
    #df=rotation.rotateAlongAxis(df,z,math.radians(rpy[2]))
    curr_frame_track_cords_df=translation.translateAlongAxis(df,x,track_distance)
    #frame
    curr_frame_cords_df=pd.concat([curr_frame_ring_cords_df,curr_frame_track_cords_df])
    #transform frames
    axis=[1,1,1]
    theta=45.24
    distance=1.67
    curr_frame_cords_df=rotation.rotateAlongAxis(curr_frame_cords_df,axis,math.radians(theta))
    curr_frame_cords_df=translation.translateAlongAxis(curr_frame_cords_df,axis,distance)
    io.writeFileMd(output_file,curr_frame_cords_df,curr_frame_no,frame_no_pos=config.frame_no_pos)

    ring_theta+=ring_d_theta
    ring_distance+=ring_d_distance
    track_theta+=track_d_theta
    track_distance+=track_d_distance
  output_file.close()


def ringTrackMultiFrameNonIdealArtificial():
  output_file_path='test_systems/ring_track_multi_frame_ideal_artificial_system.xyz'
  output_file=open(output_file_path,'w')
  x=[1,0,0]

  total_frames=100
  ring_theta=0
  track_theta=0
  ring_d_theta=2
  track_d_theta=0
  ring_distance=0
  track_distance=0
  ring_d_distance=0
  track_d_distance=0

  input_system_file_path='test_systems/ring_track_at_origin_non_ideal_artificial_system.xyz'
  input_system_cords_df=io.readFile(input_system_file_path)
  for curr_frame_no in range(total_frames):
    #ring
    input_system_ring_cords_df=input_system_cords_df[input_system_cords_df['atom_no'].isin(config.ring_atom_no_list)]
    df=rotation.rotateAlongAxis(input_system_ring_cords_df,x,math.radians(ring_theta))
    #df=rotation.rotateAlongAxis(df,y,math.radians(rpy[1]))
    #df=rotation.rotateAlongAxis(df,z,math.radians(rpy[2]))
    curr_frame_ring_cords_df=translation.translateAlongAxis(df,x,ring_distance)
    #track
    input_system_track_cords_df=input_system_cords_df[input_system_cords_df['atom_no'].isin(config.track_atom_no_list)]
    df=rotation.rotateAlongAxis(input_system_track_cords_df,x,math.radians(track_theta))
    #df=rotation.rotateAlongAxis(df,y,math.radians(rpy[1]))
    #df=rotation.rotateAlongAxis(df,z,math.radians(rpy[2]))
    curr_frame_track_cords_df=translation.translateAlongAxis(df,x,track_distance)
    #frame
    curr_frame_cords_df=pd.concat([curr_frame_ring_cords_df,curr_frame_track_cords_df])
    #transform frames
    axis=[1,1,1]
    theta=45.24
    distance=1.67
    curr_frame_cords_df=rotation.rotateAlongAxis(curr_frame_cords_df,axis,math.radians(theta))
    curr_frame_cords_df=translation.translateAlongAxis(curr_frame_cords_df,axis,distance)
    io.writeFileMd(output_file,curr_frame_cords_df,curr_frame_no,frame_no_pos=config.frame_no_pos)

    ring_theta+=ring_d_theta
    ring_distance+=ring_d_distance
    track_theta+=track_d_theta
    track_distance+=track_d_distance
  output_file.close()
    

def ringMultiFrameArtificial():
  output_file_path='test_systems/ring_multi_frame_non_ideal_artificial_system.xyz'
  output_file=open(output_file_path,'w')
  x=[1,0,0]

  total_frames=100
  ring_theta=0
  ring_d_theta=10
  ring_distance=0
  ring_d_distance=0

  ringTrackAtOriginNonIdealArtificial()
  input_system_file_path='test_systems/ring_at_origin_non_ideal_artificial_system.xyz'
  input_system_cords_df=io.readFile(input_system_file_path)
  for curr_frame_no in range(total_frames):
    df=rotation.rotateAlongAxis(input_system_cords_df,x,math.radians(ring_theta))
    #df=rotation.rotateAlongAxis(df,y,math.radians(rpy[1]))
    #df=rotation.rotateAlongAxis(df,z,math.radians(rpy[2]))
    curr_frame_cords_df=translation.translateAlongAxis(df,x,ring_distance)
   
    
    #transform frames
    axis=[1,1,1]
    theta=45.24
    distance=1.67
    curr_frame_cords_df=rotation.rotateAlongAxis(curr_frame_cords_df,axis,math.radians(theta))
    curr_frame_cords_df=translation.translateAlongAxis(curr_frame_cords_df,axis,distance)
    
    io.writeFileMd(output_file,curr_frame_cords_df,curr_frame_no,frame_no_pos=config.frame_no_pos)

    ring_theta+=ring_d_theta
    ring_distance+=ring_d_distance
  output_file.close()

def ringTrackAtOriginSemiReal():
  file_path='test_systems/ring_track_at_origin_semi_real_system.xyz'
  frame1_no=0
  frame2_no=100

  with open(config.test_file_path,'r') as file:
    frame1_cords=io.readFileMd(file,frame1_no,frame_no_pos=config.frame_no_pos)
    frame2_cords=io.readFileMd(file,frame2_no,frame_no_pos=config.frame_no_pos)
  frame1_cords,frame2_cords=shift_origin.shiftOrigin(frame1_cords,frame2_cords,process='rotation')
  io.writeFile(file_path,frame1_cords)

def ringTrackTwoFramesSemiReal(ring_rpy=[0,0,0],track_rpy=[0,0,0],ring_translation=0,track_translation=0):
  output_file_path='test_systems/ring_track_two_frames_semi_real_system.xyz'
  x=[1,0,0]
  y=[0,1,0]
  z=[0,0,1]
  
  input_system_file_path='test_systems/ring_track_at_origin_semi_real_system.xyz'
  input_system_cords_df=io.readFile(input_system_file_path)
  frame1_initial_cords_df=input_system_cords_df.copy()
  #ring
  frame1_ring_cords_df=frame1_initial_cords_df[frame1_initial_cords_df['atom_no'].isin(config.ring_atom_no_list)]
  df=rotation.rotateAlongAxis(frame1_ring_cords_df,x,math.radians(ring_rpy[0]))
  df=rotation.rotateAlongAxis(df,y,math.radians(ring_rpy[1]))
  df=rotation.rotateAlongAxis(df,z,math.radians(ring_rpy[2]))
  frame2_initial_ring_cords_df=translation.translateAlongAxis(df,x,ring_translation)
  #track
  frame1_track_cords_df=frame1_initial_cords_df[frame1_initial_cords_df['atom_no'].isin(config.track_atom_no_list)]
  df=rotation.rotateAlongAxis(frame1_track_cords_df,x,math.radians(track_rpy[0]))
  df=rotation.rotateAlongAxis(df,y,math.radians(track_rpy[1]))
  df=rotation.rotateAlongAxis(df,z,math.radians(track_rpy[2]))
  frame2_initial_track_cords_df=translation.translateAlongAxis(df,x,track_translation)
  #frame2
  frame2_initial_cords_df=pd.concat([frame2_initial_ring_cords_df,frame2_initial_track_cords_df])

  #transform both frames
  axis=[-10.2,-42,-6]
  theta=60.5
  distance=5.3
  frame1_final_cords_df=rotation.rotateAlongAxis(frame1_initial_cords_df,axis,math.radians(theta))
  frame2_final_cords_df=rotation.rotateAlongAxis(frame2_initial_cords_df,axis,math.radians(theta))
  frame1_final_cords_df=translation.translateAlongAxis(frame1_final_cords_df,axis,distance)
  frame2_final_cords_df=translation.translateAlongAxis(frame2_final_cords_df,axis,distance)
  output_file=open(output_file_path,'w')
  io.writeFileMd(output_file,frame1_final_cords_df,0,frame_no_pos=config.frame_no_pos)
  io.writeFileMd(output_file,frame2_final_cords_df,1,frame_no_pos=config.frame_no_pos)
  output_file.close()

def extractFrames():
  '''
  Extract two frames
  '''
  output_file_path='test_systems/ring_track_two_frames_extracted_semi_real_system.xyz'
  frame1_no=0
  frame2_no=1000

  with open(config.test_file_path,'r') as file:
    frame1_cords=io.readFileMd(file,frame1_no,frame_no_pos=config.frame_no_pos)
    frame2_cords=io.readFileMd(file,frame2_no,frame_no_pos=config.frame_no_pos)
  frame1_cords,frame2_cords=shift_origin.shiftOrigin(frame1_cords,frame2_cords,process='rotation')
  with open(output_file_path,'w') as output_file:
    io.writeFileMd(output_file,frame1_cords_df,frame1_no,frame_no_pos=config.frame_no_pos)
    io.writeFileMd(output_file,frame2_cords_df,frame2_no,frame_no_pos=config.frame_no_pos)

def ringTrackMultiFrameSemiReal():
  '''
  its kinda ideal semi-real system
  '''
  output_file_path='test_systems/ring_track_multi_frame_semi_real_system.xyz'
  output_file=open(output_file_path,'w')
  x=[1,0,0]

  total_frames=100
  ring_theta=0
  track_theta=0
  ring_d_theta=1
  track_d_theta=0.5
  ring_distance=0
  track_distance=0
  ring_d_distance=0.1
  track_d_distance=-0.05

  input_system_file_path='test_systems/ring_track_at_origin_semi_real_system.xyz'
  input_system_cords_df=io.readFile(input_system_file_path)
  for curr_frame_no in range(total_frames):
    #ring
    input_system_ring_cords_df=input_system_cords_df[input_system_cords_df['atom_no'].isin(config.ring_atom_no_list)]
    df=rotation.rotateAlongAxis(input_system_ring_cords_df,x,math.radians(ring_theta))
    #df=rotation.rotateAlongAxis(df,y,math.radians(rpy[1]))
    #df=rotation.rotateAlongAxis(df,z,math.radians(rpy[2]))
    curr_frame_ring_cords_df=translation.translateAlongAxis(df,x,ring_distance)
    #track
    input_system_track_cords_df=input_system_cords_df[input_system_cords_df['atom_no'].isin(config.track_atom_no_list)]
    df=rotation.rotateAlongAxis(input_system_track_cords_df,x,math.radians(track_theta))
    #df=rotation.rotateAlongAxis(df,y,math.radians(rpy[1]))
    #df=rotation.rotateAlongAxis(df,z,math.radians(rpy[2]))
    curr_frame_track_cords_df=translation.translateAlongAxis(df,x,track_distance)
    #frame
    curr_frame_cords_df=pd.concat([curr_frame_ring_cords_df,curr_frame_track_cords_df])
    #transform frames
    axis=[1,1,1]
    theta=45.24
    distance=1.67
    curr_frame_cords_df=rotation.rotateAlongAxis(curr_frame_cords_df,axis,math.radians(theta))
    curr_frame_cords_df=translation.translateAlongAxis(curr_frame_cords_df,axis,distance)
    io.writeFileMd(output_file,curr_frame_cords_df,curr_frame_no,frame_no_pos=config.frame_no_pos)

    ring_theta+=ring_d_theta
    ring_distance+=ring_d_distance
    track_theta+=track_d_theta
    track_distance+=track_d_distance
  output_file.close()

def ringTrackMultiFrameOscillatingSemiReal():
  '''
  its kinda ideal semi-real system with oscillations
  '''
  output_file_path='test_systems/ring_track_multi_frame_oscillating_semi_real_system.xyz'
  output_file=open(output_file_path,'w')
  x=[1,0,0]
  y=[0,1,0]
  z=[0,0,1]
  total_frames=100
  ring_distance=0
  track_distance=0
  ring_d_distance=1
  track_d_distance=0.5
  ring_rpy=np.zeros(3)
  track_rpy=np.zeros(3)
  input_system_file_path='test_systems/ring_track_at_origin_semi_real_system.xyz'
  input_system_cords_df=io.readFile(input_system_file_path)
  for curr_frame_no in range(total_frames):
    #ring
    input_system_ring_cords_df=input_system_cords_df[input_system_cords_df['atom_no'].isin(config.ring_atom_no_list)]
    df=rotation.rotateAlongAxis(input_system_ring_cords_df,x,math.radians(ring_rpy[0]))
    df=rotation.rotateAlongAxis(df,y,math.radians(math.radians(ring_rpy[1])))
    df=rotation.rotateAlongAxis(df,z,math.radians(math.radians(ring_rpy[2])))
    curr_frame_ring_cords_df=translation.translateAlongAxis(df,x,ring_distance)
    #track
    input_system_track_cords_df=input_system_cords_df[input_system_cords_df['atom_no'].isin(config.track_atom_no_list)]
    df=rotation.rotateAlongAxis(input_system_track_cords_df,x,math.radians(track_rpy[0]))
    df=rotation.rotateAlongAxis(df,y,math.radians(track_rpy[1]))
    df=rotation.rotateAlongAxis(df,z,math.radians(track_rpy[2]))
    curr_frame_track_cords_df=translation.translateAlongAxis(df,x,track_distance)
    #frame
    curr_frame_cords_df=pd.concat([curr_frame_ring_cords_df,curr_frame_track_cords_df])
    #transform frames
    axis=[1,1,1]
    theta=45.24
    distance=1.67
    #curr_frame_cords_df=rotation.rotateAlongAxis(curr_frame_cords_df,axis,math.radians(theta))
    #curr_frame_cords_df=translation.translateAlongAxis(curr_frame_cords_df,axis,distance)
    io.writeFileMd(output_file,curr_frame_cords_df,curr_frame_no,frame_no_pos=config.frame_no_pos)

    #ring_rpy=np.random.random(3)
    if curr_frame_no%2==0:
      ring_distance=-1*ring_d_distance
    else:
      ring_distance=1*ring_d_distance
    #track_rpy=np.random.random(3)
    if curr_frame_no%2==0:
      track_distance=-1*track_d_distance
    else:
      track_distance=1*track_d_distance
  output_file.close()

def onlyRingGetComTestSystem(**kwargs):
  if 'input_file_path' in kwargs.keys():
    input_file_path=kwargs['input_file_path']
  else:
    input_file_path='/home/vanka/ruchi/molecular_motor/case_1/ring/scr_finished/coors.xyz'
  if 'output_file_path' in kwargs.keys():
    output_file_path=kwargs['output_file_path']
  else:
    output_file_path='test_systems/only_ring_get_com_test_system.xyz'
  if 'total_frames' in kwargs.keys():
    total_frames=kwargs['total_frames']
  else:
    total_frames=100
  if 'distance' in kwargs.keys():
    distance=kwargs['distance']
  else:
    distance=10

  velocity=distance/total_frames #Angs/step
  direction=np.random.randint(-10,10,size=(3,))
  print(f'Direction = {direction}\nDistance = {distance}')
  with open(input_file_path,'r') as file:
    input_frame_cords=io.readFileMd(file,0,frame_no_pos=config.frame_no_pos)
  
  _input_frame_cords=input_frame_cords
  output_file=open(output_file_path,'w')
  for curr_frame_no in tqdm(range(total_frames)):
    curr_frame_cords=translation.translateAlongAxis(_input_frame_cords,direction,velocity)
    _input_frame_cords=curr_frame_cords
    io.writeFileMd(output_file,curr_frame_cords,curr_frame_no,frame_no_pos=config.frame_no_pos)
  
  output_file.close()


if __name__=='__main__':
  #oneAtomSystemArtificial()
  #multiAtomSystemArtificial()
  #rpyOneAtomSystemArtificial()
  #ringCordsArtificial()
  #trackCordsArtificial()
  #ringTrackTwoFramesIdealArtificial()
 

  '''
  ringTrackAtOriginNonIdealArtificial()
  init.initConfig('test_systems/ring_track_at_origin_non_ideal_artificial_system.xyz',ring_atom_no=0,track_atom_no=30)
  ringTrackTwoFramesNonIdealArtificial()
  
  ringTwoFramesArtificial()
  '''


  #ringTrackMultiFrameIdealArtificial()
  #ringMultiFrameArtificial()
  '''
  ringTrackAtOriginSemiReal()
  init.initConfig(config.test_file_path,ring_atom_no=0,track_atom_no=153)
  ringTrackTwoFramesSemiReal()
  '''
  #ringTrackMultiFrameSemiReal()
  #ringTrackMultiFrameOscillatingSemiReal()

  #onlyRingGetComTestSystem(input_file_path='/home/vanka/ruchi/molecular_motor/case_1/ring/scr_finished/coors.xyz')
  ringTrackAtOriginIdealArtificial()
  init.initConfig('test_systems/ring_track_at_origin_ideal_artificial_system.xyz',ring_atom_no=0,track_atom_no=30)
  ringTrackMultiFrameIdealArtificial()
