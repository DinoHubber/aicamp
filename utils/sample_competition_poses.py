import os
import cv2
import random
import shutil

def rename_to_consistent():
    parent_dir = 'competition'
    count = 0
    for pose in os.listdir( parent_dir ):
        pose_dirp = os.path.join( parent_dir, pose )
        for pid in os.listdir( pose_dirp ):
            pid_dirp = os.path.join( pose_dirp, pid )
            for img in os.listdir( pid_dirp ):
                src_fp = os.path.join( pid_dirp, img )
                dst_fp = os.path.join( pid_dirp, '{}_{}_{}.png'.format(pose, pid, count) )
                count += 1
                print('renaming {} -> {}'.format(src_fp, dst_fp))
                os.rename( src_fp, dst_fp )

def count_imgs( pose_dirp ):
    img_count = 0
    for _, _, files in os.walk( pose_dirp ):
        img_count += len( [f for f in files if f.endswith('.png')] )
    return img_count

def sample_a_competition():
    parent_dir = 'competition'
    target_dir = 'competition_split'
    test_target_ratio = 0.2
    for pose in os.listdir( parent_dir ):
        target_pose_dir = os.path.join( target_dir, 'test' )
        target_pose_dir = os.path.join( target_pose_dir, pose )
        if not os.path.exists( target_pose_dir ):
            os.makedirs( target_pose_dir )

        pose_dirp = os.path.join( parent_dir, pose )
        posewise_imgs = count_imgs(pose_dirp)
        target_test_count = int( posewise_imgs * test_target_ratio )

        shuff_list = list(os.listdir( pose_dirp ))
        random.shuffle( shuff_list )
        curr_count = 0
        for pid in shuff_list:
            if curr_count >= target_test_count:
                target_pose_dir = os.path.join( target_dir, 'train' )
                target_pose_dir = os.path.join( target_pose_dir, pose )
                if not os.path.exists( target_pose_dir ):
                    os.makedirs( target_pose_dir )

            pid_dirp = os.path.join( pose_dirp, pid )
            src_tgt_pairs = [(os.path.join(pid_dirp, f), os.path.join(target_pose_dir, f)) for f in os.listdir( pid_dirp ) if f.endswith('.png')]
            curr_count += len( src_tgt_pairs )
            # perform a write to target_pose_dir
            for src_fp, tgt_fp in src_tgt_pairs:
                shutil.copyfile( src_fp, tgt_fp )

from collections import defaultdict

def groupby_pids_2(pose_dirp):
    pose_dict = defaultdict(list)
    img_names = os.listdir( pose_dirp )
    for img_name in img_names:
        pid, _ = img_name.split('_')
        pose_dict[pid].append( img_name )
    return pose_dict

def groupby_pids(pose_dirp):
    pose_dict = defaultdict(list)
    img_names = os.listdir( pose_dirp )
    for img_name in img_names:
        _, pid, _ = img_name.split('_')
        pose_dict[pid].append( img_name )
    return pose_dict

