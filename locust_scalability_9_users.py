# Copyright 2021-2023 FINCONS GROUP AG within the Horizon 2020
# European project SignON under grant agreement no. 101017255.

# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 

#     http://www.apache.org/licenses/LICENSE-2.0 

# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

import datetime, time, json
from locust import HttpUser, TaskSet, task, constant, LoadTestShape
import requests
from zipfile import ZipFile
import os
import csv

class SignONUser_text2text(HttpUser):

    def getTime(self):
        return round((time.time() * 1000))

    def send_receive(self, payload_text, testname):
        headers_text = {'content-type': 'application/json'}

        with self.client.post("/message", data=json.dumps(payload_text), headers=headers_text, name=testname, catch_response=True) as response:
            try:
                if response.json()['App']['translationMode'] != 'AVATAR' and ('translationText' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['translationText'] is None):
                    response.failure("TEST FAILED!! - " + testname + " Timeout Failure.")
                elif response.json()['App']['translationMode'] == 'AVATAR' and ('glosses' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['glosses'] is None):
                    response.failure("TEST FAILED!! - " + testname + " Timeout Failure.")
                else:
                    r = response.json()
            except:
                print(response)
                response.failure("TEST FAILED!! - " + testname + str(response))

        time.sleep(1)


    def text2text(self):
        testname = "TEXT_2_TEXT"
        payload_text = {
        'App': {
            'sourceKey': 'NONE',
            'sourceText': '***********',
            'sourceLanguage': 'DUT',
            'sourceMode': 'TEXT',
            'sourceFileFormat': 'NONE',
            'sourceVideoCodec': 'NONE',
            'sourceVideoResolution': 'NONE',
            'sourceVideoFrameRate': -1,
            'sourceVideoPixelFormat': 'NONE',
            'sourceAudioCodec': 'NONE',
            'sourceAudioChannels': 'NONE',
            'sourceAudioSampleRate': -1,
            'translationLanguage': 'SPA',
            'translationMode': 'TEXT',
            'appInstanceID': 'wp2test',
            'T0App': self.getTime(),
            'appVersion': '1.0.0',
            }
        }

        self.send_receive(payload_text, testname)

    @task
    def test_text2text(self):
        self.text2text()

class SignONUser_audio2text(HttpUser):

    def getTime(self):
        return round((time.time() * 1000))

    def send_receive(self, payload_text, testname):
        headers_text = {'content-type': 'application/json'}

        with self.client.post("/message", data=json.dumps(payload_text), headers=headers_text, name=testname, catch_response=True) as response:
            try:
                if response.json()['App']['translationMode'] != 'AVATAR' and ('translationText' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['translationText'] is None):
                    response.failure("TEST FAILED!! - " + testname + " Timeout Failure.")
                elif response.json()['App']['translationMode'] == 'AVATAR' and ('glosses' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['glosses'] is None):
                    response.failure("TEST FAILED!! - " + testname + " Timeout Failure.")
                else:
                    r = response.json()
            except:
                print(response)
                response.failure("TEST FAILED!! - " + testname + str(response))

        time.sleep(1)

    def audio2text(self):
        testname = "AUDIO_2_TEXT"
        payload_text = {
        'App': {
            'sourceKey': '***************',
            'sourceText': 'NONE',
            'sourceLanguage': 'ENG',
            'sourceMode': 'AUDIO',
            'sourceFileFormat': 'm4a',
            'sourceVideoCodec': 'NONE',
            'sourceVideoResolution': 'NONE',
            'sourceVideoFrameRate': -1,
            'sourceVideoPixelFormat': 'NONE',
            'sourceAudioCodec': 'NONE',
            'sourceAudioChannels': 'NONE',
            'sourceAudioSampleRate': -1,
            'translationLanguage': 'SPA',
            'translationMode': 'TEXT',
            'appInstanceID': 'ASR-test',
            'T0App': self.getTime(),
            'appVersion': '1.0.0',
            }
        }

        self.send_receive(payload_text, testname)

    @task
    def test_audio2text(self):
        self.audio2text()

