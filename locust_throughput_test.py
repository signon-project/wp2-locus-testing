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
from locust import HttpUser, TaskSet, task, constant
import requests
from zipfile import ZipFile
import os
import csv

class SignONUser(HttpUser):

    def write_to_csv(self, data_row, testname):
        csv_file_name = "/throughput_test_times/"+testname+"_timestamps.csv"
        with open(csv_file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data_row)

    def getTime(self):
        return round((time.time() * 1000))

    def send_receive(self, payload_text, testname):
        headers_text = {'content-type': 'application/json'}

        with self.client.post("/message", data=json.dumps(payload_text), headers=headers_text, name=testname, catch_response=True) as response:
            if response.json()['App']['translationMode'] != 'AVATAR' and ('translationText' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['translationText'] is None):
                response.failure("TEST FAILED!!")
            elif response.json()['App']['translationMode'] == 'AVATAR' and ('glosses' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['glosses'] is None):
                response.failure("TEST FAILED!!")
            else:
                r = response.json()
                T6App = self.getTime()
                T0App = r['App']['T0App']
                T1Orchestrator = r['OrchestratorRequest']['T1Orchestrator']
                T2WP3 = json.loads(r['SourceLanguageProcessing'])['T2WP3']
                T3WP4 = json.loads(r['IntermediateRepresentation'])['T3WP4']
                T4WP5 = json.loads(r['MessageSynthesis'])['T4WP5']
                T5Orchestrator = r['OrchestratorResponse']['T5Orchestrator']

                T0_T6 = T6App - T0App
                T0_T1 = T1Orchestrator - T0App
                T1_T2 = T2WP3 - T1Orchestrator
                T2_T3 = T3WP4 - T2WP3
                T3_T5 = T5Orchestrator - T3WP4
                T5_T6 = T6App - T5Orchestrator

                response_time = [int(T0_T6), int(T0_T1), int(T1_T2), int(T2_T3), int(T3_T5), int(abs(T5_T6) + 1)]

                self.write_to_csv(response_time, testname)



    def text2text(self):
        testname = "TEXT_DUT_2_TEXT_SPA"
        payload_text = {
        'App': {
            'sourceKey': 'NONE',
            'sourceText': 'Hallo, leuk je te ontmoeten',
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

    def audio2text(self):
        testname = "AUDIO_ENG_2_TEXT_ENG2"
        payload_text = {
        'App': {
            'sourceKey': 'ASR-test/ENG.m4a',
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
            'translationLanguage': 'ENG',
            'translationMode': 'TEXT',
            'appInstanceID': 'ASR-test',
            'T0App': self.getTime(),
            'appVersion': '1.0.0',
            }
        }

        self.send_receive(payload_text, testname)

    def video2text(self):
        testname = "VIDEO_ISG_2_TEXT_DUT"
        payload_text = {
        'App': {
            'sourceKey': 'SL-test/ISG2.mov',
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

    def text2avatar(self):
        testname = "TEXT_DUT_2_AVATAR_DSE"
        payload_text = {
        'App': {
            'sourceKey': 'NONE',
            'sourceText': 'Hallo, leuk je te ontmoeten',
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

    def audio2avatar(self):
        testname = "AUDIO_ENG_2_AVATAR_DSE"
        payload_text = {
        'App': {
            'sourceKey': 'ASR-test/ENG.m4a',
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

    def video2avatar(self):
        testname = "VIDEO_DSE_2_AVATAR_DSE"
        payload_text = {
        'App': {
            'sourceKey': 'SL-test/DSE.mp4',
            'sourceText': 'NONE',
            'sourceLanguage': 'DSE',
            'sourceMode': 'VIDEO',
            'sourceFileFormat': 'mp4',
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
    def throughputTest(self):
        # self.text2text()
        self.audio2text()
        # self.video2text()
        # self.text2avatar()
        # self.audio2avatar()
        # self.video2avatar()