def sample_aicamp():
    parent_dir = 'P16SES'
    target_dir = 'TIL2019'
    # split_scheme = [(0.7,'train'), (0.1,'val'), (0.1,'publictest'), (0.1,'privatetest')]
    split_scheme = [(0.85,'train'), (0.15,'test')]
    for pose in os.listdir( parent_dir ):
        pose_dirp = os.path.join( parent_dir, pose )
        posewise_imgs = len(list(os.listdir(pose_dirp)))
        pose_dict = groupby_pids( pose_dirp )
        # shuff_list = list(os.listdir( pose_dirp ))
        shuff_list = list(pose_dict.keys())
        random.shuffle( shuff_list )

        idx = 0

        for ratio, split in split_scheme:
            target_pose_dir = os.path.join( target_dir, split )
            target_pose_dir = os.path.join( target_pose_dir, pose )
            if not os.path.exists( target_pose_dir ):
                os.makedirs( target_pose_dir )

            target_count = int( posewise_imgs * ratio )

            curr_count = 0
            while curr_count < target_count and idx < len(shuff_list):
            # for pid in shuff_list:
                # if curr_count >= target_test_count:
                #     target_pose_dir = os.path.join( target_dir, 'train' )
                #     target_pose_dir = os.path.join( target_pose_dir, pose )
                #     if not os.path.exists( target_pose_dir ):
                #         os.makedirs( target_pose_dir )
                pid = shuff_list[idx]

                # pid_dirp = os.path.join( pose_dirp, pid )
                src_tgt_pairs = [(os.path.join(pose_dirp, f), os.path.join(target_pose_dir, f)) for f in pose_dict[pid]]
                curr_count += len( src_tgt_pairs )
                # perform a write to target_pose_dir
                for src_fp, tgt_fp in src_tgt_pairs:
                    # print('copying {} to {}'.format(src_fp, tgt_fp))
                    shutil.copyfile( src_fp, tgt_fp )
                idx += 1
        while idx < len(shuff_list):
            pid = shuff_list[idx]

            pid_dirp = os.path.join( pose_dirp, pid )
            src_tgt_pairs = [(os.path.join(pose_dirp, f), os.path.join(target_pose_dir, f)) for f in pose_dict[pid]]
            # perform a write to target_pose_dir
            for src_fp, tgt_fp in src_tgt_pairs:
                # print('copying {} to {}'.format(src_fp, tgt_fp))
                shutil.copyfile( src_fp, tgt_fp )
            idx += 1

def sample_validation_set():
    train_folder = '/home/angeugn/Workspace/aicamp/data/TIL2019_v0.1/train'
    val_folder = '/home/angeugn/Workspace/aicamp/data/TIL2019_v0.1/val'
    ratio = 0.15

    for pose in os.listdir( train_folder ):
        pose_dirp = os.path.join( train_folder, pose )
        posewise_imgs = len(list(os.listdir(pose_dirp)))
        pose_dict = groupby_pids( pose_dirp )
        # shuff_list = list(os.listdir( pose_dirp ))
        shuff_list = list(pose_dict.keys())
        random.shuffle( shuff_list )

        idx = 0

        target_pose_dir = os.path.join( val_folder, pose )
        if not os.path.exists( target_pose_dir ):
            os.makedirs( target_pose_dir )

        target_count = int( posewise_imgs * ratio )

        curr_count = 0
        while curr_count < target_count and idx < len(shuff_list):
            pid = shuff_list[idx]

            src_tgt_pairs = [(os.path.join(pose_dirp, f), os.path.join(target_pose_dir, f)) for f in pose_dict[pid]]
            curr_count += len( src_tgt_pairs )
            # perform a write to target_pose_dir
            for src_fp, tgt_fp in src_tgt_pairs:
                # print('moving {} to {}'.format(src_fp, tgt_fp))
                shutil.move( src_fp, tgt_fp )
            idx += 1

def generate_train_val_split(source_folder, target_folder, ratio=0.15):
    # ratio = 0.15

    if os.path.exists( target_folder ):
        shutil.rmtree( target_folder )

    for pose in os.listdir( source_folder ):
        pose_dirp = os.path.join( source_folder, pose )
        posewise_imgs = len(list(os.listdir(pose_dirp)))
        pose_dict = groupby_pids( pose_dirp )
        # shuff_list = list(os.listdir( pose_dirp ))
        shuff_list = list(pose_dict.keys())
        random.shuffle( shuff_list )

        idx = 0

        target_pose_dir = os.path.join( '{}/val'.format(target_folder), pose )
        if not os.path.exists( target_pose_dir ):
            os.makedirs( target_pose_dir )

        target_count = int( posewise_imgs * ratio )

        curr_count = 0
        while curr_count < target_count and idx < len(shuff_list):
            pid = shuff_list[idx]

            src_tgt_pairs = [(os.path.join(pose_dirp, f), os.path.join(target_pose_dir, f)) for f in pose_dict[pid]]
            curr_count += len( src_tgt_pairs )
            # perform a write to target_pose_dir
            for src_fp, tgt_fp in src_tgt_pairs:
                # print('moving {} to {}'.format(src_fp, tgt_fp))
                shutil.copy( src_fp, tgt_fp )
            idx += 1

        target_pose_dir = os.path.join( '{}/train'.format(target_folder), pose )
        if not os.path.exists( target_pose_dir ):
            os.makedirs( target_pose_dir )
        while idx < len(shuff_list):
            pid = shuff_list[idx]

            src_tgt_pairs = [(os.path.join(pose_dirp, f), os.path.join(target_pose_dir, f)) for f in pose_dict[pid]]
            curr_count += len( src_tgt_pairs )
            # perform a write to target_pose_dir
            for src_fp, tgt_fp in src_tgt_pairs:
                # print('moving {} to {}'.format(src_fp, tgt_fp))
                shutil.copy( src_fp, tgt_fp )
            idx += 1

