import os
from argparse import ArgumentParser
from datetime import datetime
import torch
from torch_geometric.data import Data
# from model import *
# from dataset import *
from metrics import *
import tqdm


def get_cur_time():
    return datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M')


def process_file_list(raw_data_dir, processed_data_dir, las_data_list, has_data_list):
    for las_data_name, has_data_name in tqdm(las_data_list, has_data_list):
        las_data = np.load(os.path.join(raw_data_dir, 'las', las_data_name))
        has_data = np.load(os.path.join(raw_data_dir, 'has', has_data_name))

        str1, str2, str3, str4 = las_data_name.split('_')
        mesh_name = str1 + '_' + str2 + '.npz'
        mesh_data = np.load(os.path.join(raw_data_dir, 'mesh', mesh_name))
        node_data = np.zeros(3)
        val_data = np.zeros(3)
        for j in range(len(mesh_data['x'])):
            node_data[0] = las_data['ux'][j]
            node_data[1] = las_data['uy'][j]
            node_data[2] = las_data['p'][j]

            val_data[0] = has_data['ux'][j]
            val_data[1] = has_data['uy'][j]
            val_data[2] = has_data['p'][j]

            if j == 0:
                node_data_list = np.array([node_data])
                val_data_list = np.array([val_data])
            else:
                node_data_list = np.append(node_data_list, np.array([node_data]), axis=0)
                val_data_list = np.append(val_data_list, np.array([val_data]), axis=0)

        node_data_list = torch.tensor(node_data_list, dtype=torch.float)
        val_data_list = torch.tensor(val_data_list, dtype=torch.float)
        edge_index = np.array(mesh_data['edges'])
        edge_index = torch.tensor(edge_index, dtype=torch.long)
        edge_attr = np.array(mesh_data['edge_properties'])
        edge_attr = torch.tensor(edge_attr, dtype=torch.float)

        node_pos = np.zeros(2)
        for j in range(len(mesh_data['x'])):
            node_pos[0] = mesh_data['x'][j]
            node_pos[1] = mesh_data['y'][j]

            if j == 0:
                node_pos_list = np.array([node_pos])
            else:
                node_pos_list = np.append(node_pos_list, np.array([node_pos]), axis=0)

        node_pos_list = torch.tensor(node_pos_list, dtype=torch.float)

        data = Data(x=node_data_list, y=val_data_list, edge_index=edge_index.t().contiguous(), edge_attr=edge_attr, pos=node_pos_list)
        data_name = str1 + '_' + str2 + '_' + str4
        torch.save(data, os.path.join(processed_data_dir, data_name + '.pt'))

