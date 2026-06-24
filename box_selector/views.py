from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .services import select_box
from .models import Box

class BoxRecommendationAPI(APIView):
    def get(self, request):
        """
        Welcome to the SmartBox API!
        Send a POST request with your items data to get a box recommendation.
        Example JSON Payload:
        {
            "items": [
                {
                    "name": "Small Gadget",
                    "length": "5.00",
                    "width": "5.00",
                    "height": "5.00",
                    "weight": "0.50",
                    "quantity": 2
                }
            ]
        }
        """
        example_payload = {
            "message": "Welcome to the SmartBox API! Please send a POST request with your items.",
            "example_post_data": {
                "items": [
                    {
                        "name": "Small Gadget",
                        "length": "5.00",
                        "width": "5.00",
                        "height": "5.00",
                        "weight": "0.50",
                        "quantity": 2,
                        "is_fragile": True
                    }
                ]
            }
        }
        return Response(example_payload, status=status.HTTP_200_OK)

    def post(self, request):
        items_data = request.data.get('items', [])
        
        if not items_data:
            return Response({"error": "No items provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            selected_box = select_box(items_data)
            
            if selected_box:
                return Response({
                    "success": True,
                    "box": {
                        "name": selected_box.name,
                        "length": str(selected_box.length),
                        "width": str(selected_box.width),
                        "height": str(selected_box.height),
                        "max_weight_capacity": str(selected_box.max_weight_capacity),
                        "cost": str(selected_box.cost)
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "error": "No suitable box found for the given items."
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

def frontend_view(request):
    return render(request, 'box_selector/index.html')
