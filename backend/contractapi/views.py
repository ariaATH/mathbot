from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.web3_config_payment import Createcomp, Createcompfree, Awardwinners, AwardWithPercentage , withdrawOwner , comptotal , compstatus , compexist
import os

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

class AwardWinnersView(APIView):
    def post(self, request):
        try:
            address_1 = request.data.get('address_1')
            address_2 = request.data.get('address_2')
            address_3 = request.data.get('address_3')
            ID = request.data.get('ID')

            if not address_1 or not address_2 or not address_3 or not ID:
                return Response({"error": "All addresses and ID are required."}, status=status.HTTP_400_BAD_REQUEST)

            tx_hash = Awardwinners(address_1, address_2, address_3, ID)
            return Response({"transaction_hash": tx_hash}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AwardWithPercentageView(APIView):
    def post(self, request):
        try:
            address_1 = request.data.get('address_1')
            address_2 = request.data.get('address_2')
            address_3 = request.data.get('address_3')
            percent_1 = request.data.get('percent_1')
            percent_2 = request.data.get('percent_2')
            percent_3 = request.data.get('percent_3')
            ID = request.data.get('ID')

            if not address_1 or not address_2 or not address_3 or not percent_1 or not percent_2 or not percent_3 or not ID:
                return Response({"error": "All addresses, percentages, and ID are required."}, status=status.HTTP_400_BAD_REQUEST)

            tx_hash = AwardWithPercentage(address_1, address_2, address_3, percent_1, percent_2, percent_3, ID)
            return Response({"transaction_hash": tx_hash}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WithdrawWinnersView(APIView):
    def post(self, request):
        try:
            address = request.data.get('address')
            ID = request.data.get('ID')

            if not address or not ID:
                return Response({"error": "Address and ID are required."}, status=status.HTTP_400_BAD_REQUEST)

            tx_hash = withdrawOwner(address, ID)
            return Response({"transaction_hash": tx_hash}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CompTotalView(APIView):
    def get(self, request):
        try:
            ID = request.query_params.get('ID')
            if not ID:
                return Response({"error": "ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            total = comptotal(ID)
            return Response({"total": total}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CompStatusView(APIView):
    def get(self, request):
        try:
            ID = request.query_params.get('ID')
            if not ID:
                return Response({"error": "ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            status = compstatus(ID)
            return Response({"status": status}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CompExistView(APIView):
    def get(self, request):
        try:
            ID = request.query_params.get('ID')
            if not ID:
                return Response({"error": "ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            exist = compexist(ID)
            return Response({"exist": exist}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)