class SignONUser_video2text(HttpUser):

    def getTime(self):
        return round((time.time() * 1000))

    def send_receive(self, payload_text, testname):
        headers_text = {'content-type': 'application/json'}

        with self.client.post("/message", data=json.dumps(payload_text), headers=headers_text, name=testname, catch_response=True) as response:
            try:
                if response.json()['App']['translationMode'] != 'AVATAR' and ('translationText' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['translationText'] is None):
                    response.failure("TEST FAILED!! - " + testname + " Timeout Failure.")
                elif response.json()['App']['translationMode'] == 'AVATAR' and ('glosses' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['glosses'] is None):
                    response.failure("TEST FAILED!! - " + testname + " Timeout Failure.")
                else:
                    r = response.json()
            except:
                print(response)
                response.failure("TEST FAILED!! - " + testname + str(response))

        time.sleep(1)

    def video2text(self):
        testname = "VIDEO_2_TEXT"
        payload_text = {
        'App': {
            'sourceKey': '***********',
            'sourceText': 'NONE',
            'sourceLanguage': 'ISG',
            'sourceMode': 'VIDEO',
            'sourceFileFormat': 'mov',
            'sourceVideoCodec': 'NONE',
            'sourceVideoResolution': 'NONE',
            'sourceVideoFrameRate': -1,
            'sourceVideoPixelFormat': 'NONE',
            'sourceAudioCodec': 'NONE',
            'sourceAudioChannels': 'NONE',
            'sourceAudioSampleRate': -1,
            'translationLanguage': 'DUT',
            'translationMode': 'TEXT',
            'appInstanceID': 'SL-test',
            'T0App': self.getTime(),
            'appVersion': '1.0.0',
            }
        }

        self.send_receive(payload_text, testname)

    @task
    def test_video2text(self):
        self.video2text()

class SignONUser_text2audio(HttpUser):

    def getTime(self):
        return round((time.time() * 1000))

    def send_receive(self, payload_text, testname):
        headers_text = {'content-type': 'application/json'}

        with self.client.post("/message", data=json.dumps(payload_text), headers=headers_text, name=testname, catch_response=True) as response:
            try:
                if response.json()['App']['translationMode'] != 'AVATAR' and ('translationText' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['translationText'] is None):
                    response.failure("TEST FAILED!! - " + testname + " Timeout Failure.")
                elif response.json()['App']['translationMode'] == 'AVATAR' and ('glosses' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['glosses'] is None):
                    response.failure("TEST FAILED!! - " + testname + " Timeout Failure.")
                else:
                    r = response.json()
            except:
                print(response)
                response.failure("TEST FAILED!! - " + testname + str(response))

        time.sleep(1)

    def text2audio(self):
        testname = "TEXT_2_AUDIO"
        payload_text = {
        'App': {
            'sourceKey': 'NONE',
            'sourceText': '*********************',
            'sourceLanguage': 'DUT',
            'sourceMode': 'TEXT',
            'sourceFileFormat': 'NONE',
            'sourceVideoCodec': 'NONE',
            'sourceVideoResolution': 'NONE',
            'sourceVideoFrameRate': -1,
            'sourceVideoPixelFormat': 'NONE',
            'sourceAudioCodec': 'NONE',
            'sourceAudioChannels': 'NONE',
            'sourceAudioSampleRate': -1,
            'translationLanguage': 'ENG',
            'translationMode': 'AUDIO',
            'appInstanceID': 'wp2test',
            'T0App': self.getTime(),
            'appVersion': '1.0.0',
            }
        }

        self.send_receive(payload_text, testname)

    @task
    def test_text2audio(self):
        self.text2audio()

class SignONUser_audio2audio(HttpUser):

    def getTime(self):
        return round((time.time() * 1000))

    def send_receive(self, payload_text, testname):
        headers_text = {'content-type': 'application/json'}

        with self.client.post("/message", data=json.dumps(payload_text), headers=headers_text, name=testname, catch_response=True) as response:
            try:
                if response.json()['App']['translationMode'] != 'AVATAR' and ('translationText' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['translationText'] is None):
                    response.failure("TEST FAILED!! - " + testname + " Timeout Failure.")
                elif response.json()['App']['translationMode'] == 'AVATAR' and ('glosses' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['glosses'] is None):
                    response.failure("TEST FAILED!! - " + testname + " Timeout Failure.")
                else:
                    r = response.json()
            except:
                print(response)
                response.failure("TEST FAILED!! - " + testname + str(response))

        time.sleep(1)

    def audio2audio(self):
        testname = "AUDIO_2_AUDIO"
        payload_text = {
        'App': {
            'sourceKey': '*************',
            'sourceText': 'NONE',
            'sourceLanguage': 'ENG',
            'sourceMode': 'AUDIO',
            'sourceFileFormat': 'm4a',
            'sourceVideoCodec': 'NONE',
            'sourceVideoResolution': 'NONE',
            'sourceVideoFrameRate': -1,
            'sourceVideoPixelFormat': 'NONE',
            'sourceAudioCodec': 'NONE',
            'sourceAudioChannels': 'NONE',
            'sourceAudioSampleRate': -1,
            'translationLanguage': 'DUT',
            'translationMode': 'AUDIO',
            'appInstanceID': 'ASR-test',
            'T0App': self.getTime(),
            'appVersion': '1.0.0',
            }
        }

        self.send_receive(payload_text, testname)

    @task
    def test_audio2audio(self):
        self.audio2audio()

