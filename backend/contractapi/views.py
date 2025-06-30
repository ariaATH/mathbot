from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.web3_config_payment import Createcomp, Createcompfree, Awardwinners, AwardWithPercentage , Awardwinners , comptotal , compstatus , compexist


class CreateCompView(APIView):
    def post(self, request):
        try:
            ID = request.data.get('ID')
            Price = request.data.get('Price')
            if not ID or not Price:
                return Response({"error": "ID and Price are required."}, status=status.HTTP_400_BAD_REQUEST)

            tx_hash = Createcomp(ID, Price)
            return Response({"transaction_hash": tx_hash}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CreateCompFreeView(APIView):
    def post(self, request):
        try:
            ID = request.data.get('ID')
            if not ID:
                return Response({"error": "ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            tx_hash = Createcompfree(ID)
            return Response({"transaction_hash": tx_hash}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