def split_into_og_curveball( tilfolder, target_folder ):
    from distutils.dir_util import copy_tree
    assert os.path.exists(tilfolder), 'source folder does not exist'
    # Assumes that the folder has train and test folders
    curveball_poses = ['Spiderman', 'ChestBump', 'EaglePose', 'HighKneel', 'LeopardCrawl']

    curveball_parent = os.path.join(target_folder, 'curveball')
    curveball_train = os.path.join(curveball_parent, 'train')
    curveball_test = os.path.join(curveball_parent, 'test')
    original_parent = os.path.join(target_folder, 'original')
    original_train = os.path.join(original_parent, 'train')
    original_test = os.path.join(original_parent, 'test')

    if not os.path.exists( curveball_train ):
        os.makedirs( curveball_train )
    if not os.path.exists( curveball_test ):
        os.makedirs( curveball_test )
    if not os.path.exists( original_train ):
        os.makedirs( original_train )
    if not os.path.exists( original_test ):
        os.makedirs( original_test )

    source_train = os.path.join( tilfolder, 'train' )
    original_poses = [pose for pose in os.listdir(source_train) if pose not in curveball_poses]
    for pose in original_poses:
        source_pose_path = os.path.join(source_train, pose)
        target_pose_path = os.path.join(original_train, pose)
        copy_tree( source_pose_path, target_pose_path )
    for pose in curveball_poses:
        source_pose_path = os.path.join(source_train, pose)
        target_pose_path = os.path.join(curveball_train, pose)
        copy_tree( source_pose_path, target_pose_path )

    source_test = os.path.join( tilfolder, 'test' )
    for pose in original_poses:
        source_pose_path = os.path.join(source_test, pose)
        target_pose_path = os.path.join(original_test, pose)
        copy_tree( source_pose_path, target_pose_path )
    for pose in curveball_poses:
        source_pose_path = os.path.join(source_test, pose)
        target_pose_path = os.path.join(curveball_test, pose)
        copy_tree( source_pose_path, target_pose_path )

def sample_pose_folders( source_folder, target_parent_folder, sample_name, pose_list, mgmt_dict, target_ratio, create_pose_folders=True, keep_img_names=True ):
    sample_folder = os.path.join( target_parent_folder, sample_name )
    curr_idx = 0
    for pose in pose_list:
        print(pose)
        target_pose_folder = os.path.join( sample_folder, pose ) if create_pose_folders else sample_folder
        if not os.path.exists( target_pose_folder ):
            os.makedirs( target_pose_folder )
        pose_path = os.path.join( source_folder, pose )
        pose_dict, full_count = mgmt_dict[pose]
        shuff_list = list(pose_dict.keys())
        # print(shuff_list)
        random.shuffle( shuff_list )
        # print(shuff_list)
        quota = int(target_ratio * full_count) if target_ratio is not None else None
        # print(quota)
        total_picked = 0

        while len(shuff_list) > 0 and (quota is None or total_picked < quota):
            pid = shuff_list.pop(0)
            pid_img_paths = pose_dict[pid]
            for pid_img in pid_img_paths:
                full_img_path = os.path.join( pose_path, pid_img )
                target_img_path = os.path.join( target_pose_folder, pid_img ) if keep_img_names else os.path.join( target_pose_folder, '{0:06}.png'.format(curr_idx) )
                shutil.copyfile( full_img_path, target_img_path )
                curr_idx += 1

                # print(full_img_path)
            total_picked += len( pid_img_paths )
            del pose_dict[pid]