class SignONUser_video2audio(HttpUser):

    def getTime(self):
        return round((time.time() * 1000))

    def send_receive(self, payload_text, testname):
        headers_text = {'content-type': 'application/json'}

        with self.client.post("/message", data=json.dumps(payload_text), headers=headers_text, name=testname, catch_response=True) as response:
            try:
                if response.json()['App']['translationMode'] != 'AVATAR' and ('translationText' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['translationText'] is None):
                    response.failure("TEST FAILED!! - " + testname + " Timeout Failure.")
                elif response.json()['App']['translationMode'] == 'AVATAR' and ('glosses' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['glosses'] is None):
                    response.failure("TEST FAILED!! - " + testname + " Timeout Failure.")
                else:
                    r = response.json()
            except:
                print(response)
                response.failure("TEST FAILED!! - " + testname + str(response))

        time.sleep(1)

    def video2audio(self):
        testname = "VIDEO_2_AUDIO"
        payload_text = {
        'App': {
            'sourceKey': '*****************',
            'sourceText': 'NONE',
            'sourceLanguage': 'ISG',
            'sourceMode': 'VIDEO',
            'sourceFileFormat': 'mov',
            'sourceVideoCodec': 'NONE',
            'sourceVideoResolution': 'NONE',
            'sourceVideoFrameRate': -1,
            'sourceVideoPixelFormat': 'NONE',
            'sourceAudioCodec': 'NONE',
            'sourceAudioChannels': 'NONE',
            'sourceAudioSampleRate': -1,
            'translationLanguage': 'DSE',
            'translationMode': 'AVATAR',
            'appInstanceID': 'wp2test',
            'T0App': self.getTime(),
            'appVersion': '1.0.0',
            }
        }

        self.send_receive(payload_text, testname)

    @task
    def test_video2audio(self):
        self.video2audio()

class SignONUser_text2avatar(HttpUser):

    def getTime(self):
        return round((time.time() * 1000))

    def send_receive(self, payload_text, testname):
        headers_text = {'content-type': 'application/json'}

        with self.client.post("/message", data=json.dumps(payload_text), headers=headers_text, name=testname, catch_response=True) as response:
            try:
                if response.json()['App']['translationMode'] != 'AVATAR' and ('translationText' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['translationText'] is None):
                    response.failure("TEST FAILED!! - " + testname + " Timeout Failure.")
                elif response.json()['App']['translationMode'] == 'AVATAR' and ('glosses' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['glosses'] is None):
                    response.failure("TEST FAILED!! - " + testname + " Timeout Failure.")
                else:
                    r = response.json()
            except:
                print(response)
                response.failure("TEST FAILED!! - " + testname + str(response))

        time.sleep(1)

    def text2avatar(self):
        testname = "TEXT_2_AVATAR"
        payload_text = {
        'App': {
            'sourceKey': 'NONE',
            'sourceText': '*********************',
            'sourceLanguage': 'DUT',
            'sourceMode': 'TEXT',
            'sourceFileFormat': 'NONE',
            'sourceVideoCodec': 'NONE',
            'sourceVideoResolution': 'NONE',
            'sourceVideoFrameRate': -1,
            'sourceVideoPixelFormat': 'NONE',
            'sourceAudioCodec': 'NONE',
            'sourceAudioChannels': 'NONE',
            'sourceAudioSampleRate': -1,
            'translationLanguage': 'DSE',
            'translationMode': 'AVATAR',
            'appInstanceID': 'wp2test',
            'T0App': self.getTime(),
            'appVersion': '1.0.0',
            }
        }

        self.send_receive(payload_text, testname)

    @task
    def test_text2avatar(self):
        self.text2avatar()

