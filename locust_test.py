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

def send_msg(self, source_mode, output_mode, content, input_language, output_language, test_name):
    if source_mode == "AUDIO" or source_mode == "VIDEO":
        self.payload_text['App']['sourceKey'] = content
    else:
        self.payload_text['App']['sourceText'] = content
    self.payload_text['App']['sourceMode'] = source_mode
    self.payload_text['App']['translationMode'] = output_mode
    self.payload_text['App']['sourceText'] = content
    self.payload_text['App']['sourceLanguage'] = input_language
    self.payload_text['App']['translationLanguage'] = output_language
    headers_text = {'content-type': 'application/json'}
    with self.client.post("/message", data=json.dumps(self.payload_text), headers=headers_text, name=test_name, catch_response=True) as response:
        if output_mode == "AVATAR":
            if 'translationAvatarVideo' not in json.loads(response.json()['MessageSynthesis']) or json.loads(response.json()['MessageSynthesis'])['translationAvatarVideo'] is None:
                response.failure("The Translation should be here but the field is not present")
        else:
            if 'translationText' not in json.loads(response.json()['IntermediateRepresentation']) or json.loads(response.json()['IntermediateRepresentation'])['translationText'] is None:
                response.failure("The Translation should be here but the field is not present")

def upload_obj(self, obj, extension):
    requestURL = {'appInstanceID': 'LOCUST', 'fileFormat': extension}
    headers_text = {'content-type': 'application/json'}
    with self.client.post('/inference-storage-auth', data=json.dumps(requestURL), headers=headers_text, name="Request presigned URL") as response:
        if response.status_code != 200:
            response.failure("Something went Wrong, the presigned URL was not generated")
        presignedURL = response.json()['PreSignedURL']
        objectName = response.json()['ObjectName']
    with open(obj, 'rb') as f:
        with self.client.put(presignedURL, data=f, catch_response=True, name="minio Upload") as response:
            if response.status_code != 200:
                response.failure("Something went Wrong, the object was not uploaded to the Minio Object Storage")
    return objectName

