import datetime

posts_list = []


class Post(object):
    id = 1

    def __init__(self, user, title: str, body: str):
        self.id = Post.id
        self.user_id = user.id
        self.title = title
        self.body = body
        self.created_on = datetime.datetime.now()
        self.last_modified = None

    def save(self):
        Post.id += 1
        posts_list.append(self)

    def update(self, user, name: str, new_item: str):
        if user.id != self.user_id:
            raise UpdateError('this post does not belong to the selected user')
        if name == 'title':
            if self.title == new_item:
                raise UpdateError('title given matches the previous title')
        elif name == 'body':
            if self.body == new_item:
                raise UpdateError('body given matches the previous body')

        if name == 'title': self.title = new_item
        if name == 'body': self.body = new_item

        self.last_modified = datetime.datetime.now()
        return self

    def delete(self, user):
        if user.id != self.user_id:
            raise AssertionError('this post does not belong to the selected user')

        posts_list.remove(self)
        return True

    @property
    def serialize(self):
        return dict(title=self.title, body=self.body, created_on=str(self.created_on),
                    last_modified=str(self.last_modified))

    @property
    def __name__(self):
        return self.__class__.__name__


class UpdateError(AssertionError):
    def __init__(self, *args):
        AssertionError.__init__(self, *args)