class SignONUser_audio2avatar(HttpUser):

    def getTime(self):
        return round((time.time() * 1000))

    def send_receive(self, payload_text, testname):
        headers_text = {'content-type': 'application/json'}

        with self.client.post("/message", data=json.dumps(payload_text), headers=headers_text, name=testname, catch_response=True) as response:
            try:
                if response.json()['App']['translationMode'] != 'AVATAR' and ('translationText' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['translationText'] is None):
                    response.failure("TEST FAILED!! - " + testname + " Timeout Failure.")
                elif response.json()['App']['translationMode'] == 'AVATAR' and ('glosses' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['glosses'] is None):
                    response.failure("TEST FAILED!! - " + testname + " Timeout Failure.")
                else:
                    r = response.json()
            except:
                print(response)
                response.failure("TEST FAILED!! - " + testname + str(response))

        time.sleep(1)

    def audio2avatar(self):
        testname = "AUDIO_2_AVATAR"
        payload_text = {
        'App': {
            'sourceKey': '*************',
            'sourceText': 'NONE',
            'sourceLanguage': 'ENG',
            'sourceMode': 'AUDIO',
            'sourceFileFormat': 'm4a',
            'sourceVideoCodec': 'NONE',
            'sourceVideoResolution': 'NONE',
            'sourceVideoFrameRate': -1,
            'sourceVideoPixelFormat': 'NONE',
            'sourceAudioCodec': 'NONE',
            'sourceAudioChannels': 'NONE',
            'sourceAudioSampleRate': -1,
            'translationLanguage': 'DSE',
            'translationMode': 'AVATAR',
            'appInstanceID': 'ASR-test',
            'T0App': self.getTime(),
            'appVersion': '1.0.0',
            }
        }

        self.send_receive(payload_text, testname)

    @task
    def test_audio2avatar(self):
        self.audio2avatar()

class SignONUser_video2avatar(HttpUser):

    def getTime(self):
        return round((time.time() * 1000))

    def send_receive(self, payload_text, testname):
        headers_text = {'content-type': 'application/json'}

        with self.client.post("/message", data=json.dumps(payload_text), headers=headers_text, name=testname, catch_response=True) as response:
            try:
                if response.json()['App']['translationMode'] != 'AVATAR' and ('translationText' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['translationText'] is None):
                    response.failure("TEST FAILED!! - " + testname + " Timeout Failure.")
                elif response.json()['App']['translationMode'] == 'AVATAR' and ('glosses' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['glosses'] is None):
                    response.failure("TEST FAILED!! - " + testname + " Timeout Failure.")
                else:
                    r = response.json()
            except:
                print(response)
                response.failure("TEST FAILED!! - " + testname + str(response))

        time.sleep(1)

    def video2avatar(self):
        testname = "VIDEO_2_AVATAR"
        payload_text = {
        'App': {
            'sourceKey': '*****************',
            'sourceText': 'NONE',
            'sourceLanguage': 'ISG',
            'sourceMode': 'VIDEO',
            'sourceFileFormat': 'mov',
            'sourceVideoCodec': 'NONE',
            'sourceVideoResolution': 'NONE',
            'sourceVideoFrameRate': -1,
            'sourceVideoPixelFormat': 'NONE',
            'sourceAudioCodec': 'NONE',
            'sourceAudioChannels': 'NONE',
            'sourceAudioSampleRate': -1,
            'translationLanguage': 'DSE',
            'translationMode': 'AVATAR',
            'appInstanceID': 'wp2test',
            'T0App': self.getTime(),
            'appVersion': '1.0.0',
            }
        }

        self.send_receive(payload_text, testname)

    @task
    def test_video2avatar(self):
        self.video2avatar()

class StagesShapeWithCustomUsers(LoadTestShape):
    stages = [
        {"duration": 300, "users": 1000, "spawn_rate": 0.1, "user_classes": [SignONUser_text2text, SignONUser_text2audio, SignONUser_text2avatar,
                                                                             SignONUser_audio2text, SignONUser_audio2audio, SignONUser_audio2avatar,
                                                                             SignONUser_video2text, SignONUser_video2audio, SignONUser_video2avatar]},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                try:
                    tick_data = (stage["users"], stage["spawn_rate"], stage["user_classes"])
                except:
                    tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None

