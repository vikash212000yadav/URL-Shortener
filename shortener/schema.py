import graphene
# graphene library contains the base GraphQL
from graphene_django import DjangoObjectType
from django.db.models import Q
from .models import URL


class URLType(DjangoObjectType):
    class Meta:
        model = URL


class Query(graphene.ObjectType):
    urls = graphene.List(URLType, url=graphene.String(), first=graphene.Int(), skip=graphene.Int())

    def resolve_urls(self, info, url=None, first=None, skip=None, **kwargs):
        queryset = URL.objects.all()

        if url:
            _filter = Q(url_o__icontains=url)
            queryset = queryset.filter(_filter)

        if first:
            queryset = queryset[:first]

        if skip:
            queryset = queryset[skip:]

        return queryset


class CreateURL(graphene.Mutation):
    url = graphene.Field(URLType)

    class Arguments:
        url_o = graphene.String()

    def mutate(self, info, url_o):
        url = URL(url_o=url_o)
        url.save()

        return CreateURL(url=url)


class Mutation(graphene.ObjectType):
    create_url = CreateURL.Field()
