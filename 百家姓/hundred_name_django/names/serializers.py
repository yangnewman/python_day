

from rest_framework import serializers

from names.models import HundredNameInfo, NamesInfo


class HundredsSerializer(serializers.ModelSerializer):

    class Meta:

        # 指定序列化的模型
        model = HundredNameInfo
        # 指定序列化哪些字段
        fields = ['title', 'url', 'nums']


class NamesSerializer(serializers.ModelSerializer):

    class Meta:

        # 指定序列化的模型
        model = NamesInfo
        # 指定序列化哪些字段
        fields = ['name', 'url', 'sex_man', 'sex_woman', 'name_poetry', 'name_explain', 'name_five_lines', 'name_three', 'name_configure', 'name_analysis']























