from apps.mystories.models import Post


class PostService:
    @staticmethod
    def get_posts():
        return Post.objects.all()

    @staticmethod
    def get_post_by_id(post_id):
        return Post.objects.get(id=post_id)

    @staticmethod
    def create_post(data):
        return Post.objects.create(**data)

    @staticmethod
    def update_post(post_id, data):
        post = Post.objects.get(id=post_id)
        for key, value in data.items():
            setattr(post, key, value)
        post.save()
        return post

    @staticmethod
    def delete_post(post_id, user):
        try:
            post = Post.objects.get(id=post_id, author=user)
            post.delete()
        except Post.DoesNotExist:
            return None
