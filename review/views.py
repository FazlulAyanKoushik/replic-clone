"""
    Views for Review
"""
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from product.models import Product
from review.models import Review


# Create your views here.
@permission_classes([IsAuthenticated])
class CreateProductReview(APIView):
    def get_object(self, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404

    def post(self, request, slug):
        user = request.user
        product = self.get_object(slug)

        data = request.data

        already_exists = product.review_set.filter(user=user).exists()

        if already_exists:

            return Response({
                'msg': 'Product already reviewed'
            }, status=status.HTTP_400_BAD_REQUEST)

        if int(data['rating']) < 1:
            return Response({
                'msg': 'Please select a minimum rating'
            }, status=status.HTTP_400_BAD_REQUEST)

        else:
            if user.name is None:
                name = user.email
            else:
                name = user.name
            review = Review.objects.create(
                user=user,
                product=product,
                name=name,
                rating=data['rating'],
                comment=data['comment']
            )

            reviews = product.review_set.filter()
            product.numReview = len(reviews)

            sum_of_rating = 0
            for i in reviews:
                sum_of_rating += i.rating

            product.rating = sum_of_rating / product.numReview
            product.save()

            return Response({
                'msg': 'Review added'
            }, status=status.HTTP_201_CREATED)
