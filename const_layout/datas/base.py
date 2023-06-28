import torch
import seaborn as sns
import os
from pathlib import Path
from torch_geometric.data import InMemoryDataset


class BaseDataset(InMemoryDataset):
    labels = []
    _label2index = None
    _index2label = None
    _colors = None

    def __init__(self, name, split, transform):
        assert split in ['train', 'val', 'test']
        dir_path = os.path.dirname(os.path.realpath(__file__))
        super().__init__(os.path.join(dir_path, "dataset", name), transform)
        idx = self.processed_file_names.index('{}.pt'.format(split))
        self.data, self.slices = torch.load(self.processed_paths[idx])

    @property
    def label2index(self):
        if self._label2index is None:
            self._label2index = dict()
            for idx, label in enumerate(self.labels):
                self._label2index[label] = idx
        return self._label2index

    @property
    def index2label(self):
        if self._index2label is None:
            self._index2label = dict()
            for idx, label in enumerate(self.labels):
                self._index2label[idx] = label
        return self._index2label

    @property
    def colors(self):
        if self._colors is None:
            n_colors = self.num_classes

            palette = sns.color_palette(None, n_colors)
            if n_colors > 10:
                palette[10:] = sns.color_palette("husl", n_colors-10)
    
            self._colors = [[int(x[0]*255), int(x[1]*255), int(x[2]*255)] for x in palette]

            # colors = sns.color_palette('husl', n_colors=n_colors)
            # self._colors = [tuple(map(lambda x: int(x * 255), c))
            #                 for c in colors]
        return self._colors

    @property
    def raw_file_names(self):
        raw_dir = Path(self.raw_dir)
        if not raw_dir.exists():
            return []
        return [p.name for p in raw_dir.iterdir()]

    @property
    def processed_file_names(self):
        return ['train.pt', 'val.pt', 'test.pt']

    def download(self):
        raise FileNotFoundError('See data/README.md to prepare dataset')

    def process(self):
        raise NotImplementedError
