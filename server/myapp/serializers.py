from rest_framework import serializers

from myapp.models import (
    Thing, Classification, Tag, User, Comment, LoginLog, Order, OrderLog,
    OpLog, Banner, Ad, Notice, ErrorLog, Address, Company, Resume, Post
)


def _fmt_dt(value):
    if not value:
        return None
    return value.strftime('%Y-%m-%d %H:%M:%S')


class PostSerializer(serializers.ModelSerializer):
    create_time = serializers.SerializerMethodField()
    thing_title = serializers.SerializerMethodField()
    user_username = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_create_time(self, obj):
        return _fmt_dt(getattr(obj, 'create_time', None))

    def get_thing_title(self, obj):
        return getattr(getattr(obj, 'thing', None), 'title', None)

    def get_user_username(self, obj):
        return getattr(getattr(obj, 'user', None), 'username', None)


class ResumeSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = '__all__'

    def get_username(self, obj):
        return getattr(getattr(obj, 'user', None), 'username', None)


class CompanySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = '__all__'

    def get_username(self, obj):
        return getattr(getattr(obj, 'user', None), 'username', None)


class ThingSerializer(serializers.ModelSerializer):
    classification_title = serializers.SerializerMethodField()
    company_title = serializers.SerializerMethodField()

    class Meta:
        model = Thing
        fields = '__all__'

    def get_classification_title(self, obj):
        return getattr(getattr(obj, 'classification', None), 'title', None)

    def get_company_title(self, obj):
        return getattr(getattr(obj, 'company', None), 'title', None)


class DetailThingSerializer(serializers.ModelSerializer):
    classification_title = serializers.SerializerMethodField()

    class Meta:
        model = Thing
        exclude = ('wish', 'collect',)

    def get_classification_title(self, obj):
        return getattr(getattr(obj, 'classification', None), 'title', None)


class UpdateThingSerializer(serializers.ModelSerializer):
    classification_title = serializers.SerializerMethodField()

    class Meta:
        model = Thing
        exclude = ('wish', 'collect',)

    def get_classification_title(self, obj):
        return getattr(getattr(obj, 'classification', None), 'title', None)


class ListThingSerializer(serializers.ModelSerializer):
    classification_title = serializers.SerializerMethodField()

    class Meta:
        model = Thing
        exclude = ('wish', 'collect', 'description',)

    def get_classification_title(self, obj):
        return getattr(getattr(obj, 'classification', None), 'title', None)


class ClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    create_time = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_create_time(self, obj):
        return _fmt_dt(getattr(obj, 'create_time', None))


class CommentSerializer(serializers.ModelSerializer):
    comment_time = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'comment_time', 'like_count', 'thing', 'user', 'title', 'username']

    def get_comment_time(self, obj):
        return _fmt_dt(getattr(obj, 'comment_time', None))

    def get_title(self, obj):
        return getattr(getattr(obj, 'thing', None), 'title', None)

    def get_username(self, obj):
        return getattr(getattr(obj, 'user', None), 'username', None)


class LoginLogSerializer(serializers.ModelSerializer):
    log_time = serializers.SerializerMethodField()

    class Meta:
        model = LoginLog
        fields = '__all__'

    def get_log_time(self, obj):
        return _fmt_dt(getattr(obj, 'log_time', None))


class OpLogSerializer(serializers.ModelSerializer):
    re_time = serializers.SerializerMethodField()

    class Meta:
        model = OpLog
        fields = '__all__'

    def get_re_time(self, obj):
        return _fmt_dt(getattr(obj, 're_time', None))


class ErrorLogSerializer(serializers.ModelSerializer):
    log_time = serializers.SerializerMethodField()

    class Meta:
        model = ErrorLog
        fields = '__all__'

    def get_log_time(self, obj):
        return _fmt_dt(getattr(obj, 'log_time', None))


class OrderSerializer(serializers.ModelSerializer):
    order_time = serializers.SerializerMethodField()
    expect_time = serializers.SerializerMethodField()
    return_time = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    cover = serializers.FileField(source='thing.cover', required=False)

    class Meta:
        model = Order
        fields = '__all__'

    def get_order_time(self, obj):
        return _fmt_dt(getattr(obj, 'order_time', None))

    def get_expect_time(self, obj):
        return _fmt_dt(getattr(obj, 'expect_time', None))

    def get_return_time(self, obj):
        return _fmt_dt(getattr(obj, 'return_time', None))

    def get_username(self, obj):
        return getattr(getattr(obj, 'user', None), 'username', None)

    def get_title(self, obj):
        return getattr(getattr(obj, 'thing', None), 'title', None)

    def get_price(self, obj):
        return getattr(getattr(obj, 'thing', None), 'price', None)


class OrderLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLog
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    create_time = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = '__all__'

    def get_create_time(self, obj):
        return _fmt_dt(getattr(obj, 'create_time', None))

    def get_title(self, obj):
        return getattr(getattr(obj, 'thing', None), 'title', None)


class AdSerializer(serializers.ModelSerializer):
    create_time = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = '__all__'

    def get_create_time(self, obj):
        return _fmt_dt(getattr(obj, 'create_time', None))


class NoticeSerializer(serializers.ModelSerializer):
    create_time = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = '__all__'

    def get_create_time(self, obj):
        return _fmt_dt(getattr(obj, 'create_time', None))


class AddressSerializer(serializers.ModelSerializer):
    create_time = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = '__all__'

    def get_create_time(self, obj):
        return _fmt_dt(getattr(obj, 'create_time', None))
