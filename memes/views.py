from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from memes.models import Meme, Comment

import json


class MemeView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(MemeView, self).dispatch(*args, **kwargs)

    def get(self, request, meme_id=None):

        if meme_id is None:
            meme_list = []

            for meme in Meme.objects.order_by("-created")[:100]:
                comment_list = []
                for comment in Comment.objects.order_by("-created").filter(meme_id=meme.id):
                    comment_data = {
                        "id": comment.id,
                        "name": comment.name,
                        "content": comment.content
                    }
                    comment_list.append(comment_data)

                meme_data = {
                    "id": meme.id,
                    "name": meme.name,
                    "url": meme.url,
                    "caption": meme.caption,
                    "likes": meme.likes,
                    "comments": comment_list,
                }
                meme_list.append(meme_data)

            return HttpResponse(json.dumps(meme_list), content_type="application/json")

        else:

            try:
                meme = Meme.objects.get(id=meme_id)
            except:
                return HttpResponse("Meme not found - Task failed successfully", status=404)

            comment_list = []
            for comment in Comment.objects.order_by("-created").filter(meme_id=meme.id):
                comment_data = {
                    "id": comment.id,
                    "name": comment.name,
                    "content": comment.content
                }
                comment_list.append(comment_data)

            meme_data = {
                "id": meme.id,
                "name": meme.name,
                "url": meme.url,
                "caption": meme.caption,
                "likes": meme.likes,
                "comments": comment_list,
            }
            return HttpResponse(
                json.dumps(meme_data), content_type="application/json"
            )

    def post(self, request):
        post_data = json.loads(request.body)

        if Meme.objects.filter(name=post_data["name"], caption=post_data["caption"], url=post_data["url"]).exists():
            return HttpResponse("Meme already exists - Duplicates, Duplicates Everywhere", status=409)

        meme = Meme(name=post_data["name"], caption=post_data["caption"], url=post_data["url"])
        meme.save()
        return HttpResponse(
            json.dumps({
                "id": meme.id
            }), content_type="application/json",
            status=201
        )

    def patch(self, request):
        meme_data = json.loads(request.body)

        try:
            meme = Meme.objects.get(id=meme_data["id"])
        except:
            return HttpResponse("Meme not found - Task failed successfully", status=404)

        if Meme.objects.filter(caption=meme_data["caption"], url=meme_data["url"]).exists():
            return HttpResponse("Modified meme already exists - What are you trying to change?", status=409)

        meme.caption = meme_data["caption"]
        meme.url = meme_data["url"]
        meme.save()

        return HttpResponse("Meme Updated - Change is good, trust me.", status=201)


    @staticmethod
    @csrf_exempt
    def post_comment(request):
        comment_data = json.loads(request.body)

        try:
            meme = Meme.objects.get(id=comment_data["meme_id"])
        except:
            return HttpResponse("Meme not found - Task failed successfully", status=404)

        if Comment.objects.filter(name=comment_data["name"], content=comment_data["content"], meme=meme).exists():
            return HttpResponse("Duplicate comment - dont spam here", status=409)

        comment = Comment(name=comment_data["name"], content=comment_data["content"], meme=meme)
        comment.save()

        return HttpResponse(
            json.dumps({
                "meme_id": meme.id,
                "id": comment.id
            }), content_type="application/json",
            status=201
        )

    @staticmethod
    @csrf_exempt
    def like_meme(request):
        meme_data = json.loads(request.body)

        try:
            meme = Meme.objects.get(id=meme_data["meme_id"])
        except:
            return HttpResponse("Meme not found - Task failed successfully", status=404)

        meme.likes = meme.likes + 1
        meme.save()

        return HttpResponse(
            json.dumps({
                "id": meme.id
            }), content_type="application/json",
            status=201
        )
