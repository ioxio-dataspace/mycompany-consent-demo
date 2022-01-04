from fastapi import APIRouter

from settings import conf

router = APIRouter()


@router.get("", summary="Get configuration for frontend", tags=["configuration"])
async def get_configuration():
    """
    Get configuration for frontend
    """
    return {
        "shareOptions": [
            {
                "label": "Person",
                "options": [
                    {
                        "label": "Minna Multanen",
                        "value": "82ec1614-292a-45a6-a538-8d1976964897",
                    },
                    {
                        "label": "Yost Robinson",
                        "value": "43ded801-79c5-4b16-8091-78bccebcdded",
                    },
                    {
                        "label": "James Jaatinen",
                        "value": "d10feb05-96b2-46a6-81f3-79520a9a704d",
                    },
                ],
            },
            {
                "label": "Company",
                "options": [
                    {
                        "label": "Digital Living International Oy",
                        "value": "7b6ac647-35b4-4d0d-95ff-558db9d4925e",
                    },
                    {
                        "label": "Oy Startup Ab",
                        "value": "b6e9c9c1-5760-44eb-8b4b-e0edf568b975",
                    },
                ],
            },
        ],
        "companies": [
            {
                "businessId": "2464491-9",
                "id": "7b6ac647-35b4-4d0d-95ff-558db9d4925e",
                "boardGroupId": "0347ec23-b2a7-48d0-99fe-96350338ff88",
                "shareholdersGroupId": "27178256-1946-4e7a-af4a-1b293786b039",
            },
            {
                "businessId": "0522908-2",
                "id": "b6e9c9c1-5760-44eb-8b4b-e0edf568b975",
                "boardGroupId": "79c3a173-e84c-4195-b006-786a818941e4",
                "shareholdersGroupId": "154e5e5c-b1f9-48e7-b827-923384f0aa9d",
            },
        ],
        "nexusBaseDomain": conf.NEXUS_BASE_DOMAIN,
    }
