from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder


class ActionEncoder():
    """
        Class that will be used to encode all the key into
        One Hot Encoder and Label Encoder (map integer into action key)
    """

    def __init__(self):
        self.dict_act_key_to_mirror_key = {}
        self.dict_index_act_to_mirror_index = {}

    def fit(self, list_all_action):
        """
        Fit the encoder of Label Encoder. So it can map an integer to an action key.
        Also fit the One Hot Encoder.
        :param list_all_action: list of all possible action keys in the game
        :return:
        """
        self.le = preprocessing.LabelEncoder()
        list_all_action = self.le.fit_transform(list_all_action)
        self.shape_all_actions = len(list_all_action)
        self.onehot_encoder = OneHotEncoder(self.shape_all_actions, sparse=False)
        list_all_action = list_all_action.reshape(len(list_all_action), 1)
        self.onehot_encoder.fit(list_all_action)
        self.create_mirror_dict()

    def transform(self, data):
        """
        Transform the action key into one hot encoder
        :param data: action key
        :return:
        """
        data = self.le.transform(data)
        data = data.reshape(len(data), 1)
        data = self.onehot_encoder.transform(data)
        return data

    def inverse_transform(self, data):
        """
        Transform the integer into the action key based on the dictionary
        fitted in the Label Encoder.
        :param data: int, an encoded label integer
        :return: action key
        """
        data = self.le.inverse_transform(data)
        return data

    def create_mirror_dict(self):
        """
        Create the dictionary of the index action's which maps the encoded action into
        its encoded mirror action

        :return:
        """
        for i in self.le.classes_:
            all_act = self.le.classes_
            from util.state_modifier_util import get_key_mirror_action
            import numpy as np
            self.dict_act_key_to_mirror_key[i] = get_key_mirror_action(i)
            index_orig = np.where(all_act == i)[0][0]
            index_mirror = np.where(all_act == get_key_mirror_action(i))
            self.dict_index_act_to_mirror_index[index_orig] = index_mirror[0].tolist()

    def array_mirrored(self, array):
        """
        Mirror the index of the array that has the shape of the list of action which
         represent the encoded action key into
        the index of its opposite action key.

        :param array:
        :return:
        """
        import numpy as np
        new_array = np.zeros_like(array)
        index_np = np.where(array > 0)[0]
        new_index = []
        for z in index_np:
            new_index.append(self.dict_index_act_to_mirror_index[int(z)][0])
        new_index = np.array(new_index)
        new_array[new_index] = array[index_np]
        return new_array