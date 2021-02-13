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
        """
        Method to retrieve latest 100 memes from database
        OR
        A specific meme if requested with a meme_id

        Path: /memes
        Method: GET

        Parameters:
        meme_id - integer

        If meme_id is not given:
            Response:
            list of latest 100 memes (sorted by created time)

        If meme_id is given:
            Response:
            name, caption, url: url to the meme image, likes, comments: list of comments on the meme 

        """

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
        """
        Method to post a new meme to the database.

        Path: /memes
        Method: POST

        Parameters:
        name, caption, url

        If duplicate of above meme exists in database:
            Response:
            HTTP status code 409 - Duplicate

        If meme_id is given:
            Response:
            meme_id: id of newly created meme
            HTTP status code 201 - Created
        """

        post_data = json.loads(request.body)

        if Meme.objects.filter(name=post_data["name"], caption=post_data["caption"], url=post_data["url"]).exists():
            return HttpResponse("Meme already exists - Duplicates, Duplicates Everywhere", status=409)

        meme = Meme(
            name=post_data["name"], caption=post_data["caption"], url=post_data["url"])
        meme.save()
        return HttpResponse(
            json.dumps({
                "id": meme.id
            }), content_type="application/json",
            status=201
        )

    def patch(self, request):
        """
        Method to update an existing meme in the database.

        Path: /memes
        Method: PATCH

        Parameters:
        meme_id, caption, url

        If duplicate of above meme exists in database:
            Response:
            HTTP status code 409 - Duplicate

        If above meme_id does not exist:
            Response:
            HTTP status code 404 - Resource (Meme) Not Found

        If meme_id exist and no duplicates exist:
            Response:
            HTTP status code 201 - Created
        """

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
        """
        Method to post a comment on a meme (specified by meme_id)

        Path: /comment
        Method: POST

        Parameters:
        meme_id, name, content

        If duplicate of above comment exists under the same meme:
            Response:
            HTTP status code 409 - Duplicate

        If above meme_id does not exist:
            Response:
            HTTP status code 404 - Resource (Meme) Not Found

        If meme_id exists and comment is not duplicate:
            Response:
            meme_id: id of meme
            comment_id: id of newly created comment
            HTTP status code 201 - Created
        """

        comment_data = json.loads(request.body)

        try:
            meme = Meme.objects.get(id=comment_data["meme_id"])
        except:
            return HttpResponse("Meme not found - Task failed successfully", status=404)

        if Comment.objects.filter(name=comment_data["name"], content=comment_data["content"], meme=meme).exists():
            return HttpResponse("Duplicate comment - dont spam here", status=409)

        comment = Comment(
            name=comment_data["name"], content=comment_data["content"], meme=meme)
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
        """
        Method to increment the likes on a meme (specified by meme_id)

        Path: /like
        Method: POST

        Parameters:
        meme_id

        If above meme_id does not exist:
            Response:
            HTTP status code 404 - Resource (Meme) Not Found

        If meme_id exists:
            Response:
            meme_id
        """

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
