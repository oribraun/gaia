import json
import random
import requests
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from .base_api import BaseUserAuthApi
from new_app.api.jsonResponse import baseHttpResponse
from new_app.app_models.company import Company
from new_app.app_models.user_prompt import UserPrompt
import openai
import time
import math
import os


class ChatGptApi(BaseUserAuthApi):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        response = baseHttpResponse()
        return JsonResponse(response.dict(), safe=False)

    def post_old(self, request, format=None):
        prompt = request.data['prompt']
        ip_address = self.get_client_ip(request=request)
        user = request.user
        company = user.company
        # if not company:
        #     UserPrompt.objects.create(user=request.user, prompt=prompt, ip_address=ip_address)

        # user_prompt.save()
        # print('user_prompt', user_prompt.user)
        # all_users_prompt = UserPrompt.objects.all()
        # user_prompt = UserPrompt.objects.filter(user=request.user)
        # print('all_users_prompt', all_users_prompt.values())
        # print('user_prompt', user_prompt.values())
        answer = self.askChatGpt(prompt)

        return JsonResponse({
            'err': 0,
            'errMessage': '',
            'data': {
                'answer': answer
            }
        }, safe=False)

    def askChatGpt(self, prompt):
        openai.api_key = os.environ['OPEN_AI_KEY']
        # inp = 'Multiple layers above the Generative AI services which will help businesses unlock the full potential of generative AI while'
        # prompt = f'expand: {inp}'
        words_length = prompt.split(' ')
        chars = len(prompt)

        # https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them
        token_count = math.ceil(len(prompt) / 4)
        print('token_count', token_count)
        max_tokens = 4000 - token_count
        result = ''
        try:
            res = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0,
                n=1,
            )
            print('res', res)
            if 'choices' in res and len(res['choices']):
                result = res['choices'][0]["text"]
        except Exception as e:
            # print('e', e)
            result = 'operation failed - ' + str(e)

        return result

    def post1(self, request):
        openai.api_key = os.environ['OPEN_AI_KEY']
        prompt = request.data.get('prompt')
        prompt_length = len(prompt)
        token_count = math.ceil(prompt_length / 4)
        max_tokens = 4000 - token_count
        ip_address = self.get_client_ip(request=request)
        user = request.user
        company = user.company
        # if not company:
        #     UserPrompt.objects.create(user=request.user, prompt=prompt, ip_address=ip_address)

        # user_prompt.save()
        # print('user_prompt', user_prompt.user)
        # all_users_prompt = UserPrompt.objects.all()
        # user_prompt = UserPrompt.objects.filter(user=request.user)
        # print('all_users_prompt', all_users_prompt.values())
        # print('user_prompt', user_prompt.values())
        response = requests.post(
            "https://api.openai.com/v1/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai.api_key}"
            },
            json={
                "model": "text-davinci-003",
                "prompt": prompt,
                "temperature": 0,
                "max_tokens": max_tokens,
                "n": 1,
                "stream": True
            },
            stream=True
        )

        def stream_response():
            for chunk in response.iter_content(chunk_size=1024):
                print('chunk', chunk)
                if chunk:
                    yield chunk

        res = StreamingHttpResponse(stream_response(), content_type='application/json')
        # res['Content-Type'] = 'application/json'
        return res

    def post(self, request):
        openai.api_key = os.environ['OPEN_AI_KEY']
        prompt = request.data.get('prompt')
        prompt_length = len(prompt)
        token_count = math.ceil(prompt_length / 4)
        max_tokens = 4000 - token_count
        ip_address = self.get_client_ip(request=request)
        user = request.user
        company = user.company
        # if not company:
        #     UserPrompt.objects.create(user=request.user, prompt=prompt, ip_address=ip_address)

        # user_prompt.save()
        # print('user_prompt', user_prompt.user)
        # all_users_prompt = UserPrompt.objects.all()
        # user_prompt = UserPrompt.objects.filter(user=request.user)
        # print('all_users_prompt', all_users_prompt.values())
        # print('user_prompt', user_prompt.values())

        exception = ''
        try:
            completion = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0,
                n=1,
                stream=True
            )

            def stream_response():
                for chunk in completion:
                    # obj = json.dumps({'answer': chunk['choices'][0]["text"]})
                    # print('obj', obj)
                    yield chunk['choices'][0]["text"]
        except Exception as e:
            exception = str(e)
            def stream_response():
                yield exception

        return StreamingHttpResponse(stream_response(), content_type='application/json')

    def conversation(self):
        completion = openai.Completion.create(engine="davinci", prompt="", max_tokens=0, n=1, stop=None,
                                              temperature=0.0, stream=True)
        conversation_id = completion['id']

        prompt = "Hello, how are you?"
        response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=1024, n=1, stop=None,
                                            temperature=0.5, stream=False, context=conversation_id)
        print(response.choices[0].text)

        prompt = "I'm doing well, thanks for asking. How about you?"
        response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=1024, n=1, stop=None,
                                            temperature=0.5, stream=False, context=conversation_id)
        print(response.choices[0].text)