class SignONUser(HttpUser):

    wait_time = constant(1)

    payload_text = {
        'App': {
            'sourceKey': 'NONE',
            'sourceText': 'NONE',
            'sourceLanguage': 'NONE',
            'sourceMode': 'NONE',
            'sourceFileFormat': 'NONE',
            'sourceVideoCodec': 'NONE',
            'sourceVideoResolution': 'NONE',
            'sourceVideoFrameRate': -1,
            'sourceVideoPixelFormat': 'NONE',
            'sourceAudioCodec': 'NONE',
            'sourceAudioChannels': 'NONE',
            'sourceAudioSampleRate': -1,
            'translationLanguage': 'NONE',
            'translationMode': 'NONE',
            'appInstanceID': 'LOCUST',
            'T0App': datetime.datetime.utcnow().timestamp()*1000,
            'appVersion': '0.1.0',
            }
        }

    payload_text_elan = {
        'fileName': 'myFile',
        'fileFormat': 'm4a',
        'annotations': [
            {
                "time_start_ms": 1234,
                "time_stop_ms": 4321,
                "transcription": "Lorem Ipsum"
            }
        ],
        'metadata': {
            "sourceLanguage": "BFI",
            "annotationLanguage": "SPA",
            "messageType": "Social media post",
            "languageType": "Elicited",
            "register": "Semi-formal",
            "age": "18-30",
            "gender": "Male",
            "hearingStatus": "Deaf"
        }
    }

    payload_text_presignedURL_zip = {
        'hashPhoneNumber': 'LOCUST',
        'metadata': {
            "sourceLanguage": "BFI",
            "annotationLanguage": "SPA",
            "messageType": "Social media post",
            "languageType": "Elicited",
            "register": "Semi-formal",
            "age": "18-30",
            "gender": "Male",
            "hearingStatus": "Deaf"
        }
    }

    @task
    def text_message(self):
        languages = ['ENG', 'SPA', 'DUT', 'GLE']
        for input_language in languages:
            if input_language == 'ENG':
                input_text = "Garay sympathetically depicts a number of attitudes that at the time were considered shocking and even unnatural"
            elif input_language == 'SPA':
                input_text = "Garay mostró con naturalidad una serie de actitudes que en aquella época se consideraban escabrosas e incluso antinaturales"
            elif input_language == 'NLD':
                input_text = "Het gewenste type kan op de module zelf worden ingesteld met behulp van een draaiknop"
            elif input_language == 'GLD':
                input_text = input_text = "Déanfaimid ionchúisimh ina dhiaidh seo de réir mar is cuí"
            for output_language in languages:
                send_msg(self, "TEXT", "TEXT", input_text, input_language, output_language, "TEXT " + input_language + " TEXT " + output_language)
                send_msg(self, "TEXT", "AUDIO", input_text, input_language, output_language, "TEXT " + input_language + " AUDIO " + output_language)
            send_msg(self, "TEXT", "AVATAR", input_text, input_language, "DSE", "TEXT " + input_language + " AVATAR " + "DSE")

    # @task
    # def audio_message(self):
    #     languages = ['ENG', 'SPA', 'DUT', 'GLE']
    #     for input_language in languages:
    #         for output_language in languages:
    #             objectName = upload_obj(self, "../../minioUpload/51_53_55.wav", "wav")
    #             send_msg(self, "AUDIO", "TEXT", objectName, input_language, output_language, "AUDIO " + input_language + " TEXT " + output_language)
    #             objectName = upload_obj(self, "../../minioUpload/51_53_55.wav", "wav")
    #             send_msg(self, "AUDIO", "AUDIO", objectName, input_language, output_language, "AUDIO " + input_language + " AUDIO " + output_language)
                # objectName = upload_obj(self, "../../minioUpload/51_53_55.wav", "wav")
                # send_msg(self, "AUDIO", "AVATAR", objectName, input_language, output_language, "AUDIO " + input_language + " AVATAR " + output_language)

    # @task
    # def video_message(self):
    #     sign_languages = ['VGT', 'SSP', 'BFI', 'ISG', 'DSE']
    #     text_spoken_languages = ['ENG', 'SPA', 'DUT', 'GLE']
    #     for input_language in sign_languages:
    #         for output_language in text_spoken_languages:
    #             objectName = upload_obj(self, "../../minioUpload/test.MOV", "mov")
    #             send_msg(self, "VIDEO", "TEXT", objectName, input_language, output_language, "VIDEO " + input_language + " TEXT " + output_language)
    #             objectName = upload_obj(self, "../../minioUpload/test.MOV", "mov")
    #             send_msg(self, "VIDEO", "AUDIO", objectName, input_language, output_language, "VIDEO " + input_language + " AUDIO " + output_language)
    #     for input_language in sign_languages:
    #         for output_language in sign_languages:
    #             objectName = upload_obj(self, "../../minioUpload/test.MOV", "mov")
    #             send_msg(self, "VIDEO", "AVATAR", objectName, input_language, output_language, "VIDEO " + input_language + " AVATAR " + output_language)

    # @task
    # def send_contribution(self):
    #     headers_text = headers_text = {'content-type': 'application/json'}
    #     with self.client.post("/eaf-format", data=json.dumps(self.payload_text_elan), headers=headers_text, name="Create Elan File", catch_response=True) as response:
    #         elan_text = response.json()['eafData']
    #     f = open("../../minioUpload/elan_test.xml", "w")
    #     f.write(elan_text)
    #     f.close()
    #     with ZipFile("../../minioUpload/test_locust.zip", 'w') as zip_object:
    #         zip_object.write('../../minioUpload/elan_test.xml')
    #         zip_object.write('../../minioUpload/51_53_55.wav')
    #     headers_text = {'content-type': 'application/json'}
    #     with self.client.post('/dataset-storage-auth', data=json.dumps(self.payload_text_presignedURL_zip), headers=headers_text, name="Request presigned URL for ZIP") as response:
    #         if response.status_code != 200:
    #             response.failure("Something went Wrong, the presigned URL was not generated:\tStatus Code - " + str(response.status_code))
    #         presignedURL = response.json()['PreSignedURL']
    #         objectName = response.json()['ObjectName']
    #     with open("../../minioUpload/test_locust.zip", 'rb') as f:
    #         with self.client.put(presignedURL, data=f, catch_response=True, name="minio Upload for ZIP") as response:
    #             if response.status_code != 200:
    #                 response.failure("Something went Wrong, the object was not uploaded to the Minio Object Storage:\tStatus Code - " + str(response.status_code))
