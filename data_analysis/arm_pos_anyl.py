import bpy
import csv


def data_handler(scene):
    frame_text = "Frame " + str(scene.frame_current)
    
    # get data
    vert_1_pos = scene.objects['vert_1_pos_Text'].data.body
    vert_1_pos_influance = scene.objects['vert_1_mv_ratio_Text'].data.body
    tendon_pull_distance = scene.objects['ctrl_dist_Text'].data.body
    
    position_data = str(vert_1_pos) + "," + str(tendon_pull_distance)
    position_data.encode('utf8')
    position_data = position_data.replace("\n","")
    
    scene.objects['output_text'].data.body = str(frame_text)
    
    # write to file
    csv_data_file = ("C:\\Users\\Jason\\Documents\\head_robotics\\open-tentacle\\0.1.1\\data\\open_tendon_videos\\1st_movment_study\\visual_arm_movement.csv")
    file = open(csv_data_file, 'a')
    file.write(position_data+'\n')
    file.close()

bpy.app.handlers.frame_change_pre.append(data_handler)
#bpy.app.handlers.frame_change_pre.remove(data_handler)