def generate_real_competition( poses_folder, target_folder ):
    assert os.path.exists(poses_folder), 'source pose folder does not exist'

    all_poses = [pose for pose in os.listdir(poses_folder)]
    curveball_poses = ['Spiderman', 'ChestBump', 'EaglePose', 'HighKneel', 'LeopardCrawl']
    original_poses = [pose for pose in all_poses if pose not in curveball_poses]

    overall_dict = {}
    # construct a dictionary that maps pose: id: im_fp
    for pose in os.listdir( poses_folder ):
        pose_dirp = os.path.join( poses_folder, pose )
        num_pose_imgs = len(list(os.listdir(pose_dirp)))
        pose_dict = groupby_pids_2( pose_dirp )
        overall_dict[pose] = (pose_dict, num_pose_imgs)

    # train
    sample_pose_folders( source_folder=poses_folder,
                         target_parent_folder=target_folder, 
                         sample_name='0_train',
                         pose_list=original_poses,
                         mgmt_dict=overall_dict,
                         target_ratio=0.25,
                         create_pose_folders=True )

    # leaderboard1
    sample_pose_folders( source_folder=poses_folder,
                         target_parent_folder=target_folder, 
                         sample_name='1_leaderboard1',
                         pose_list=original_poses,
                         mgmt_dict=overall_dict,
                         target_ratio=0.15,
                         create_pose_folders=False )

    # curveball
    sample_pose_folders( source_folder=poses_folder,
                         target_parent_folder=target_folder, 
                         sample_name='2_curveball',
                         pose_list=curveball_poses,
                         mgmt_dict=overall_dict,
                         target_ratio=0.40,
                         create_pose_folders=True )

    # leaderboard2
    sample_pose_folders( source_folder=poses_folder,
                         target_parent_folder=target_folder, 
                         sample_name='3_leaderboard2',
                         pose_list=all_poses,
                         mgmt_dict=overall_dict,
                         target_ratio=0.15,
                         create_pose_folders=False )

    # finaltestset
    sample_pose_folders( source_folder=poses_folder,
                         target_parent_folder=target_folder, 
                         sample_name='4_finaltestset',
                         pose_list=all_poses,
                         mgmt_dict=overall_dict,
                         target_ratio=None,
                         create_pose_folders=False,
                         keep_img_names=False )

def annonimize_poses( poses_folder ):
    for pose in os.listdir( poses_folder ):
        pose_path = os.path.join( poses_folder, pose )
        for img in os.listdir(pose_path):
            img_path = os.path.join( pose_path, img )
            split_tokens = img.split('_')
            annon_img = '{}_{}'.format( split_tokens[1], split_tokens[2] )
            target_path = os.path.join( pose_path, annon_img )
            os.rename( img_path, target_path )


if __name__ == '__main__':
    source_folder = '/home/angeugn/Workspace/aicamp/data/P16SES'
    target_folder = 'TIL2019_v1.0'

    # annonimize_poses( source_folder )

    generate_real_competition( source_folder, target_folder )

    # split_into_og_curveball( source_folder, target_folder )


    # source_folder = '/home/angeugn/Workspace/aicamp/data/TIL2019_v0.1_yoloed/train'
    # target_folder = '/home/angeugn/Workspace/aicamp/data/TIL2019_v0.1_yoloed/split'
    # ratio = 0.15
    # generate_train_val_split(source_folder, target_folder, ratio)
    # sample_aicamp()
    # sample_validation_set()
    # sample_a_competition()
    # rename_to_consistent()


