# vim: tabstop=4 shiftwidth=4 softtabstop=4

# copyright [2013] [Vitalii Lebedynskyi]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json


def to_json(key, value, **kwargs):
    d = {key: value}

    if kwargs:
        d.update(kwargs)

    return json.dumps(d, allow_nan=False, cls=ResponseEncoder)


class JsonSerializable(object):
    def get_values(self):
        values = self.__dict__
        keys = self.get_values_keys()
        d = {v: values[v] for v in values.keys() if
             v in keys and values[v] is not None}
        return d

    def get_values_keys(self):
        raise NotImplementedError("get_values_keys not implemented")


class ResponseEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, JsonSerializable):
            return o.get_values()

        if isinstance(o, BaseException):
            return str(o)

        return o